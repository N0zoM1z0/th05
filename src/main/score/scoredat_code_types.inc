; Complete TH05 GENSOU.SCR section, shared with the canonical C++ records.
SCOREDAT_PLACES equ 5
SCOREDAT_NAME_LEN equ 8
SCORE_DIGITS equ 8

SCORE_PAYLOAD struc
 SP_names db SCOREDAT_PLACES dup ((SCOREDAT_NAME_LEN + 1) dup (?))
 SP_scores db SCOREDAT_PLACES dup (SCORE_DIGITS dup (?))
 SP_stages db SCOREDAT_PLACES dup (?)
 SP_cleared db ?
 SP_unused db ?
SCORE_PAYLOAD ends

SCORE_SECTION struc
 SS_key1 db ?
 SS_key2 db ?
 SS_sum dw ?
 SS_payload SCORE_PAYLOAD <>
SCORE_SECTION ends

IF (size SCORE_PAYLOAD) ne 92
 .ERR
ENDIF
IF (size SCORE_SECTION) ne 96
 .ERR
ENDIF
