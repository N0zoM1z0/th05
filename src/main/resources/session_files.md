# MAIN demo, EMS and face resource names: 66 initialized bytes

The original MAIN initialized DATA `[20BEC,20C2E)` contains eight actual
file or resident names: demo recording `DEMO0.REC`, launcher `op`, EMS
resident `KAIKIEMS`, bomb backdrop `BB0.CDG`, and the four character face
resources `KAO0.cd2` through `KAO3.cd2`. The original labels are anchored in
the retained native MAIN TASM source and the unrelocated original DATA bytes.

Maintained `session_files.c` groups the eight genuine C character-array
objects without pointer pooling, padding, instruction bytes or invented
runtime state. All field offsets and the complete 66-byte size are checked
at compile time. It starts at the real even DGROUP offset `021C`, immediately
after the separate three five-byte pause strings; those preceding pause
strings remain outside this owner. The true original and candidate MZ
relocation lists are both empty in the reviewed extent.

Focused receipt:
`.analysis/unit-replays/gpt-web-main-session-files-20261111/receipt.json`.
Both native Borland C/TLINK producers reproduce all **66 original bytes**;
a compiled `KAO3.cd2` to `KAO4.cd2` mutation is rejected. This is an
observed resource layout modeled as one natural C aggregate, not a claim
that the historical source declared that exact struct.

## Writable bomb-CDG filename for the actual EMS consumer (2026-11-12)

The field `main_session_files.bomb_background` is not a read-only resource
constant: the independently accepted `bomb_bg_load__ems_preload_playchar_cdgs()`
updates **byte index 2** of its original `BB0.CDG` filename to select the
current player character's background. The maintained C struct now
expresses that actual mutation by declaring this one `char[8]` field
**writable**, while leaving independently read-only filename fields
unchanged. The physical record remains 66 bytes, the bomb field remains
at offset 22, and the actual data is still ordinary initialized DATA.

The scoped native replay
`.analysis/unit-replays/gpt-web-session-bb-mutable-a/receipt.json`
produces both original 66-byte Borland C objects, with complete DATA
LEDATA/MAP and the unchanged compiled filename negative. This change
is a source mutability/ABI correction, not new byte credit or a claim
that the historical program declared this aggregate type.
