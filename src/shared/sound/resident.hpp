// Real-mode Kaja driver signature header and detection state.
#ifndef TH05_SOUND_RESIDENT_HPP
#define TH05_SOUND_RESIDENT_HPP
#include "src/shared/abi.hpp"
struct kaja_isr_header_t {
    unsigned char entry_jump[2];
    unsigned char magic[3];
};
// ES selects the interrupt vector table at entry to each detector.
#define KAJA_ISR(vector) (*reinterpret_cast<kaja_isr_header_t far * __es *>((vector) * 4))
#define KAJA_ISR_MAGIC(vector, a, b, c) ( \
    KAJA_ISR(vector)->magic[0] == (a) && \
    KAJA_ISR(vector)->magic[1] == (b) && \
    KAJA_ISR(vector)->magic[2] == (c) \
)
extern "C" {
    extern unsigned char snd_interrupt_if_midi;
    extern unsigned char snd_midi_possible;
    extern unsigned char snd_bgm_mode;
    extern unsigned char snd_se_mode;
}
typedef char kaja_signature_at_2[(offsetof(kaja_isr_header_t, magic) == 2) ? 1 : -1];
typedef char kaja_header_is_5[(sizeof(kaja_isr_header_t) == 5) ? 1 : -1];
#endif
