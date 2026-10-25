// Native resident-program services and semantic message objects.
#ifndef TH05_ZUN_RESIDENT_INITIALIZE_HPP
#define TH05_ZUN_RESIDENT_INITIALIZE_HPP
#include "src/zun/resident/config.hpp"

extern const char ZUN_RESIDENT_ID[];
extern const char ZUN_RESIDENT_LOGO[];
extern const char ZUN_RESIDENT_NOT_FOUND[];
extern const char ZUN_RESIDENT_REMOVED[];
extern const char ZUN_RESIDENT_BAD_OPTION[];
extern const char ZUN_RESIDENT_ALREADY_PRESENT[];
extern const char ZUN_RESIDENT_NO_MEMORY[];
extern const char ZUN_RESIDENT_INITIALIZED[];
extern const char ZUN_RESIDENT_FILE_FAILURE[];

extern "C" {
    void __seg *pascal near resdata_exist(const char near *id,
        unsigned id_length, unsigned paragraphs);
    void __seg *pascal near resdata_create(const char near *id,
        unsigned id_length, unsigned paragraphs);
    void pascal near dos_free(void __seg *segment);
    void pascal near dos_puts2(const char near *message);
    void pascal near graph_clear(void);
}
#endif
