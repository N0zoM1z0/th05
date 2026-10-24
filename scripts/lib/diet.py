"""Observe DIET's target-owned decoder; decoded bytes are private evidence.

Adapted from TH04's deterministic Unicorn observation approach. The decoder's
terminal ES:DI, transfer, stack, and relocation stream are checked independently
of any reference source build. This does not regenerate a packed executable.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import struct

from .pc98 import parse_mz


UNICORN_VERSION = "1.0.2"
RELOCATION_OPCODE = b"\x26\x01\x2f"
DEFAULT_LOAD_SEGMENTS = (0x1000, 0x3333)


class DietError(ValueError):
    """A target, decoder or observation violated the decoding contract."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class DietPolicy:
    target_sha256: str
    payload_size: int
    relocation_count: int
    initial_ss: int
    initial_sp: int = 0x80
    entry_cs: int = 0
    entry_ip: int = 0


@dataclass(frozen=True)
class Relocation:
    segment: int
    offset: int
    linear: int


@dataclass(frozen=True)
class DietRun:
    load_segment: int
    relocated_payload: bytes
    relocations: tuple[Relocation, ...]
    decoded_end: int
    transfer_site: int
    final_cs: int
    final_ip: int
    final_ss: int
    final_sp: int
    instruction_count: int
    dos_version_calls: int


def normalize_payload(data: bytes, relocations: tuple[Relocation, ...], load_segment: int) -> bytes:
    """Undo only relocation additions actually observed in the target stub."""
    result = bytearray(data)
    for item in relocations:
        if item.linear < 0 or item.linear + 2 > len(result):
            raise DietError(f"relocation escapes payload: 0x{item.linear:x}")
        if item.segment * 16 + item.offset != item.linear:
            raise DietError("relocation segment:offset disagrees with linear offset")
        word = struct.unpack_from("<H", result, item.linear)[0]
        struct.pack_into("<H", result, item.linear, (word - load_segment) & 0xffff)
    return bytes(result)


