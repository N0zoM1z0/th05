# Source-backed Master `EDGES`: 34-byte raster masks in all three EXEs

The original Master 0.23 author's public-domain `EDGES.ASM` defines one
complete **17-word (34-byte)** border mask table in initialized DATA. Its
word values begin `0000h, 0080h, 00C0h, ... 00FFh`, continue through
`80FFh, C0FFh, ... FEFFh` and end at `FFFFh`. The original Master clipping
functions use consecutive entries to select exact pixel-edge masks, not
instruction bytes or gameplay state.

| Executable | Full original EDGES extent | Actual calibration MAP public |
| --- | --- | --- |
| MAIN | `20D4C..20D6E` | `209E:038E` |
| OP | `F4D0..F4F2` | `0EFE:04F0` |
| MAINE | `102EA..1030C` | `1010:01DA` |

`python3 scripts/review_master_edges_initial.py --check` regenerates the
complete little-endian 34-byte table independently from the author's 17
binary `dw` source declarations, checks every word against the analytical
nibble mask sequence, and verifies each retained TASM source, ordinary
`_DATA` LEDATA, real MAP public, original MZ payload and ordered empty
fixup stream. This is a **102-byte** recovery of third-party initialized
DATA, not C/C++ CODE and not game-authored DATA. The neighboring 16-byte
Master CLIP initializers and six-byte FILE handles have their own separately
accepted owners; the shared boundary is not double-counted.
