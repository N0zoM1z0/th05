# Reconstruction workflow

1. Read the handoff; inspect `git status --short`.
2. Run `python3 scripts/preflight.py` and attest the selected analysis view.
3. Choose one reviewed function or coherent translation unit. Record artifact,
   segment:offset, complete extent, origin and confidence.
4. Recover semantics and declarations as C/C++; preserve original Borland ABI.
5. Compile in two fresh workspaces with the pinned toolchain. Inspect OMF records,
   segment layout and fixups; compare all bytes in the declared extent.
6. Reject mismatches. Store compiler experiments privately and retain concise
   replayable observations. Separate source-present from exact acceptance.
7. Run affected checks, public CI, and `git diff --check`. Update progress and
   the handoff; commit with `gpt-6.1-sol: ...` and push.

Use one CPU and low scheduling priority for heavy tools. Keep Wine writers
serial and Ghidra's heap bounded. Never modify the original HDI or executables.
