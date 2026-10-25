; Foreign full mask bank and three complete word states, no initialized payload.
extrn _PI_MASKS:word:(PI_MASK_COUNT*PI_MASK_H)
extrn _pi_mask_ptr:word, _pi_mask_y:word, _pi_put_masked_vram_offset:word
extrn @pi_mask_setup_egc_and_advance$qv:near
extrn GRAPH_PACK_PUT_8_NOCLIP:far, EGC_OFF:far
