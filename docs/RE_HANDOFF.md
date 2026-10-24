# TH05 current handoff

Goal: at least 98% authored bytes exact. Commit prefix: `gpt-6.1-sol:`.
The project is newly initialized; no authored units are accepted yet.

The user's supplied Japanese image is accessible through WSL. Public
`config/targets.toml` pins its identity and four KAIKI executables. The image
digest differs from TH04's outer Japanese image, while all four TH05 executable
hashes agree with its calibration corpus. Original assets remain private.

Next: complete toolchain/bootstrap and Ghidra attestation, unpack packed targets
with an independently checked decoder, establish the ownership denominator,
then recover bounded authored functions and cold-replay them.

TH03 has unrelated uncommitted work; do not modify it. TH04 is a read-only
reference. Use an independent Wine prefix and serialize heavy jobs.
