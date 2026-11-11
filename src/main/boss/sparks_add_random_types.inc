; Real TH05 Spark ring: 64 records ×16 bytes, near-Pascal center/radius/count.
SPARK_CAPACITY             equ 64
SPARK_RECORD_BYTES         equ 16
SPARK_RING_BYTES           equ (SPARK_CAPACITY * SPARK_RECORD_BYTES)
SPARK_FREE                 equ 0
SPARK_ALIVE                equ 1
SPARK_FLAG_AND_AGE         equ 0
SPARK_POSITION_X           equ 2
SPARK_POSITION_Y           equ 4
SPARK_VELOCITY             equ 10
SPARK_PLAYFIELD_X_MAX      equ (384 * 16)
SPARK_PLAYFIELD_Y_MAX      equ (368 * 16)
SPARK_COMPLETE_ANGLE       equ 100h

; Original random-spark extra angle byte within the full 16-byte record.
SPARK_ANGLE equ 14
SPARK_RANDOM_SPEED_SPAN_MASK equ ((2 * 16) - 1)
