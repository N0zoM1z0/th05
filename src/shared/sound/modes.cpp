// Natural ReC98 b6ba5b0a th04/snd/detmodes.cpp, GAME=5 behavior.
#pragma option -zCSHARED
#include <dos.h>
#include "src/shared/abi.hpp"
typedef unsigned char bool;
enum { SND_BGM_OFF = 0, SND_BGM_FM26 = 1, SND_BGM_FM86 = 2, SND_BGM_MIDI = 3, _snd_bgm_mode_t_FORCE_UINT8 = 0xFF };
enum { SND_SE_OFF = 0, SND_SE_FM = 1, SND_SE_BEEP = 2, _snd_se_mode_t_FORCE_INT16 = 0x7FFF };
static const unsigned int PMD_GET_DRIVER_TYPE_AND_VERSION = 9;
#define PMD 0x60
extern "C" {
    extern unsigned char snd_bgm_mode;
    extern unsigned char snd_se_mode;
    extern bool snd_midi_possible;
    int far snd_pmd_resident(void);
    int far snd_mmd_resident(void);
}
inline bool snd_bgm_active(void) { return snd_bgm_mode; }

extern "C" int pascal far snd_determine_modes(int req_bgm_mode, int req_se_mode)
{
	snd_pmd_resident();
	if(req_bgm_mode == SND_BGM_MIDI) {
		snd_mmd_resident();
	}
	// ZUN landmine: We should be returning if neither driver is resident!

	_AH = PMD_GET_DRIVER_TYPE_AND_VERSION;
	geninterrupt(PMD);
	if(_AL == 0xFF) {
		snd_bgm_mode = SND_BGM_OFF;
	} else if(_AL == 0x00) {
		snd_bgm_mode = SND_BGM_FM26;
	} else {
		snd_bgm_mode = SND_BGM_FM86;
	}

	if(req_se_mode == SND_SE_FM) {
		_AX = (snd_bgm_active() ? SND_SE_FM : SND_SE_OFF);
		snd_se_mode = _AX;
	} else if(req_se_mode == SND_SE_BEEP) {
		snd_se_mode = SND_SE_BEEP;
	} else {
		snd_se_mode = SND_SE_OFF;
	}

	// We tentatively set [snd_bgm_mode] above, but do we even want any?
	if(req_bgm_mode == SND_BGM_OFF) {
		snd_bgm_mode = SND_BGM_OFF;
	} else if((req_bgm_mode == SND_BGM_MIDI) && snd_midi_possible) {
		snd_bgm_mode = SND_BGM_MIDI;
	} else if((req_bgm_mode == SND_BGM_FM26) && snd_bgm_active()) {
		snd_bgm_mode = SND_BGM_FM26;
	}

	return snd_bgm_mode;
}
