; Complete foreign filename13, packed bank15 and mode bytes; no owned payload.
extrn _snd_load_fn:byte:SOUND_FILENAME_BYTES
extrn _SND_LOAD_EXT:sound_extension_bank_t
extrn _snd_se_mode:byte, _snd_bgm_mode:byte
extrn BGM_FINISH:far, BGM_INIT:far, BGM_READ_SDATA:far
extrn SND_KAJA_INTERRUPT:far
