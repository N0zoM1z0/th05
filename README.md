# 東方怪綺談 ～ Mystic Square

<p align="center">
  <img src="resources/progress.svg" alt="TH05 authored byte exact reconstruction progress">
</p>

Source reconstruction of the original Japanese PC-98 **Touhou 5: Mystic Square**.
The goal is **98% authored bytes exact** across `MAIN.EXE`, `OP.EXE`,
`MAINE.EXE` and `ZUN.COM`, with maintained C/C++ and justified original assembly.

The project reuses the build and analysis lessons from
[TH04](https://github.com/N0zoM1z0/th04) and
[TH03](https://github.com/N0zoM1z0/th03). ReC98 is a pinned candidate reference;
its progress and exactness labels do not transfer to this repository.

Work has started with private target attestation, reproducible tooling and an
independent exact oracle. No authored-byte denominator has been accepted yet;
unreviewed ownership is not silently excluded. Packed-file equality and decoded
function equality will be reported separately.

## Setup

Use your own Japanese game image. Game executables, assets, disk images and
proprietary compiler binaries are never included in this repository.

```sh
python3 scripts/import_targets.py /path/to/jp.hdi
python3 scripts/preflight.py
mkdir -p _reference
git clone https://github.com/nmlgc/ReC98.git _reference/ReC98
git -C _reference/ReC98 checkout --detach b6ba5b0a529edbb31efdf8c0e939263804f8ee47
bash scripts/bootstrap_toolchain.sh
bash scripts/bootstrap_analysis_toolchain.sh
bash scripts/run_heavy.sh python3 scripts/attest_toolchain.py
bash scripts/run_heavy.sh python3 scripts/ghidra.py th05-main import
```

An existing attested TH03/TH04 installation can be reused with
`bash scripts/bootstrap_toolchain.sh --from /path/to/th04` and the equivalent
analysis bootstrap option. This creates independent Wine state and reuses
immutable analysis tools. Bootstrap refuses to overlay an existing installation.
Ghidra defaults to one CPU and a 384 MiB Java heap. The heavy-job wrapper sets
a 35% CPU quota, 768 MiB memory limit, no swap, and low scheduling priority.

`python3 -m pip install -r requirements-ci.txt` installs the pinned instruction
observer used by the DIET decoder and its public negative controls.
`bash scripts/run_heavy.sh python3 scripts/unpack_targets.py` exports private
decoded payloads and ordered relocation streams. OP/MAINE execute their original
decoders at two distinct load segments; MAIN is already unpacked and ZUN is COM.

The target manifest pins the supplied copy, with `candidate-local-attested`
provenance. Independent pristine-dump confirmation remains open.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `MAIN.EXE` | 149,990 | `c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0` |
| `OP.EXE` | 44,450 | `c94efc071a4b1adf8ce6e2c5a7eefb9eb47c26f8bab61b2e58e736dda8130abb` |
| `MAINE.EXE` | 44,321 | `8308c416e756a07766f9f66dbf5575fa12c09189059226931a9562e7272b6997` |
| `ZUN.COM` | 18,116 | `5044ae03f7c0333f37d88ef34e244502f90d7314287f6f387c07569e4e0b120e` |

## Reconstruction

- [Current handoff](docs/RE_HANDOFF.md)
- [Workflow](docs/RE_WORKFLOW.md)
- [Exact oracle contract](docs/ORACLES.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Progress](docs/PROGRESS.md)

Product source lives under `src/main/`, `src/op/`, `src/maine/`, `src/zun/` and
`src/shared/`. One Borland/Wine build or Ghidra analysis runs at a time.

Repository-authored code and documentation are MIT licensed. Original game and
third-party materials retain their respective rights; see [provenance](docs/PROVENANCE.md).
