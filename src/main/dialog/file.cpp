// .TX2 dialog script loading. Each file holds one script per player
// character; only the current character's script is read into memory.
// ReC98: th05/formats/dialog.cpp.
#pragma option -zCF_DIALOG_TEXT -zPmain_01
#include "src/main/dialog/file.hpp"

void pascal far dialog_load(const char far *fn)
{
    size_t size;
    tx2_header_t header;
    if(dialog_p) {
        hmem_free(reinterpret_cast<void __seg *>(dialog_p));
    }
    // ZUN landmine: no check of the header or of the open and read results.
    file_ropen(fn);
    file_read(&header, sizeof(header));
    size = (header.offset_for[playchar + 1] - header.offset_for[playchar]);
    dialog_p = reinterpret_cast<unsigned char far *>(hmem_allocbyte(size));
    file_seek(header.offset_for[playchar], 0);
    file_read(dialog_p, size);
    file_close();
}

// Loads _DM0<stage>.TX2.
void near dialog_load(void)
{
    dialog_fn[4] = ('0' + stage_id);
    dialog_load(dialog_fn);
}

// Relies on dialog_p's segment still being the one hmem_allocbyte()
// returned, since dialog_run() only advances its offset.
void near dialog_free(void)
{
    if(dialog_p) {
        hmem_free(reinterpret_cast<void __seg *>(dialog_p));
        dialog_p = 0;
    }
}
