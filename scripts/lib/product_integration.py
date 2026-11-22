"""Link accepted maintained units into the ReC98-scaffolded DOS product.

The product build (`scripts/build_reference.py --overlay`) starts from ReC98's
tree, whose undecompiled code lives in the IDA-derived dumps (`th05_main.asm`,
`th05_maine.asm`) and the ASM files they include. This module replaces dump
procedures with the accepted maintained units that reproduce them:

1. Compile every eligible unit module into `obj/integ/`.
2. Mark every dump procedure public, relink once, and read the procedure
   addresses from the MAP. The bytes do not change.
3. Locate each unit object's code in that image: all bytes outside the
   object's FIXUPP fields must match. The dump procedures that tile the match
   are removed from the source and declared `extrn` instead.
4. Give the unit object alias PUBDEFs for the removed names, so dump callers
   and other ReC98 modules resolve to the maintained code.

Position does not matter for a working product: the relink audit showed that
the ReC98 code is position independent.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import shutil
import tomllib

from .omf import parse_omf
from .omf_edit import (add_aliases_at, externs, fixups, lnames_segments, object_segments, publics,
                       rename_externs)
from .pc98 import parse_mz

PROC = re.compile(r"^[ \t]*([A-Za-z_@$?][\w@$?]*)[ \t]+proc\b([^\r\n;]*)", re.I | re.M)
INCLUDE = re.compile(r"^[ \t]*include[ \t]+(\S+\.asm)\b", re.I | re.M)
PUBLIC = re.compile(r"^[ \t]*public[ \t]+([^\r\n;]+)", re.I | re.M)
MAP_PUBLIC = re.compile(r"^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?(\S+)\s*$", re.M)
MAP_ROW = re.compile(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)")
DUMPS = {"main": ("th05_main.asm", "obj\\th05\\main.obj"),
         "maine": ("th05_maine.asm", "obj\\th05\\maine.obj")}
SPECIAL = ("compiler_pipeline", "generated_sources", "bindings_after_compiler", "binary")


@dataclass
class Proc:
    name: str
    path: Path
    start: int  # character offsets of the complete proc ... endp block
    end: int
    distance: str


@dataclass
class Module:
    index: int
    module: str
    entry: dict
    units: list[str] = field(default_factory=list)
    obj: str = ""


def dump_files(root: Path, top: str) -> list[Path]:
    order, stack = [], [root / top]
    while stack:
        path = stack.pop(0)
        if path in order or not path.is_file():
            continue
        order.append(path)
        for match in INCLUDE.finditer(path.read_text(encoding="cp932", errors="surrogateescape")):
            stack.append(root / match[1].replace("\\", "/"))
    return order


def scan_procs(files: list[Path]) -> list[Proc]:
    procs = []
    for path in files:
        text = path.read_text(encoding="cp932", errors="surrogateescape")
        for match in PROC.finditer(text):
            name = match[1]
            end = re.compile(r"^[ \t]*" + re.escape(name) + r"[ \t]+endp\b[^\n]*\n?", re.I | re.M).search(
                text, match.end())
            if not end:
                continue
            words = match[2].lower().split()
            distance = "far" if "far" in words else "near"
            procs.append(Proc(name, path, match.start(), end.end(), distance))
    return procs


def map_publics(path: Path) -> dict[str, int]:
    text = path.read_text(encoding="cp437")
    head = text.find("Publics by Value")
    table = text[head:] if head >= 0 else text
    return {m[3]: int(m[1], 16) * 16 + int(m[2], 16) for m in MAP_PUBLIC.finditer(table)}


def map_contributions(path: Path) -> list[tuple[int, int, str, str, str, int, str]]:
    """(start, size, class, segment, module, frame, group) of every nonempty contribution."""
    rows = []
    for line in path.read_text(encoding="cp437").splitlines():
        m = MAP_ROW.match(line)
        if m and int(m[3], 16):
            rows.append((int(m[1], 16) * 16 + int(m[2], 16), int(m[3], 16), m[4], m[5], m[7], int(m[1], 16), m[6]))
    return rows


DATA_LABEL = re.compile(r"^[ \t]*([A-Za-z_?$][\w@$?]*)[ \t]+(?:db|dw|dd|df|dq|dt|label)\b", re.I | re.M)


def scan_data_labels(files: list[Path]) -> dict[Path, list[tuple[int, str]]]:
    """Data label definitions outside STRUC/UNION bodies: path -> [(offset, name)]."""
    found = {}
    for path in files:
        text = path.read_text(encoding="cp932", errors="surrogateescape")
        skip = []
        for m in re.finditer(r"^[ \t]*\w+[ \t]+(?:struc|union)\b.*?^[ \t]*\w*[ \t]*ends\b", text, re.I | re.M | re.S):
            skip.append((m.start(), m.end()))
        rows = [(m.start(), m[1]) for m in DATA_LABEL.finditer(text)
                if not any(a <= m.start() < b for a, b in skip)]
        if rows:
            found[path] = rows
    return found


def eligible_modules(project: Path, artifact: str, overlaid: set[str], reference: Path) -> tuple[list[Module], dict]:
    suffix = "" if artifact == "main" else f".{artifact}"
    entries = tomllib.loads((project / f"config/exact_units{suffix}.toml").read_text())["units"]
    accepted = {u["id"] for u in json.loads((project / f"config/accepted_units{suffix}.json").read_text())["units"]}
    modules: dict[str, Module] = {}
    skipped = {"special-pipeline": [], "rec98-tu": [], "data": []}
    for entry in entries:
        if entry["id"] not in accepted:
            continue
        module = entry["module"]
        if entry.get("extent_kind") == "initialized-data" or "data" in entry.get("origin", ""):
            skipped["data"].append(entry["id"])
            continue
        if any(key in entry for key in SPECIAL):
            skipped["special-pipeline"].append(entry["id"])
            continue
        if module in overlaid or (reference / module).exists():
            skipped["rec98-tu"].append(entry["id"])
            continue
        if module not in modules:
            modules[module] = Module(len(modules), module, entry)
        elif (modules[module].entry["source"], modules[module].entry.get("wrapper_options")) != (
                entry["source"], entry.get("wrapper_options")):
            raise ValueError(f"module {module} has two different sources")
        modules[module].units.append(entry["id"])
    return list(modules.values()), skipped


def code_segments(raw: bytes) -> dict[int, tuple[str, bytes, set[int]]]:
    """Code segment index -> (name, LEDATA image, fixup-covered offsets)."""
    _, segments, _ = lnames_segments(raw)
    images = object_segments(raw)
    return {i: (segments[i - 1][0], bytes(images[i][0]), images[i][1])
            for i in images if segments[i - 1][1] == "CODE" and images[i][0]}


def find_masked(image: bytes, data: bytes, covered: set[int]) -> list[int]:
    n = len(data)
    best, start = (0, 0), None
    for i in range(n + 1):
        if i < n and i not in covered:
            start = i if start is None else start
        else:
            if start is not None and i - start > best[1] - best[0]:
                best = (start, i)
            start = None
    a, b = best
    if b - a < 8:
        return []
    hits, p = [], image.find(data[a:b])
    while p != -1:
        base = p - a
        if base >= 0 and base + n <= len(image) and all(
                image[base + i] == data[i] for i in range(n) if i not in covered):
            hits.append(base)
        p = image.find(data[a:b], p + 1)
    return hits


def asm_failed(output: str) -> bool:
    """TASM /t prints nothing on success."""
    return "**Error**" in output or "**Fatal**" in output


KEEP = (r"^[ \t]*(\w+[ \t]+ends\b|\w+[ \t]+segment\b|include\b|assume\b|public\b"
        r"|extrn\b|extern\b|\S+[ \t]+procdesc\b)")
UNDEFINED_ASM = re.compile(r"\*\*Error\*\* (\S+)\((\d+)\) Undefined symbol: (\S+)")
TLINK_UNDEFINED = re.compile(r"Undefined symbol (\S+) in module (\S+)", re.I)
TLINK_DUPLICATE = re.compile(r"(\S+(?: \S+)*?) defined in module (\S+) is duplicated in module (\S+)", re.I)


def base_name(symbol: str) -> str:
    """Comparable base: @NAME$Q..., TLINK's NAME(args), _name and Class::name -> name."""
    name = symbol.split("(")[0].split("::")[-1]
    if name.startswith("@"):
        name = name[1:].split("$")[0].split("@")[-1]
    elif name.startswith("_"):
        name = name[1:]
    return name.lower()


