; Original external master.lib file and allocator functions, plus real DATA.
; No linked provider implementations or initialized record bytes are owned.
extrn FILE_ROPEN:far
extrn FILE_READ:far
extrn FILE_SEEK:far
extrn FILE_CLOSE:far
extrn HMEM_ALLOCBYTE:far
extrn HMEM_FREE:far
extrn _cdg_slots:byte
extrn _cdg_noalpha:byte
extrn _cdg_images_to_load:byte
