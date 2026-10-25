// Natural resident-program entry candidate; native acceptance is separate.
#pragma option -2
#include "src/zun/resident/initialize.hpp"

#define ZUN_ARG_IS(arg, upper, lower) \
    (((arg)[0] == '-' || (arg)[0] == '/') && \
     ((arg)[1] == (upper) || (arg)[1] == (lower)))

int main(int argc, const unsigned char **argv)
{
    resident_t __seg *seg;
    int i;
    resident_t far *resident;
    unsigned char far *resident_bytes;
    const char *res_id = ZUN_RESIDENT_ID;

    seg = reinterpret_cast<resident_t __seg *>(resdata_exist(res_id,
        sizeof(((resident_t *)0)->id) - 1, (sizeof(resident_t) + 15) >> 4));
    dos_puts2(ZUN_RESIDENT_LOGO);
    graph_clear();
    if(argc == 2) {
        if(ZUN_ARG_IS(argv[1], 'R', 'r')) {
            if(!seg) {
                dos_puts2(ZUN_RESIDENT_NOT_FOUND);
                return 1;
            }
            dos_free(seg);
            dos_puts2(ZUN_RESIDENT_REMOVED);
            return 0;
        } else if(ZUN_ARG_IS(argv[1], 'D', 'd')) {
            debug = 1;
        } else {
            dos_puts2(ZUN_RESIDENT_BAD_OPTION);
            return 1;
        }
    }
    if(seg) {
        dos_puts2(ZUN_RESIDENT_ALREADY_PRESENT);
        return 1;
    }
    seg = reinterpret_cast<resident_t __seg *>(resdata_create(res_id,
        sizeof(((resident_t *)0)->id) - 1, (sizeof(resident_t) + 15) >> 4));
    if(!seg) {
        dos_puts2(ZUN_RESIDENT_NO_MEMORY);
        return 1;
    }
    resident_bytes = reinterpret_cast<unsigned char far *>(seg);
    dos_puts2(ZUN_RESIDENT_INITIALIZED);
    for(i = sizeof(((resident_t *)0)->id); i < sizeof(resident_t); i++) {
        resident_bytes[i] = 0;
    }
    if(cfg_init(seg)) {
        dos_free(seg);
        dos_puts2(ZUN_RESIDENT_FILE_FAILURE);
        return 1;
    }
    resident = reinterpret_cast<resident_t far *>(resident_bytes);
    if(debug) {
        resident->debug = true;
    }
    return 0;
}

#undef ZUN_ARG_IS
