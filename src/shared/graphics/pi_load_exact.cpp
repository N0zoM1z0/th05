// TH05 .PI slot load with original near-slot free and master.lib far loader.
#pragma option -zCSHARED -2 -k-
#include <dos.h>
extern void far *pi_buffers[8];
extern unsigned char pi_headers[8][72];
extern "C" int pascal far graph_pi_load_pack(const char far *fn, void far *header, void far *buffer_slot);
extern "C" void pascal near pi_free(int slot);
#pragma codeseg SHARED
int pascal far pi_load(int slot, const char far *fn)
{
    _DI = slot;
    asm { push di }
    asm { push cs }
    asm { call near ptr pi_free }
    _SI = _DI;
    _SI <<= 2;
    _SI += FP_OFF(pi_buffers);
    asm { imul di, di, 72 }
    _DI += FP_OFF(pi_headers);
    return graph_pi_load_pack(fn, reinterpret_cast<void far *>(reinterpret_cast<void near *>(_DI)), reinterpret_cast<void far *>(reinterpret_cast<void near *>(_SI)));
}
