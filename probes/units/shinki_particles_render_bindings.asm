; Real monochrome sprite API and full foreign particle pool; no owned bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
SHINKI_PARTICLE_TEXT segment byte public 'CODE' use16
assume cs:SHINKI_PARTICLE_TEXT
public Z_SUPER_ROLL_PUT_16X16_MONO_RAW
org (0C21Eh - 0AE10h)
Z_SUPER_ROLL_PUT_16X16_MONO_RAW label near
org (10CB2h - 0AE10h)
SHINKI_PARTICLE_TEXT ends
main_01 group SHINKI_PARTICLE_TEXT
; Natural paragraph placement accommodates either complete candidate extent.
SHINKI_PARTICLE_DGROUP_GAP segment para public 'CODE' use16
org (209D0h - 10D60h)
SHINKI_PARTICLE_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _boss_particles
org 04684h
_boss_particles label byte
org 04A84h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
