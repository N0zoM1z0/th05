// Local 16-bit declarations, corroborated by nmlgc/ReC98@b6ba5b0a529edbb3.
// Layout assertions are compiler checks, not target-byte acceptance.
#ifndef TH05_SHARED_ABI_HPP
#define TH05_SHARED_ABI_HPP

#include <stddef.h>

#if !defined(__TURBOC__) || !defined(__MSDOS__)
#error TH05 exact source requires the attested 16-bit Borland DOS compiler
#endif

typedef unsigned char uint8_t;
typedef unsigned int uint16_t;
typedef unsigned long uint32_t;
typedef int pixel_t;
typedef unsigned char pixel_length_8_t;

typedef char th05_abi_byte_is_1[(sizeof(uint8_t) == 1) ? 1 : -1];
typedef char th05_abi_int_is_2[(sizeof(int) == 2) ? 1 : -1];
typedef char th05_abi_long_is_4[(sizeof(uint32_t) == 4) ? 1 : -1];

#endif
