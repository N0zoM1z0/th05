// Script subcommands, interpreted only after their controlling top-level byte.
// The same printable character can have a different meaning in each handler.
#ifndef TH05_CUTSCENE_SUBCOMMANDS_HPP
#define TH05_CUTSCENE_SUBCOMMANDS_HPP

enum CutsceneScriptSubcommand {
    CUTSCENE_BOX_SKIP_WAIT = '-',
    CUTSCENE_COLOR_MAP_ASSIGN = '=',
    CUTSCENE_FADE_OUT = 'o',
    CUTSCENE_FADE_IN = 'i',
    CUTSCENE_WAIT_FOR_MEASURE = 'm',
    CUTSCENE_WAIT_EXTRA_KEY = 'k',
    CUTSCENE_SHOW_PAGE = 'p',
    CUTSCENE_FADE_MUSIC = 'm',
    CUTSCENE_GAIJI_DIRECT = 'a',
    CUTSCENE_PIC_USE_PALETTE = '=',
    CUTSCENE_PIC_KEEP_PALETTE = '@',
    CUTSCENE_PIC_FREE = '-',
    CUTSCENE_PIC_PALETTE_ONLY = 'p',
    CUTSCENE_PIC_LOAD_NAME = ',',
    CUTSCENE_QUARTER_TRANSITION = '=',
    CUTSCENE_ESCAPE_COMMAND = 0x5c,
    CUTSCENE_INLINE_GAIJI = '@',
    CUTSCENE_INLINE_SWEAT = 't',
    CUTSCENE_INLINE_HEART = 'h',
    CUTSCENE_INLINE_QUESTION = '?',
    CUTSCENE_INLINE_EXCLAMATION = '!'
};

// Defaults on parameter-free script operations. Changing these values alters
// actual scene timing or colors, not just a source spelling.
enum CutsceneScriptDefaults {
    CUTSCENE_WAIT_DEFAULT_FRAMES = 64,
    CUTSCENE_TONE_NORMAL = 100,
    CUTSCENE_TONE_APPLY_FRAMES = 1,
    CUTSCENE_DEFAULT_MEASURE_FADE = 1,
    CUTSCENE_QUARTER_TRANSITION_DELAY = 1,
    CUTSCENE_PAGE_FOREGROUND = 0,
    CUTSCENE_PAGE_BACKGROUND = 1
};

#endif
