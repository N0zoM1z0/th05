// Natural TH05 .TX2 loader from ReC98 th05/formats/dialog.cpp,
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47. External resource contents stay external.
#pragma option -zCF_DIALOG_TEXT -zPmain_01
#include "src/main/dialog/file.hpp"

void pascal far dialog_load(const char far *fn)
{
    size_t size;
    tx2_header_t header;
    if(dialog_p) {
        hmem_free(reinterpret_cast<void __seg *>(dialog_p));
    }
    file_ropen(fn);
    file_read(&header, sizeof(header));
    size = (header.offset_for[playchar + 1] - header.offset_for[playchar]);
    dialog_p = reinterpret_cast<unsigned char far *>(hmem_allocbyte(size));
    file_seek(header.offset_for[playchar], 0);
    file_read(dialog_p, size);
    file_close();
}

void near dialog_load(void)
{
    dialog_fn[4] = ('0' + stage_id);
    dialog_load(dialog_fn);
}

void near dialog_free(void)
{
    if(dialog_p) {
        hmem_free(reinterpret_cast<void __seg *>(dialog_p));
        dialog_p = 0;
    }
}
