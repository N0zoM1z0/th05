// ReC98 b6ba5b0a th04/formats/scoredat/decode.cpp and impl.hpp, with the
// complete canonical score records. TH04's fixed-AL key template is omitted.
#pragma option -zCSCORE_TEXT
#include "src/op/hiscore/view.hpp"

// TC4J has no byte rotate intrinsic. This operation acts on a C++ local;
// the traversal, key mixing, checksum and return remain ordinary C++.
#define SCOREDAT_DECODE_SECTION(section, sum, index) { \
    for((index) = offsetof(scoredat_section_t, score); \
        (index) < (sizeof(scoredat_section_t) - 1); (index)++) { \
        unsigned char value = reinterpret_cast<unsigned char *>(&(section))[(index) + 1]; \
        unsigned char key = (section).key2; \
        asm { ror value, 3; } \
        value ^= key; \
        reinterpret_cast<unsigned char *>(&(section))[(index)] = \
            (section).key1 + value + reinterpret_cast<unsigned char *>(&(section))[(index)]; \
    } \
    reinterpret_cast<unsigned char *>(&(section))[(index)] += (section).key1; \
    (sum) = 0; \
    for((index) = offsetof(scoredat_section_t, score); \
        (index) < sizeof(scoredat_section_t); (index)++) { \
        (sum) += reinterpret_cast<unsigned char *>(&(section))[(index)]; \
    } \
}

uint8_t pascal near scoredat_decode(void)
{
    int index;
    int sum;
    SCOREDAT_DECODE_SECTION(hi, sum, index);
#if BINARY == 'O'
    if(hi.score_sum != sum) {
        return 1;
    }
    SCOREDAT_DECODE_SECTION(hi2, sum, index);
    return (hi2.score_sum - sum);
#else
    return (hi.score_sum - sum);
#endif
}

#undef SCOREDAT_DECODE_SECTION