def emulate_once(target: bytes, policy: DietPolicy, load_segment: int,
                 max_instructions: int = 2_000_000) -> DietRun:
    """Stop before the restored program starts; permit only DOS version query."""
    if sha256(target) != policy.target_sha256:
        raise DietError("target SHA-256 mismatch")
    if target[0x1c:0x20].lower() != b"diet":
        raise DietError("missing DIET marker at file offset 0x1c")
    image = parse_mz(target)
    if not image.valid or image.relocations or image.overlay:
        raise DietError("DIET carrier must be valid MZ without outer relocations or overlay")
    if not 0x100 <= load_segment <= 0x7000:
        raise DietError("load segment must be in 0x0100..0x7000")
    if not 0 < policy.payload_size <= 0x80000 or max_instructions <= 0:
        raise DietError("invalid payload size or instruction budget")
    try:
        import unicorn
        import unicorn.x86_const as x86
    except ImportError as error:
        raise DietError("install Unicorn 1.0.2 to observe DIET targets") from error
    if unicorn.__version__ != UNICORN_VERSION:
        raise DietError(f"Unicorn {UNICORN_VERSION} required; got {unicorn.__version__}")

    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_16)
    uc.mem_map(0, 0x200000)
    base = load_segment * 16
    psp = load_segment - 0x10
    uc.mem_write(base, image.program_image)
    uc.mem_write(psp * 16, b"\xcd\x20\x00\x90")
    for register, value in (("CS", load_segment + image.header.initial_relative_cs),
                            ("IP", image.header.initial_ip),
                            ("SS", load_segment + image.header.initial_relative_ss),
                            ("SP", image.header.initial_sp), ("DS", psp), ("ES", psp)):
        uc.reg_write(getattr(x86, "UC_X86_REG_" + register), value)

    relocations: list[Relocation] = []
    state = {"count": 0, "dos": 0, "error": None, "end": None, "transfer": None}

    def reg(name: str) -> int:
        return int(uc.reg_read(getattr(x86, "UC_X86_REG_" + name))) & 0xffff

    def fail(message: str) -> None:
        state["error"] = message
        uc.emu_stop()

    def on_code(machine, address, size, unused):
        del machine, unused
        state["count"] += 1
        if state["count"] > max_instructions:
            fail("instruction budget exceeded")
            return
        raw = bytes(uc.mem_read(address, max(size, 16)))
        # Both target stubs end decoding with POP BP; PUSH CS; POP DS;
        # ADD [restored SS],BP; ADD [far-jump CS],BP; JMP +0; MOV CX,count.
        # ES:DI still names the first byte past the decoder's complete output.
        if (raw[:5] == b"\x5d\x0e\x1f\x01\x2e"
                and raw[7:9] == b"\x01\x2e" and raw[11:14] == b"\xeb\x00\xb9"):
            if state["end"] is not None:
                fail("duplicate decoder end")
                return
            state["end"] = reg("ES") * 16 + reg("DI") - base
            if state["end"] != policy.payload_size:
                fail("decoder ES:DI output extent differs from policy")
                return
        if raw.startswith(RELOCATION_OPCODE):
            if state["end"] is None or reg("BP") != load_segment:
                fail("relocation outside restored decoder phase")
                return
            es, bx = reg("ES"), reg("BX")
            linear = es * 16 + bx - base
            if not 0 <= linear <= policy.payload_size - 2:
                fail("observed relocation escapes decoded output")
                return
            relocations.append(Relocation(es - load_segment, bx, linear))
        if raw[0] == 0xea:
            ip, cs = struct.unpack_from("<HH", raw, 1)
            if (cs, ip) != (load_segment + policy.entry_cs, policy.entry_ip):
                fail("unexpected direct far transfer")
                return
            if state["end"] is None:
                fail("entry transfer precedes decoder end")
                return
            state["transfer"] = (address - base, cs, ip)
            uc.emu_stop()

    def on_interrupt(machine, number, unused):
        del machine, unused
        if number != 0x21 or reg("AX") >> 8 != 0x30:
            fail(f"unexpected interrupt {number:02x}/AH={reg('AX') >> 8:02x}")
            return
        uc.reg_write(x86.UC_X86_REG_AX, 5)
        uc.reg_write(x86.UC_X86_REG_BX, 0)
        uc.reg_write(x86.UC_X86_REG_CX, 0)
        state["dos"] += 1

    uc.hook_add(unicorn.UC_HOOK_CODE, on_code)
    uc.hook_add(unicorn.UC_HOOK_INTR, on_interrupt)
    entry = (load_segment + image.header.initial_relative_cs) * 16 + image.header.initial_ip
    try:
        uc.emu_start(entry, 0x1fffff, count=max_instructions + 1)
    except unicorn.UcError as error:
        raise DietError(f"decoder emulation failed: {error}") from error
    if state["error"]:
        raise DietError(state["error"])
    if state["transfer"] is None:
        raise DietError("decoder did not reach restored entry transfer")
    if len(relocations) != policy.relocation_count:
        raise DietError("observed relocation count differs from policy")
    if (reg("SS") - load_segment, reg("SP")) != (policy.initial_ss, policy.initial_sp):
        raise DietError("restored stack differs from policy")
    site, cs, ip = state["transfer"]
    return DietRun(load_segment, bytes(uc.mem_read(base, policy.payload_size)),
                   tuple(relocations), state["end"], site, cs, ip, reg("SS"), reg("SP"),
                   state["count"], state["dos"])


def verify_runs(runs: list[DietRun]) -> bytes:
    """Require independent load addresses, complete bytes and relocation equality."""
    if len(runs) < 2 or len({run.load_segment for run in runs}) != len(runs):
        raise DietError("at least two distinct load segments are required")
    first = runs[0]
    payload = normalize_payload(first.relocated_payload, first.relocations, first.load_segment)
    for run in runs[1:]:
        if run.relocations != first.relocations:
            raise DietError("relocation stream depends on load segment")
        if run.decoded_end != first.decoded_end or run.transfer_site != first.transfer_site:
            raise DietError("decoder topology depends on load segment")
        if normalize_payload(run.relocated_payload, run.relocations, run.load_segment) != payload:
            raise DietError("decoded bytes depend on load segment")
    return payload


def observe(target: bytes, policy: DietPolicy,
            load_segments: tuple[int, ...] = DEFAULT_LOAD_SEGMENTS,
            max_instructions: int = 2_000_000) -> tuple[bytes, list[DietRun]]:
    if len(load_segments) < 2 or len(set(load_segments)) != len(load_segments):
        raise DietError("at least two distinct load segments are required")
    runs = [emulate_once(target, policy, segment, max_instructions) for segment in load_segments]
    return verify_runs(runs), runs
