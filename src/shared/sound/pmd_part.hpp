// Candidate PMD QQ work record. This defines fields, not driver storage.
#ifndef TH05_SHARED_SOUND_PMD_PART_HPP
#define TH05_SHARED_SOUND_PMD_PART_HPP
#include <stddef.h>

struct PmdLfoTiming {
    unsigned char delay, speed, step, time;
    unsigned char delay_setting, speed_setting, step_setting, time_setting;
};

// Complete 98-byte candidate layout, including the tail after the note byte.
// Signedness of fields not read here does not establish a new driver contract.
struct PmdPart {
    unsigned short playback_offset, end_return_offset;
    unsigned char remaining_length, gate_time;
    unsigned short pitch;
    short detune, lfo_delta;
    short portamento_total, portamento_step, portamento_remainder;
    unsigned char volume;
    signed char transpose;
    PmdLfoTiming lfo;
    unsigned char lfo_switch, pushed_volume;
    unsigned char modulation_depth, modulation_speed, modulation_speed_setting;
    unsigned char old_envelope_state, new_envelope_state;
    unsigned char envelope_attack, envelope_decay, envelope_sustain_rate;
    unsigned char envelope_release, envelope_sustain_level, envelope_initial_level;
    unsigned char envelope_attack_counter, envelope_decay_counter;
    unsigned char envelope_sustain_counter, envelope_release_counter;
    signed char envelope_volume;
    unsigned char extended_flags, pan_modulation, psg_mixer, instrument;
    unsigned char loop_state, fm_carrier;
    unsigned char slot1_level, slot3_level, slot2_level, slot4_level;
    unsigned char slot_mask, instrument_mask, lfo_waveform, part_mask;
    unsigned char keyoff_flags, volume_lfo_mask, gate_q, gate_Q;
    unsigned char hardware_lfo_delay, hardware_lfo_delay_counter;
    short lfo2_delta;
    PmdLfoTiming lfo2;
    unsigned char modulation2_depth, modulation2_speed, modulation2_speed_setting;
    unsigned char lfo2_waveform, volume_lfo2_mask;
    unsigned char modulation_counter, modulation_counter_setting;
    unsigned char modulation2_counter, modulation2_counter_setting;
    unsigned char note;
    unsigned char slot_delay, slot_delay_counter, slot_delay_mask;
    unsigned char algorithm_feedback, note_change_counter, minimum_gate;
    unsigned short ppz8_fnum_high;
    unsigned char untransposed_note;
    signed char master_transpose;
    unsigned char gate_random_range, reserved;
};

typedef char pmd_part_size_check[(sizeof(PmdPart) == 98) ? 1 : -1];
typedef char pmd_part_length_check[(offsetof(PmdPart, remaining_length) == 4) ? 1 : -1];
typedef char pmd_part_gate_check[(offsetof(PmdPart, gate_time) == 5) ? 1 : -1];
typedef char pmd_part_note_check[(offsetof(PmdPart, note) == 85) ? 1 : -1];
typedef char pmd_part_tail_check[(offsetof(PmdPart, reserved) == 97) ? 1 : -1];
#endif