class Integration:
    def __init__(self, project: Path, source: Path, artifact: str, run, tasm_arguments: list[str],
                 overlaid: set[str]):
        self.project, self.source, self.artifact, self.run = project, source, artifact, run
        self.dump, self.dump_obj = DUMPS[artifact]
        self.tasm_arguments = tasm_arguments  # flags only, without source/object
        self.overlaid = overlaid
        self.extra_labels: set[str] = set()
        self.label_kinds: dict[str, str] = {}
        self.publicize: set[str] = set()
        self.label_owner: dict[str, tuple[str, str]] = {}
        self.excluded: dict[str, str] = {}
        self.log: list[str] = []

    # -- helpers ---------------------------------------------------------
    def dos(self, *args: str) -> list[str]:
        return ["wine", str(self.project / "_reference/ReC98/bin/msdos.exe"), "-e", "-x", *args]

    def assemble(self, output: str, label: str) -> str:
        result = self.run(label, ["wine", r"C:\TASM50\bin\TASM32.EXE", *self.tasm_arguments, self.dump, output],
                          check=False)
        return result

    def response(self) -> tuple[str, str]:
        path = self.source / f"bin/th05/{self.artifact}.rsp"
        return path.read_bytes().decode("ascii"), str(path)

    def link(self, label: str, objects_text: str, exe: str, map_path: str) -> str:
        text, path = self.response()
        body = text.replace("+\r\n", " ").strip()
        objs, files = body.split(",", 1)
        rest = files.split(",")[2:]
        args = objs.split()
        lines, line = [], []
        for arg in args + objects_text.split():
            line.append(arg)
            if len(" ".join(line)) > 100:
                lines.append(" ".join(line))
                line = []
        if line:
            lines.append(" ".join(line))
        rsp = "+\r\n".join(lines) + f", {exe}, {map_path}," + ",".join(rest) + "\r\n"
        temp = self.source / f"bin/th05/{label}.rsp"
        temp.write_bytes(rsp.encode("ascii"))
        return self.run(label, self.dos("tlink", "@" + str(temp.relative_to(self.source)).replace("/", "\\")),
                        check=False)

    # -- steps -----------------------------------------------------------
    def compile_modules(self) -> None:
        from .unit_context import compiler_arguments
        from .replay_toolchain import include_closure
        self.modules, self.skipped = eligible_modules(self.project, self.artifact, self.overlaid,
                                                      self.source)
        (self.source / "integ").mkdir(exist_ok=True)
        (self.source / "obj/integ").mkdir(parents=True, exist_ok=True)
        converted = set()
        for module in self.modules:
            entry = module.entry
            if entry.get("source_encoding") == "cp932":
                for name in include_closure(self.project, entry["source"]):
                    if name.startswith("src/") and name not in converted:
                        path = self.source / name
                        try:  # the overlay step may already have converted it
                            path.write_bytes(path.read_bytes().decode("utf-8").encode("cp932"))
                        except UnicodeDecodeError:
                            pass
                        converted.add(name)
            stem = f"u{module.index:03d}"
            prefix = f"#pragma option {entry['wrapper_options']}\n" if entry.get("wrapper_options") else ""
            (self.source / f"integ/{stem}.cpp").write_text(prefix + f'#include "{entry["source"]}"\n')
            binary = {"main": "M", "op": "O", "maine": "E"}[self.artifact]
            arguments = compiler_arguments(entry, binary)[:-1] + ["-nobj/integ/", f"integ/{stem}.cpp"]
            module.obj = f"obj\\integ\\{stem}.obj"
            wrapper = (self.source / f"integ/{stem}.cpp").read_text()
            stamp = self.source / f"obj/integ/{stem}.src"
            if not (self.source / f"obj/integ/{stem}.obj").exists() or not stamp.exists() or stamp.read_text() != wrapper:
                (self.source / f"obj/integ/{stem}.obj").unlink(missing_ok=True)
                out = self.run(f"integ-{stem}", self.dos("tcc", *arguments), check=False)
                if re.search(r"(?m)^Error ", out):
                    self.excluded[module.module] = "compile failed"
                stamp.write_text(wrapper)
                if (self.source / f"obj/integ/{stem}.obj").exists():
                    shutil.copyfile(self.source / f"obj/integ/{stem}.obj", self.source / f"obj/integ/{stem}.pri")
            if not (self.source / f"obj/integ/{stem}.pri").exists():
                self.excluded[module.module] = "compile failed"
        # Edited copies are written to .obj; the pristine compiler output stays in .pri.
        self.objects = {m.module: (self.source / m.obj.replace("\\", "/")).with_suffix(".pri").read_bytes()
                        for m in self.modules if m.module not in self.excluded}

    def marker(self) -> None:
        """Relink once with a plain public marker label before every dump procedure and data label."""
        files = dump_files(self.source, self.dump)
        self.files = files
        self.procs = scan_procs(files)
        originals = {path: path.read_text(encoding="cp932", errors="surrogateescape") for path in files}
        self.label_kinds, self.label_owner = {}, {}
        inserts: dict[Path, list[tuple[int, str]]] = {}
        self.markers: dict[str, tuple[str, str]] = {}  # marker -> (kind, spelled name)
        for number, proc in enumerate(self.procs):
            inserts.setdefault(proc.path, []).append((proc.start, f"MKP_{number}"))
            self.markers[f"MKP_{number}"] = ("proc", proc.name)
        number = 0
        for path, rows in scan_data_labels(files).items():
            for offset, name in rows:
                inserts.setdefault(path, []).append((offset, f"MKD_{number}"))
                self.markers[f"MKD_{number}"] = ("data", name)
                number += 1
        for label in sorted(self.extra_labels):
            for path in files:
                text = originals[path]
                match = re.search(r"^[ \t]*(" + re.escape(label) + r")(?:[ \t]*(:)|[ \t]+label[ \t]+(\w+))",
                                  text, re.I | re.M)
                if match:
                    self.label_kinds[match[1]] = "near" if match[2] else match[3].lower()
                    inserts.setdefault(path, []).append((match.start(), f"MKL_{len(self.label_kinds)}"))
                    self.markers[f"MKL_{len(self.label_kinds)}"] = ("label", match[1])
                    break
        for path, items in inserts.items():
            text = originals[path]
            for offset, marker in sorted(items, reverse=True):
                text = text[:offset] + f"public {marker}\n{marker} label byte\n" + text[offset:]
            path.write_text(text, encoding="cp932", errors="surrogateescape")
        try:
            out = self.assemble("obj\\th05\\marker.obj", "marker-asm")
            if asm_failed(out):
                raise RuntimeError("marker assembly failed:\n" + out[-2000:])
        finally:
            for path, text in originals.items():
                path.write_text(text, encoding="cp932", errors="surrogateescape")
        self.link_replacing("marker-link", self.dump_obj, "obj\\th05\\marker.obj", "bin\\th05\\marker.exe",
                            "obj\\th05\\marker.map")
        self.image = parse_mz((self.source / "bin/th05/marker.exe").read_bytes()).program_image
        found = map_publics(self.source / "obj/th05/marker.map")
        self.addresses = {}
        self.by_address: dict[int, list[str]] = {}
        for marker, (kind, name) in self.markers.items():
            if marker in found:
                self.addresses[name.lower()] = found[marker]
                self.by_address.setdefault(found[marker], []).append(name)
        self.declared = {}
        for text in originals.values():
            for match in PUBLIC.finditer(text):
                for name in match[1].split(","):
                    self.declared.setdefault(name.strip().lower(), name.strip())
        rows = map_contributions(self.source / "obj/th05/marker.map")
        self.rows = rows
        dump_module = Path(self.dump).name.lower()
        self.dump_rows = [r for r in rows if r[4].lower() == dump_module and r[2] == "CODE"]
        self.object_publics(rows)
        exe = self.source / f"obj/th05/{self.artifact}.map"
        self.real_publics = {n.lower() for n in map_publics(exe)} if exe.exists() else set()

    def object_publics(self, rows) -> None:
        """Add the mangled publics of every other linked object at their linked addresses."""
        text, _ = self.response()
        names = text.replace("+\r\n", " ").split(",", 1)[0].split()[3:]
        starts: dict[tuple[str, str], list[int]] = {}
        for row in rows:
            starts.setdefault((row[4].lower(), row[3]), []).append(row[0])
        for name in names:
            path = self.source / name.replace("\\", "/")
            if not path.exists() or name.lower() == self.dump_obj.lower():
                continue
            raw = path.read_bytes()
            module = raw[4:4 + raw[3]].decode("cp437").lower()
            segments = lnames_segments(raw)[1]
            for public, (_, segment, offset) in publics(raw).items():
                if not segment:
                    continue
                where = starts.get((module, segments[segment - 1][0]))
                if where and len(where) == 1:
                    self.by_address.setdefault(where[0] + offset, []).append(public)

    def link_replacing(self, label, old_obj, new_obj, exe, map_path) -> str:
        text, path = self.response()
        body = text.replace("+\r\n", " ").strip()
        objs, files = body.split(",", 1)
        objs = " ".join(new_obj if o.lower() == old_obj.lower() else o for o in objs.split())
        rest = files.split(",")[2:]
        temp = self.source / f"bin/th05/{label}.rsp"
        words, lines, line = objs.split(), [], []
        for word in words:
            line.append(word)
            if len(" ".join(line)) > 100:
                lines.append(" ".join(line))
                line = []
        if line:
            lines.append(" ".join(line))
        temp.write_bytes(("+\r\n".join(lines) + f", {exe}, {map_path}," + ",".join(rest) + "\r\n").encode("ascii"))
        return self.run(label, self.dos("tlink", "@" + str(temp.relative_to(self.source)).replace("/", "\\")),
                        check=False)

    def plan(self) -> None:
        located = []
        for proc in self.procs:
            address = self.addresses.get(proc.name.lower())
            if address is not None and any(s <= address < s + n for s, n, *_ in self.dump_rows):
                located.append((address, proc))
        located.sort(key=lambda item: item[0])
        starts = [a for a, _ in located]
        self.removals: dict[str, list[Proc]] = {}
        self.aliases: dict[str, dict[str, tuple[int, int]]] = {}
        self.matches: dict[str, dict[int, int]] = {}
        self.spans: dict[str, list[tuple[Path, int, int]]] = {}
        claimed: set[str] = set()
        for module in self.modules:
            if module.module in self.excluded:
                continue
            raw = self.objects[module.module]
            segs = code_segments(raw)
            removed, aliases, spans = [], {}, []
            for index, (name, data, covered) in segs.items():
                hits = find_masked(self.image, data, covered)
                if len(hits) != 1:
                    self.excluded[module.module] = f"{len(hits)} matches for {name}"
                    break
                start, end = hits[0], hits[0] + len(data)
                inside = [(a, p) for a, p in located if start <= a < end]
                following = [a for a in starts if a >= end]
                before = [a for a in starts if a < start]
                if not inside or inside[0][0] != start:
                    self.excluded[module.module] = f"{name} does not start at a dump procedure"
                    break
                row = [r for r in self.dump_rows if r[0] <= start < r[0] + r[1]]
                if not row or end > row[0][0] + row[0][1]:
                    self.excluded[module.module] = f"{name} leaves its dump segment"
                    break
                if following and following[0] < end:
                    self.excluded[module.module] = f"{name} ends inside a dump procedure"
                    break
                for address, proc in inside:
                    removed.append(proc)
                    aliases[proc.name] = (index, address - start)
                    aliases[self.exported(proc.name)] = (index, address - start)
                # Text that ends the region: the next procedure when the region reaches it.
                tail = None
                if following and end <= following[0] < end + 16:  # at most alignment in between
                    nxt = next(p for a, p in located if a == following[0])
                    last = inside[-1][1]
                    if nxt.path == last.path:
                        tail = nxt.start
                    else:  # the next procedure opens an included file
                        text = last.path.read_text(encoding="cp932", errors="surrogateescape")
                        relative = str(nxt.path.relative_to(self.source)).replace("/", "[/\\\\]")
                        hit = re.compile(r"^[ \t]*include[ \t]+" + relative + r"\b", re.I | re.M).search(text, last.end)
                        if hit:
                            tail = hit.start()
                row_end = row[0][0] + row[0][1]
                if tail is None and end >= row_end - 15 and (not following or following[0] >= row_end):
                    last = inside[-1][1]  # the region closes its dump segment
                    text = last.path.read_text(encoding="cp932", errors="surrogateescape")
                    hit = re.compile(r"^[ \t]*\w+[ \t]+ends\b", re.I | re.M).search(text, last.end)
                    if hit:
                        tail = hit.start()
                files = {p.path for _, p in inside}
                if len(files) == 1:
                    first, last = inside[0][1], inside[-1][1]
                    between = [p for a, p in located if p.path == first.path and first.start < p.start < last.start
                               and not start <= a < end]
                    finish = tail if tail else last.end
                    ours = {id(p) for _, p in inside}
                    strays = [p for p in self.procs if p.path == first.path and first.start <= p.start < finish
                              and id(p) not in ours]
                    if not between and not strays:
                        spans.append((first.path, first.start, finish))
                for label, kind in self.label_kinds.items():
                    address = self.addresses.get(label.lower())
                    if address is not None and start <= address < end:
                        aliases[label] = (index, address - start)
                        self.label_owner[label.lower()] = (module.module, kind)
            if module.module in self.excluded:
                continue
            names = {p.name.lower() for p in removed}
            if names & claimed:
                self.excluded[module.module] = "procedures already replaced by another module"
                continue
            claimed |= names
            self.removals[module.module] = removed
            self.spans[module.module] = spans
            self.matches[module.module] = {index: find_masked(self.image, data, covered)[0]
                                           for index, (_, data, covered) in segs.items()}
            self.aliases[module.module] = aliases

    def group_frame(self, raw: bytes, frame: tuple | None) -> int | None:
        if not frame or frame[0] != 1:
            return None
        name = lnames_segments(raw)[2][frame[1] - 1][0].lower()
        frames = [r[5] for r in self.rows if r[6].lower() == name]
        return min(frames) if frames else None

    def extern_name(self, module: str, reported: str) -> str | None:
        """Our EXTDEF spelling of a symbol TLINK reported (possibly demangled)."""
        names = externs(self.objects[module])
        if reported in names:
            return reported
        found = [n for n in names if base_name(n) == base_name(reported)]
        return found[0] if len(found) == 1 else None

    def exported(self, name: str) -> str:
        """TASM exports a public with the spelling of its PUBLIC directive."""
        return self.declared.get(name.lower(), name)

    def dump_name(self, name: str) -> str | None:
        """The exported spelling of a procedure or data label defined in the dump, if any."""
        lowered = name.lower()
        found = next((n for names in self.by_address.values() for n in names
                      if n.lower() == lowered and n.lower() in self.addresses), None)
        return self.exported(found) if found else None

    def resolve(self, module: str, symbol: str) -> str | None:
        """The product symbol that the matched ReC98 code uses where we reference `symbol`."""
        raw = self.objects[module]
        names = externs(raw)
        images = object_segments(raw)
        for fix in fixups(raw):
            if fix["target_method"] != 2 or names[fix["target_index"] - 1] != symbol:
                continue
            start = self.matches.get(module, {}).get(fix["segment"])
            if start is None:
                continue
            at = start + fix["offset"]
            word = int.from_bytes(self.image[at:at + 2], "little")
            ours = int.from_bytes(bytes(images[fix["segment"]][0][fix["offset"]:fix["offset"] + 2]), "little")
            candidates = []
            if fix["kind"] == 3:
                segment = int.from_bytes(self.image[at + 2:at + 4], "little")
                candidates = [segment * 16 + word - fix["displacement"]]
            elif fix["kind"] in (1, 5):
                if fix["self_relative"]:
                    frame = next(r[5] for r in self.rows if r[0] <= at < r[0] + r[1])
                    candidates = [frame * 16 + ((at - frame * 16 + 2 + word) & 0xFFFF)]
                else:
                    frame = self.group_frame(raw, fix["frame"])
                    if frame is None:
                        continue
                    candidates = [frame * 16 + ((word - fix["displacement"]) & 0xFFFF),
                                  frame * 16 + ((word - fix["displacement"] - ours) & 0xFFFF)]
            for address in candidates:
                found = self.by_address.get(address, [])
                if found:
                    best = sorted(found, key=lambda n: (n.lower().startswith(("sub_", "loc_", "byte_", "word_", "dword_", "unk_")), n))[0]
                    return self.exported(best)
        return None

    def apply(self) -> None:
        removed = {p.name.lower() for procs in self.removals.values() for p in procs}
        cuts: dict[Path, list[tuple[int, int, list[Proc]]]] = {}
        for module, procs in self.removals.items():
            spans = self.spans.get(module, [])
            covered = set()
            for path, begin, finish in spans:
                inside = [p for p in procs if p.path == path and begin <= p.start < finish]
                cuts.setdefault(path, []).append((begin, finish, inside))
                covered |= {id(p) for p in inside}
            for proc in procs:
                if id(proc) not in covered:
                    cuts.setdefault(proc.path, []).append((proc.start, proc.end, [proc]))
        for path in self.files:
            text = path.read_text(encoding="cp932", errors="surrogateescape")
            for begin, finish, procs in sorted(cuts.get(path, []), key=lambda c: -c[0]):
                block = text[begin:finish]
                # The cut may hold segment-closing, include and declaration lines; keep those,
                # together with their backslash continuation lines.
                kept, carry = [], False
                for line in re.findall(r"^[^\n]*\n?", block, re.M):
                    if carry or re.match(KEEP, line, re.I):
                        kept.append(line)
                        carry = line.rstrip("\r\n").rstrip().endswith("\\")
                kept = "".join(kept)
                inner = [f"\textrn {label}:{kind}\n" for label, kind in self.label_kinds.items()
                         if re.search(r"^[ \t]*" + re.escape(label) + r"\b", block, re.I | re.M)]
                declared = "".join(f"\textrn {self.exported(p.name)}:{p.distance}\n" for p in procs)
                text = text[:begin] + declared + "".join(inner) + kept + text[finish:]

            def keep(match: re.Match) -> str:
                names = [n.strip() for n in match[1].split(",")]
                left = [n for n in names if n.lower() not in removed]
                return (match.group(0).replace(match[1], ", ".join(left)) if left else "")
            text = PUBLIC.sub(keep, text)
            for name in sorted(self.publicize):
                match = re.search(r"^[ \t]*" + re.escape(name) + r"(?:[ \t]*:|[ \t]+(?:proc|label|db|dw|dd|df|dq)\b)",
                                  text, re.I | re.M)
                if match:
                    text = text[:match.start()] + f"public {name}\n" + text[match.start():]
            path.write_text(text, encoding="cp932", errors="surrogateescape")
        for module, aliases in self.aliases.items():
            path = self.source / next(m.obj for m in self.modules if m.module == module).replace("\\", "/")
            path.write_bytes(add_aliases_at(self.objects[module], aliases))

    def segments_for_anchor(self) -> list[tuple[str, str]]:
        """(segment, group) of every code segment in the integrated objects."""
        out = []
        for module in self.removals:
            raw = (self.source / next(m.obj for m in self.modules if m.module == module).replace("\\", "/")).read_bytes()
            _, segments, groups = lnames_segments(raw)
            for number, (name, klass) in enumerate(segments, 1):
                if klass != "CODE":
                    continue
                group = next((g for g, members in groups if number in members), "(none)")
                out.append((name, group))
        return out
