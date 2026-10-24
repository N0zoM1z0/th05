// TH05 .TX2 dialog-file format and real master.lib ABI. ReC98 source:
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47, th05/formats/dialog.hpp.
#ifndef TH05_MAIN_DIALOG_FILE_HPP
#define TH05_MAIN_DIALOG_FILE_HPP
#include "src/shared/abi.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner is TH05 MAIN dialog-file loading
#endif
static const unsigned int PLAYCHAR_COUNT = 4;
struct tx2_header_t {
    uint16_t offset_for[PLAYCHAR_COUNT + 1];
};
extern unsigned char far *dialog_p;
extern char far *dialog_fn;
extern unsigned char playchar;
extern unsigned char stage_id;
extern "C" {
    void __seg *pascal far hmem_allocbyte(unsigned bytesize);
    void pascal far hmem_free(void __seg *block);
    int pascal far file_ropen(const char far *filename);
    int pascal far file_read(void far *buffer, unsigned size);
    void pascal far file_seek(long position, int direction);
    void pascal far file_close(void);
}
void pascal far dialog_load(const char far *filename);
void near dialog_load(void);
void near dialog_free(void);
typedef char th05_tx2_header_is_10[(sizeof(tx2_header_t) == 10) ? 1 : -1];
typedef char th05_tx2_offsets_start_at_0[(offsetof(tx2_header_t, offset_for) == 0) ? 1 : -1];
typedef char th05_tx2_dialog_pointer_is_far[(sizeof(dialog_p) == 4) ? 1 : -1];
#endif
