# Shared sound: notes

- **Frames.** OP and MAINE use their own original CODE, DATA and `BGM_SOUND`
  far-call frames; MAINE's Kaja frame is `E80`, not the calibration's `E7F`.
- **SE arbitration.** A new effect replaces the current one when its priority
  is at least the current priority; after its frame limit the current effect
  is released. The priority lookup loads the current effect into BL and clears
  BH, with DX holding the new effect. Writing it as plain C++ indexing by the
  unsigned current SE (no BP frame) matches.
- **Playback state.** `snd_se_playing` starts at `SE_NONE` (`FFh`) and is
  followed by the elapsed-frame byte, starting at 0. `snd_se_reset()` restores
  both.
