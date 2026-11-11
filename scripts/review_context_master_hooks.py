#!/usr/bin/env python3
"""Bounded original OP/MAINE Master display, file, BFNT and DOS/EGC CODE.

Review complete procedures plus PFEND's source-written portions through the
actual TASM OMF, original author source and decoded original MZ images.
The two-byte PFEND writable slot remains unowned.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file, parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned, need, sha, stored_lzh, source_blocks
from review_master_bgm import source_lines as bgm_lines
from review_main_bfnt_entry import derived_source as bfnt_derived_source
from review_master_grcg import symbolic_source
from review_context_master_large import ROOT, MASTER, real_omf, native_map, whole_source, rebind

PROOF = ROOT / 'config/context_master_hooks.json'
DECISION = ROOT / 'config/reviewed_context_master_hooks.json'
# Original native MAP publics and reviewed whole end boundaries. PFEND's
# split source-written spans are added separately below. GRAPH_PACK origin
# remains unreviewed and outside these claims.
SCOPES = (
    ('BGM_STOP_SOUND', 'libs/master.lib/bgm_stop_sound.asm', 'B_SP_SND.ASM',
     {'op': (0x3590, 32), 'maine': (0x3758, 32)}, 'equivalent-original'),
    ('GRAPH_GAIJI_PUTS', 'libs/master.lib/graph_gaiji_puts.asm', 'GRPGPUTS.ASM',
     {'op': (0x3674, 170), 'maine': (0x383c, 170)}, 'game5-gaiji-port'),
    ('GRAPH_GAIJI_PUTC', 'libs/master.lib/graph_gaiji_putc.asm', 'GRPGJPUT.ASM',
     {'op': (0x371e, 154), 'maine': (0x38e6, 154)}, 'game5-gaiji-port'),
    ('PFSTART', 'libs/master.lib/pfint21.asm', 'PFINT21.ASM',
     {'op': (0x37b8, 160), 'maine': (0x3980, 160)}, 'game5-archive-port'),
    ('PFOPEN', 'th03/formats/pfopen.asm', 'PFOPEN.ASM',
     {'op': (0x39f0, 296), 'maine': (0x3bb8, 296)}, 'game5-archive-port'),
    # These four adjacent original BFNT functions also occur in both
    # front-end executables. The 20-byte error helper is private to the
    # next exported function, not itself an exported MAP public.
    ('BFTENTRY_INVAL', 'libs/master.lib/bfnt_entry_pat.asm', 'BFTENTRY.ASM',
     {'op': (0x272, 20), 'maine': (0x272, 20)}, 'bfnt-error-branch-port'),
    ('BFNT_ENTRY_PAT', 'libs/master.lib/bfnt_entry_pat.asm', 'BFTENTRY.ASM',
     {'op': (0x286, 302), 'maine': (0x286, 302)}, 'bfnt-error-branch-port'),
    ('BFNT_HEADER_READ', 'libs/master.lib/bfnt_header_read.asm', 'BFNTHDRR.ASM',
     {'op': (0x3b4, 60), 'maine': (0x3b4, 60)}, 'original-identical'),
    ('BFNT_EXTEND_HEADER_ANALYSIS', 'libs/master.lib/bfnt_header_analysis.asm', 'BFTHDRAN.ASM',
     {'op': (0x3f0, 100), 'maine': (0x3f0, 100)}, 'original-identical'),
    # Source-identical complete Master library buffering, DOS and EGC helpers.
    ('BCLOSER', 'libs/master.lib/bcloser.asm', 'BCLOSER.ASM',
     {'op': (0x53c, 24), 'maine': (0x53c, 24)}, 'original-identical'),
    ('BFILL', 'libs/master.lib/bfill.asm', 'BFILL.ASM',
     {'op': (0x554, 60), 'maine': (0x554, 60)}, 'original-identical'),
    ('BGETC', 'libs/master.lib/bgetc.asm', 'BGETC.ASM',
     {'op': (0x5d0, 48), 'maine': (0x5d0, 48)}, 'original-identical'),
    ('BSEEK', 'libs/master.lib/bseek.asm', 'BSEEK.ASM',
     {'op': (0x706, 66), 'maine': (0x706, 66)}, 'original-identical'),
    ('BSEEK_', 'libs/master.lib/bseek_.asm', 'BSEEK_.ASM',
     {'op': (0x748, 48), 'maine': (0x748, 48)}, 'original-identical'),
    ('DOS_AXDX', 'libs/master.lib/dos_axdx.asm', 'DOSC.ASM',
     {'op': (0x778, 24), 'maine': (0x778, 24)}, 'original-identical'),
    ('DOS_READ', 'libs/master.lib/dos_read.asm', 'DOSREAD.ASM',
     {'op': (0x7c0, 26), 'maine': (0x7ce, 26)}, 'original-identical'),
    ('DOS_SEEK', 'libs/master.lib/dos_seek.asm', 'DOSSEEK.ASM',
     {'op': (0x7da, 28), 'maine': (0x7e8, 28)}, 'original-identical'),
    ('DOS_SETVECT', 'libs/master.lib/dos_setvect.asm', 'DOSVECT.ASM',
     {'op': (0x7f6, 32), 'maine': (0x804, 32)}, 'original-identical'),
    ('EGC_ON', 'libs/master.lib/egc.asm', 'EGC.ASM',
     {'op': (0x816, 22), 'maine': (0x824, 22)}, 'original-identical'),
    ('EGC_OFF', 'libs/master.lib/egc.asm', 'EGC.ASM',
     {'op': (0x82c, 32), 'maine': (0x83a, 32)}, 'original-identical'),
    ('EGC_END', 'libs/master.lib/egc.asm', 'EGC.ASM',
     {'op': (0x84c, 44), 'maine': (0x85a, 44)}, 'original-identical'),
    # Complete original Master palette, file and graphics helpers.
    ('BFNT_PALETTE_SET', 'libs/master.lib/bfnt_palette_set.asm', 'BFTPALST.ASM',
     {'op': (0x590, 64), 'maine': (0x590, 64)}, 'reviewed-native-spelling'),
    ('PALETTE_BLACK_IN', 'libs/master.lib/palette_black_in.asm', 'BLACKIN.ASM',
     {'op': (0x600, 68), 'maine': (0x600, 68)}, 'reviewed-native-spelling'),
    ('PALETTE_BLACK_OUT', 'libs/master.lib/palette_black_out.asm', 'BLACKOUT.ASM',
     {'op': (0x644, 62), 'maine': (0x644, 62)}, 'reviewed-native-spelling'),
    ('BOPENR', 'libs/master.lib/bopenr.asm', 'BOPENR.ASM',
     {'op': (0x682, 84), 'maine': (0x682, 84)}, 'reviewed-native-spelling'),
    ('BREAD', 'libs/master.lib/bread.asm', 'BREAD.ASM',
     {'op': (0x6d6, 48), 'maine': (0x6d6, 48)}, 'reviewed-native-spelling'),
    ('DOS_PUTS2', 'libs/master.lib/dos_puts2.asm', 'DOSPUTS2.ASM',
     {'op': (0x796, 42)}, 'original-identical'),
    ('DOS_FILESIZE', 'libs/master.lib/dos_filesize.asm', 'DOSFSIZE.ASM',
     {'maine': (0x790, 56)}, 'original-identical'),
    ('FILE_APPEND', 'libs/master.lib/file_append.asm', 'FILAPEND.ASM',
     {'op': (0x878, 84), 'maine': (0x886, 84)}, 'reviewed-native-spelling'),
    ('FILE_CLOSE', 'libs/master.lib/file_close.asm', 'FILCLOSE.ASM',
     {'op': (0x938, 16), 'maine': (0x946, 16)}, 'original-identical'),
    ('FILE_CREATE', 'libs/master.lib/file_create.asm', 'FILCREAT.ASM',
     {'op': (0x948, 64), 'maine': (0x956, 64)}, 'reviewed-native-spelling'),
    ('FILE_EXIST', 'libs/master.lib/file_exist.asm', 'FILEXIST.ASM',
     {'op': (0x988, 28), 'maine': (0x996, 28)}, 'reviewed-native-spelling'),
    ('FILE_ROPEN', 'libs/master.lib/file_ropen.asm', 'FILROPEN.ASM',
     {'op': (0xa58, 60), 'maine': (0xa66, 60)}, 'reviewed-native-spelling'),
    ('FILE_SEEK', 'libs/master.lib/file_seek.asm', 'FILSEEK.ASM',
     {'op': (0xa94, 52), 'maine': (0xaa2, 52)}, 'original-identical'),
    ('FILE_TELL', 'libs/master.lib/file_seek.asm', 'FILSEEK.ASM',
     {'op': (0xac8, 14), 'maine': (0xad6, 14)}, 'original-identical'),
    ('FILE_SIZE', 'libs/master.lib/file_size.asm', 'FILSIZE.ASM',
     {'maine': (0xae4, 14)}, 'original-identical'),
    ('DOS_CLOSE', 'libs/master.lib/dos_close.asm', 'FNTCLOSE.ASM',
     {'op': (0xb7c, 22), 'maine': (0xb98, 22)}, 'original-identical'),
    ('DOS_ROPEN', 'libs/master.lib/dos_ropen.asm', 'FONTOPEN.ASM',
     {'op': (0xb92, 26), 'maine': (0xbae, 32)}, 'original-identical'),
    ('GRCG_SETCOLOR', 'libs/master.lib/grcg_setcolor.asm', 'GC_SETCO.ASM',
     {'op': (0xee2, 42), 'maine': (0xf28, 42)}, 'original-identical'),
    ('GRCG_CIRCLEFILL', 'libs/master.lib/grcg_circlefill.asm', 'GC_CIRCF.ASM',
     {'maine': (0xd36, 150)}, 'reviewed-native-spelling'),
    # Complete original Master archive I/O and random-helper CODE. GAME=5
    # intentionally removes one original nibble-rotation in PFGETX1.
    ('PFCLOSE', 'libs/master.lib/pfclose.asm', 'PFCLOSE.ASM',
     {'op': (0x1afa, 26), 'maine': (0x1c94, 26)}, 'reviewed-native-spelling'),
    ('PFGETC', 'libs/master.lib/pfgetc.asm', 'PFGETC.ASM',
     {'op': (0x1b14, 16), 'maine': (0x1cae, 16)}, 'original-identical'),
    ('PFGETC1', 'libs/master.lib/pfgetc.asm', 'PFGETC.ASM',
     {'op': (0x1b24, 78), 'maine': (0x1cbe, 78)}, 'original-identical'),
    ('PFGETX0', 'libs/master.lib/pfgetc.asm', 'PFGETC.ASM',
     {'op': (0x1b72, 68), 'maine': (0x1d0c, 68)}, 'original-identical'),
    ('PFGETX1', 'libs/master.lib/pfgetc.asm', 'PFGETC.ASM',
     {'op': (0x1bb6, 14), 'maine': (0x1d50, 14)}, 'pf-game5-direct-decode'),
    ('PFREAD', 'libs/master.lib/pfread.asm', 'PFREAD.ASM',
     {'op': (0x1bc4, 46), 'maine': (0x1d5e, 46)}, 'original-identical'),
    ('PFREWIND', 'libs/master.lib/pfrewind.asm', 'PFREWIND.ASM',
     {'op': (0x1bf2, 60), 'maine': (0x1d8c, 60)}, 'original-identical'),
    ('PFSEEK', 'libs/master.lib/pfseek.asm', 'PFSEEK.ASM',
     {'op': (0x1c2e, 48), 'maine': (0x1dc8, 48)}, 'original-identical'),
    ('IRAND', 'libs/master.lib/random.asm', 'RANDOM.ASM',
     {'op': (0x1c5e, 42), 'maine': (0x1df8, 42)}, 'original-identical'),
    # Original OP residency palette and complete trapezoid rasterizer.
    # The original Master author archive has explicit GAME=5 conditional
    # ports here; no joystick-specific code shares these source claims.
    ('RESPAL_EXIST', 'libs/master.lib/respal_exist.asm', 'RSPEXIST.ASM',
     {'op': (0x2adc, 60)}, 'respal-game5-port'),
    ('RESPAL_CREATE', 'libs/master.lib/respal_exist.asm', 'RSPEXIST.ASM',
     {'op': (0x2b18, 118)}, 'respal-game5-port'),
    ('RESPAL_FREE', 'libs/master.lib/respal_free.asm', 'RSPFREE.ASM',
     {'op': (0x2b8e, 30)}, 'respal-game5-port'),
    ('draw_trapezoid', 'libs/master.lib/draw_trapezoid.asm', 'KOIZOID.ASM',
     {'op': (0x2bd6, 228)}, 'koizoid-game5-mask-port'),
    # Previously unknown OP display / machine functions and MAINE private
    # integer square-root helpers. All are complete source-written PROCs;
    # leave the following __AHINCR vendor startup and unrelated DATA unowned.
    ('GRAPH_SHOW', 'libs/master.lib/graph_show.asm', 'GRPSHOW.ASM',
     {'op': (0x193c, 6)}, 'original-identical'),
    ('GRAPH_START', 'libs/master.lib/graph_start.asm', 'GRPSTART.ASM',
     {'op': (0x1942, 38)}, 'original-identical'),
    ('JS_END', 'libs/master.lib/js_end.asm', 'JSEND.ASM',
     {'op': (0x1968, 6), 'maine': (0x1b84, 6)}, 'reviewed-native-spelling'),
    ('KEY_BEEP_OFF', 'libs/master.lib/keybeep.asm', 'KEYBEEP.ASM',
     {'op': (0x196e, 12)}, 'original-identical'),
    ('KEY_BEEP_ON', 'libs/master.lib/keybeep.asm', 'KEYBEEP.ASM',
     {'op': (0x197a, 12)}, 'original-identical'),
    ('make_linework', 'libs/master.lib/make_linework.asm', 'MAKE_LIN.ASM',
     {'op': (0x1986, 54)}, 'master-private-field-alias'),
    ('PALETTE_INIT', 'libs/master.lib/palette_init.asm', 'PALINIT.ASM',
     {'op': (0x19bc, 52)}, 'original-identical'),
    ('GRAPH_CLEAR', 'libs/master.lib/graph_clear.asm', 'GRPCLEAR.ASM',
     {'op': (0x1216, 58), 'maine': (0x1302, 58)}, 'original-identical'),
    ('GRAPH_COPY_PAGE', 'libs/master.lib/graph_copy_page.asm', 'GRPCPPG.ASM',
     {'op': (0x1250, 86), 'maine': (0x133c, 86)}, 'reviewed-native-spelling'),
    ('GET_MACHINE_98', 'libs/master.lib/get_machine_98.asm', 'GETMAC98.ASM',
     {'op': (0x0f98, 104)}, 'native-machine-near-jump-port'),
    ('IHYPOT', 'libs/master.lib/isqrt.asm', 'ISQRT.ASM',
     {'maine': (0x1af8, 24)}, 'isqrt-private-root-name'),
    ('ISQRT', 'libs/master.lib/isqrt.asm', 'ISQRT.ASM',
     {'maine': (0x1b10, 116)}, 'isqrt-private-root-name'),
    ('GRAPH_PI_FREE', 'libs/master.lib/graph_pi_free.asm', 'GRPPIFRE.ASM',
     {'op': (0x12fc, 88), 'maine': (0x13ee, 88)}, 'reviewed-native-spelling'),
    ('TEXT_CLEAR', 'libs/master.lib/text_clear.asm', 'TXCLEAR.ASM',
     {'op': (0x20fe, 18), 'maine': (0x2298, 18)}, 'original-identical'),
    ('MEM_UNASSIGN', 'libs/master.lib/mem_unassign.asm', 'MEMUNASI.ASM',
     {'op': (0x24ce, 36), 'maine': (0x270c, 36)}, 'mem-game5-conditional-port'),
    ('SUPER_ENTRY_BFNT', 'libs/master.lib/super_entry_bfnt.asm', 'SUPERBFT.ASM',
     {'op': (0x2656, 138), 'maine': (0x2894, 138)}, 'reviewed-native-spelling'),
    ('GRAPH_SCROLLUP', 'libs/master.lib/graph_scrollup.asm', 'GRPSCRLU.ASM',
     {'maine': (0x1a2e, 88)}, 'original-identical'),
    ('GRAPH_HIDE', 'libs/master.lib/graph_hide.asm', 'GRPHIDE.ASM',
     {'maine': (0x13e8, 6)}, 'original-identical'),
    ('PALETTE_WHITE_IN', 'libs/master.lib/palette_white_in.asm', 'WHITEIN.ASM',
     {'maine': (0x243c, 64)}, 'original-identical'),
    ('PALETTE_WHITE_OUT', 'libs/master.lib/palette_white_out.asm', 'WHITEOUT.ASM',
     {'maine': (0x247c, 64)}, 'original-identical'),
    # The original sources contain two complete private/near text PROCs and
    # a full 114-byte TEXT_PUTSA; the following four CODE bytes in each
    # artifact have no source LEDATA and must remain unknown.
    ('TEXT_HEIGHT', 'libs/master.lib/txesc.asm', 'TXESC.ASM',
     {'op': (0x2110, 10)}, 'original-identical'),
    ('TEXT_SYSTEMLINE_SHOWN', 'libs/master.lib/txesc.asm', 'TXESC.ASM',
     {'op': (0x211a, 10)}, 'original-identical'),
    ('TEXT_25LINE', 'libs/master.lib/txesc.asm', 'TXESC.ASM',
     {'op': (0x2124, 6)}, 'original-identical'),
    ('TEXT_20LINE', 'libs/master.lib/txesc.asm', 'TXESC.ASM',
     {'op': (0x212a, 6)}, 'original-identical'),
    ('TEXT_CURSOR_HIDE', 'libs/master.lib/txesc.asm', 'TXESC.ASM',
     {'op': (0x2130, 6)}, 'original-identical'),
    ('TEXT_CURSOR_SHOW', 'libs/master.lib/txesc.asm', 'TXESC.ASM',
     {'op': (0x2136, 6)}, 'original-identical'),
    ('TEXT_SYSTEMLINE_HIDE', 'libs/master.lib/txesc.asm', 'TXESC.ASM',
     {'op': (0x213c, 6)}, 'original-identical'),
    ('TEXT_SYSTEMLINE_SHOW', 'libs/master.lib/txesc.asm', 'TXESC.ASM',
     {'op': (0x2142, 6)}, 'original-identical'),
    ('putcmd', 'libs/master.lib/txesc.asm', 'TXESC.ASM',
     {'op': (0x2148, 22)}, 'reviewed-native-spelling'),
    ('TEXT_PUTSA', 'libs/master.lib/text_putsa.asm', 'TXPUTSA.ASM',
     {'maine': (0x22aa, 114)}, 'reviewed-native-spelling'),
)
ARTIFACTS = ('op', 'maine')
# These are the actual original CODE spans after the complete source-written
# RET instructions, not compiler-owned instructions or accepted alignment.
TEXT_UNWRITTEN_HOLES = (('th05-op', 0x215e, 0x2162),
                        ('th05-maine', 0x231c, 0x2320))
# Permitted spellings between the original Master 0.23 archived PROC and
# the real TH05 TASM source: typed pointer sizes, preserved IF LDATA arms,
# renamed BFNT header member, and actual native near-call relaxation macros.
# Every old line must occur at the reviewed multiplicity and every resulting
# line must match the complete native procedure; no compiler bytes are copied.
_TYPED_FILENAME = {
    '_push[bp+filename+2]': ('ifldata', 'pushwordptr[bp+filename+2]', 'endif'),
    'push[bp+filename]': ('pushwordptr[bp+filename]',),
}
NATIVE_SPELLINGS = {
    'BFNT_PALETTE_SET': {'test[bx].col,80h': ('test[bx].bfnt_header.col,80h',)},
    'PALETTE_BLACK_IN': {
        'callvsync_wait': ('nopcallvsync_wait',),
        'callpalette_show': ('nopcallpalette_show',),
    },
    'PALETTE_BLACK_OUT': {
        'callvsync_wait': ('nopcallvsync_wait',),
        'callpalette_show': ('nopcallpalette_show',),
    },
    'BOPENR': {
        '_push[bp+fname+2]': ('ifldata', 'pushwordptr[bp+fname+2]', 'endif'),
        'push[bp+fname]': ('pushwordptr[bp+fname]',),
        'movpferrno,pfenomem': ('movbyteptrpferrno,pfenomem',),
        'movpferrno,pfenotopen': ('movbyteptrpferrno,pfenotopen',),
    },
    'BREAD': {'_loop:push[bp+bf]': ('_loop:pushwordptr[bp+bf]',)},
    'FILE_APPEND': _TYPED_FILENAME,
    'FILE_CREATE': {**_TYPED_FILENAME, 'calldos_axdx': ('nopcalldos_axdx',)},
    'FILE_EXIST': {
        '_pushss:[bx+filename+2]': ('ifldata', 'pushwordptrss:[bx+filename+2]', 'endif'),
        'pushss:[bx+filename]': ('pushwordptrss:[bx+filename]',),
        'calldos_ropen': ('nopcalldos_ropen',),
    },
    'FILE_ROPEN': {**_TYPED_FILENAME, 'calldos_ropen': ('nopcalldos_ropen',)},
    'GRCG_CIRCLEFILL': {
        'push[bp+x]': ('pushwordptr[bp+x]',),
        'push[bp+y]': ('pushwordptr[bp+y]',),
    },
    'PFCLOSE': {'push[bp+pf]': ('pushwordptr[bp+pf]',)},
    'JS_END': {'calldos_keyclear': ('nopcalldos_keyclear',)},
    'GRAPH_COPY_PAGE': {
        'callsmem_wget': ('nopcallsmem_wget',),
        'callsmem_release': ('nopcallsmem_release',),
    },
    'GRAPH_PI_FREE': {'callhmem_free': ('nopcallhmem_free',)},
    'SUPER_ENTRY_BFNT': {
        '_push[bp+file_name+2]': ('ifldata','pushwordptr[bp+file_name+2]','endif'),
        'push[bp+file_name]': ('pushwordptr[bp+file_name]',),
    },
    'putcmd': {'putcmdproccallmodel': ('putcmdproc',)},
    'TEXT_PUTSA': {'push[bp+atrb]': ('pushwordptr[bp+atrb]',)},
}


# Observed real source OMF fixup cardinalities for the newly reviewed full functions.
EXPECTED_NATIVE_FIXUPS = {
    'BFNT_PALETTE_SET': 1,
    'PALETTE_BLACK_IN': 4,
    'PALETTE_BLACK_OUT': 3,
    'BOPENR': 5,
    'BREAD': 0,
    'DOS_PUTS2': 0,
    'DOS_FILESIZE': 0,
    'FILE_APPEND': 10,
    'FILE_CLOSE': 1,
    'FILE_CREATE': 8,
    'FILE_EXIST': 0,
    'FILE_ROPEN': 8,
    'FILE_SEEK': 3,
    'FILE_TELL': 3,
    'FILE_SIZE': 1,
    'DOS_CLOSE': 0,
    'DOS_ROPEN': 1,
    'GRCG_SETCOLOR': 0,
    'GRCG_CIRCLEFILL': 0,
    'PFCLOSE': 0,
    'PFGETC': 0,
    'PFGETC1': 0,
    'PFGETX0': 0,
    'PFGETX1': 0,
    'PFREAD': 0,
    'PFREWIND': 0,
    'PFSEEK': 0,
    'IRAND': 5,
    'RESPAL_EXIST': 2,
    'RESPAL_CREATE': 2,
    'RESPAL_FREE': 2,
    'draw_trapezoid': 26,
    'GRAPH_SHOW': 0,
    'GRAPH_START': 1,
    'JS_END': 0,
    'KEY_BEEP_OFF': 0,
    'KEY_BEEP_ON': 0,
    'make_linework': 0,
    'PALETTE_INIT': 3,
    'GRAPH_CLEAR': 2,
    'GRAPH_COPY_PAGE': 1,
    'GET_MACHINE_98': 1,
    'IHYPOT': 0,
    'ISQRT': 0,
    'GRAPH_PI_FREE': 1,
    'TEXT_CLEAR': 0,
    'MEM_UNASSIGN': 4,
    'SUPER_ENTRY_BFNT': 6,
    'GRAPH_SCROLLUP': 2,
    'PALETTE_WHITE_IN': 4,
    'PALETTE_WHITE_OUT': 4,
    'TEXT_SYSTEMLINE_SHOW': 0,
    'putcmd': 0,
    'TEXT_PUTSA': 1,
    'TEXT_HEIGHT': 0,
    'TEXT_SYSTEMLINE_SHOWN': 0,
    'TEXT_25LINE': 0,
    'TEXT_20LINE': 0,
    'TEXT_CURSOR_HIDE': 0,
    'TEXT_CURSOR_SHOW': 0,
    'TEXT_SYSTEMLINE_HIDE': 0,
    'GRAPH_HIDE': 0,
}


def game5_respal_derived(author, native, name):
    """Restrict all GAME>=2 additions to authentic source NOP and private labels."""
    original = symbolic_source(author)
    actual = symbolic_source(native)
    if name=='RESPAL_EXIST':
        changes={
            'find:':'rspexist_find:',
            'jeshortskip':'jeshortrspexist_skip',
            'repcmpsb':'repecmpsb',
            'jeshortfound':'jeshortrspexist_found',
            'skip:':'rspexist_skip:',
            'jeshortfind':'jeshortrspexist_find',
            'notfound:':'rspexist_notfound:',
            'found:':'rspexist_found:',
        }
        need(all(original.count(a)==1 for a in changes),
             'original Master residency palette search labels/CMPSB changed')
        expected=[changes.get(line,line) for line in original]
    elif name=='RESPAL_CREATE':
        changes={
            'jnzshortignore':'jnzshortrspexist_ignore',
            'create:':'rspexist_create:',
            'jcshortdame':'jcshortrspexist_dame',
            'jnbshortalloc_ok':'jnbshortrspexist_alloc_ok',
            'alloc_ok:':'rspexist_alloc_ok:',
            'dame:':'rspexist_dame:',
            'ignore:':'rspexist_ignore:',
        }
        need(all(original.count(a)==1 for a in changes) and
             original.count('pushdi')==1,
             'original Master palette-allocation register or jump labels changed')
        expected=[part for line in original for part in
                  (('pushdi','ifgamege2','nop','endif') if line=='pushdi'
                   else (changes.get(line,line),))]
    elif name=='RESPAL_FREE':
        need(original.count('jnzshortfree')==1 and
             original.count('callrespal_exist')==1,
             'original Master palette release call branch changed')
        expected=[part for line in original for part in
                  (('jnzshortfree','ifgamege2','nop','endif') if line=='jnzshortfree'
                   else (line,))]
    else:
        raise ValueError('not an original residency palette Master procedure')
    need(expected==actual,
         'native RESPAL source differs beyond original private labels and GAME>=2 NOP branch port')


def game5_trapezoid_derived(author, native):
    """One complete original KOIZOID rasterizer with explicit GAME>=3 mask."""
    import re
    original=symbolic_source(author)
    actual=symbolic_source(native)
    fields={
        'yb_adr':'koizoid_yb_adr',
        'trapez_a_dlx':'koizoid_trapez_a_dlx',
        'trapez_b_dlx':'koizoid_trapez_b_dlx',
        'trapez_a_d':'koizoid_trapez_a_d',
        'trapez_b_d':'koizoid_trapez_b_d',
        'clipxl_1':'koizoid_clipxl_1',
        'clipxl_2':'koizoid_clipxl_2',
        'clipxw_1':'koizoid_clipxw_1',
        'trapez_a+dlx':'trapez_a+koizoid_dlx',
        'trapez_b+dlx':'trapez_b+koizoid_dlx',
        'trapez_a+d':'trapez_a+koizoid_d',
        'trapez_b+d':'trapez_b+koizoid_d',
        'trapez_a+x':'trapez_a+koizoid_x',
        'trapez_b+x':'trapez_b+koizoid_x',
        'trapez_a+s':'trapez_a+koizoid_s',
        'trapez_b+s':'trapez_b+koizoid_s',
    }
    need(original.count('notax')==original.count('movax,0ffffh')==1 and
         original.count('repstosw')==1,
         'original KOIZOID opaque trapezoid inner loop differs')
    keys=re.compile('|'.join(re.escape(k) for k in sorted(fields,key=len,reverse=True)))
    # clipyb_adr is an unrelated *actual* hardware/data symbol. The original
    # `yb_adr` private self-modifying operand must not be renamed inside it.
    need(original.count('movax,clipyb_adr')==1,
         'original KOIZOID external VRAM address source changed')
    translated=[line if line=='movax,clipyb_adr'
                else keys.sub(lambda m:fields[m.group()],line)
                for line in original]
    expected=[]
    for line in translated:
        if line=='notax':
            expected += ['notax','ifgamege3','andax,trapezoid_hmask','endif']
        elif line=='movax,0ffffh':
            expected += ['ifgamege3','movax,trapezoid_hmask','else',line,'endif']
        else:
            expected.append(line)
    need(expected==actual,
         'native 228-byte KOIZOID drawing source changed beyond namespaced fields and true GAME>=3 horizontal mask')


def private_master_display_derived(author, compiled, name):
    """Only original Master author private field/label names can differ."""
    old = symbolic_source(author)
    actual = symbolic_source(compiled)
    if name == 'make_linework':
        changes = {
            'mov[bx+x],dx':'mov[bx+make_lin_x],dx',
            'mov[bx+d],ax':'mov[bx+make_lin_d],ax',
            'mov[bx+dlx],ax':'mov[bx+make_lin_dlx],ax',
            'mov[bx+s],8000h':'movwordptr[bx+make_lin_s],8000h',
        }
        need(all(old.count(key)==1 for key in changes),
             'original Master linework private fields changed')
        expected = [changes.get(line,line) for line in old]
    elif name in ('IHYPOT','ISQRT'):
        old_key = 'jmpshortroot' if name=='IHYPOT' else 'root:'
        new_key = 'jmpshortisqrt_root' if name=='IHYPOT' else 'isqrt_root:'
        need(old.count(old_key)==1, 'original square-root shared helper changed')
        expected=[line.replace(old_key,new_key) for line in old]
    else:
        raise ValueError('not a reviewed original Master private source procedure')
    need(expected==actual, 'native private Master source differs beyond verified field/label aliases: '+name)


def native_machine_98_derived(author, compiled, name):
    """Source-backed PC-98 machine probe with its retained TASM near JMP DB."""
    need(name=='GET_MACHINE_98', 'unexpected original source machine probe')
    old=symbolic_source(author)
    actual=symbolic_source(compiled)
    changes={
        'movax,fmr':'movax,fmr_98',
        'jmpget_machine_dosbox':'db0e9h,057h,001h',
    }
    need(all(old.count(key)==1 for key in changes),
         'original machine 98 branch or FM-R constant changed')
    expected=[changes.get(line,line) for line in old]
    need(expected==actual,
         'native GET_MACHINE_98 differs from original beyond pinned constant and real TASM near-jump spelling')


def native_spelling_equivalent(author, compiled, name):
    source_lines = symbolic_source(author)
    native_lines = symbolic_source(compiled)
    replacements = NATIVE_SPELLINGS[name]
    # Specific source statements are pinned, so omissions never silently
    # turn a reviewed port difference into an accepted unrelated rewrite.
    multiplicity = {'callvsync_wait': 2, 'callpalette_show': 2,
                    'callhmem_free': 3}
    for old in replacements:
        count = multiplicity.get(old, 1)
        need(source_lines.count(old) == count,
             'original Master source spelling changed: '+name+': '+old)
    expected = [part for line in source_lines
                for part in replacements.get(line, (line,))]
    need(expected == native_lines,
         'native Master procedure has unreviewed source change: '+name)

# PFEND is one original 408-byte procedure but has an actual two-byte
# unwritten CS: runtime dispatch slot. Only the two real LEDATA extents count.
PFEND_PARENT = {'op': 0x3858, 'maine': 0x3a20}
PFEND_SIZE = 408
PFEND_WRITTEN = (('PFEND_SOURCE_HEAD', 0, 156),
                 ('PFEND_SOURCE_TAIL', 158, 250))
PFEND_UNWRITTEN = (156, 2)


def upstream_procedure(archive, filename, name):
    blocks = [b for b in source_blocks(archive[filename], 'cp932')
              if b['name'].casefold() == name.casefold()]
    if name in ('PALETTE_BLACK_IN', 'PALETTE_BLACK_OUT',
                 'PALETTE_WHITE_IN', 'PALETTE_WHITE_OUT'):
        # Master 0.23 has two same-name conditional platform definitions.
        # The first, shorter complete PROC is the one used in the PC-98 code.
        need(len(blocks) == 2 and
             len(symbolic_source(blocks[0]['text'])) <
             len(symbolic_source(blocks[1]['text'])),
             'original Master PC-98 palette platform definitions changed')
        return blocks[0]
    need(len(blocks) == 1, 'original author Master procedure absent: ' + name)
    return blocks[0]


def source_linked():
    parent = json.loads(MASTER.read_text())
    archive = stored_lzh(pinned(ROOT, parent['inputs']['inner_archive']))
    results = []
    target_views = {}
    for art in ARTIFACTS:
        root = ROOT / f'.analysis/builds/{art}-calibration-a/source'
        module = 'op' if art == 'op' else 'mainem'
        source_filename = 'th05_op.asm' if art == 'op' else 'th05_maine_master.asm'
        obj_path = root / f'obj/th05/{module}.obj'
        object_bytes = obj_path.read_bytes()
        segments, blocks, fixups, groups = real_omf(object_bytes)
        map_data, offsets, publics = native_map(art, source_filename, segments)
        c = UnitContext(ROOT, art)
        original = load_unit_target(c, c.config())[1]
        target_views[art] = sha(original.program_image)
        calibration = parse_mz((root / f'bin/th05/{art}.exe').read_bytes())
        cg = int.from_bytes(calibration.program_image[1:3], 'little')
        og = int.from_bytes(original.program_image[1:3], 'little')
        need(og - cg == (1 if art == 'maine' else 0), 'unexpected artifact CRT group')
        for name, source, author, positions, adaptation in SCOPES:
            if art not in positions:
                continue
            start, size = positions[art]
            if name == 'BFTENTRY_INVAL':
                need(publics.get('BFNT_ENTRY_PAT') == {start + size} and
                     start == 0x272 and size == 20,
                     'actual private BFNT error helper boundary changed')
            elif name == 'putcmd':
                need(art == 'op' and start == 0x2148 and size == 22 and
                     publics.get('TEXT_SYSTEMLINE_SHOW') == {0x2142} and
                     publics.get('VSYNC_START') == {0x2162},
                     'private original text-command dispatcher boundary changed')
            else:
                need(publics.get(name) == {start}, 'native public entry ambiguity: '+name)
            path = root / source
            content = path.read_bytes()
            live = [b for b in source_blocks(content, 'utf8') if b['name'] == name]
            need(len(live) == 1, 'missing native full procedure source: '+name)
            upstream = upstream_procedure(archive, author,
                'INVAL' if name == 'BFTENTRY_INVAL' else name)
            # Only the BGM NOPCALL is exactly the author's unchanged semantic
            # source: TLINK's call relaxation produces its actual NOP. The
            # remaining GAME>=4 / GAME=5 edits are acknowledged explicitly,
            # not erased through opcode normalization.
            if adaptation == 'equivalent-original':
                need(bgm_lines(live[0]['text'], name) == bgm_lines(upstream['text'], name),
                     'BGM original procedure source differs')
            elif adaptation == 'game5-gaiji-port':
                need('if GAME ge 4' in live[0]['text'] and
                     'add' in live[0]['text'].lower() and
                     'adc' in upstream['text'].lower(),
                     'missing explicit GAME>=4 Master GAIJI adaptation')
            elif adaptation == 'bfnt-error-branch-port':
                # Only the original long-error branch expansion and local
                # private-label renames are allowed; copied target bytes are
                # not a substitute for the actual author PROC body.
                bfnt_derived_source(symbolic_source(upstream['text']),
                                    symbolic_source(live[0]['text']), name)
            elif adaptation == 'original-identical':
                need(symbolic_source(upstream['text']) == symbolic_source(live[0]['text']),
                     'original Master BFNT header PROC source differs')
            elif adaptation == 'reviewed-native-spelling':
                native_spelling_equivalent(upstream['text'], live[0]['text'], name)
            elif adaptation == 'respal-game5-port':
                game5_respal_derived(upstream['text'],live[0]['text'],name)
            elif adaptation == 'koizoid-game5-mask-port':
                need(name=='draw_trapezoid', 'unknown original trapezoid code family')
                game5_trapezoid_derived(upstream['text'],live[0]['text'])
            elif adaptation == 'master-private-field-alias' or adaptation == 'isqrt-private-root-name':
                private_master_display_derived(upstream['text'],live[0]['text'],name)
            elif adaptation == 'native-machine-near-jump-port':
                native_machine_98_derived(upstream['text'],live[0]['text'],name)
            elif adaptation == 'mem-game5-conditional-port':
                # The full original MEMUNASI.ASM has two GAME=1-only checks.
                # Reuse the already reviewed MAIN source transformation rather
                # than independently asserting that they are byte-equivalent.
                from review_master_gap_functions import private_source_author, source_spelling
                need(name == 'MEM_UNASSIGN' and
                     private_source_author(upstream['text'],name) ==
                     source_spelling(live[0]['text']),
                     'original Master heap bounds / GAME=1 conditional source changed')
            elif adaptation == 'pf-game5-direct-decode':
                author_lines = symbolic_source(upstream['text'])
                native_lines = symbolic_source(live[0]['text'])
                need(name == 'PFGETX1' and
                     author_lines.count('roral,4') == 1 and
                     author_lines.count('xoral,es:[pf_key]') == 1 and
                     author_lines.index('roral,4') ==
                     author_lines.index('xoral,es:[pf_key]') + 1 and
                     [x for x in author_lines if x != 'roral,4'] == native_lines,
                     'TH05 PFGETX1 source differs beyond the missing key nibble rotate')
            else:
                need(adaptation == 'game5-archive-port' and
                     'if GAME eq 5' in live[0]['text'] and
                     ('pf' in live[0]['text'].lower()),
                     'missing actual GAME=5 original Master file-port branch')
            # All source is from the real native compilation object. Compare
            # source LEDATA, every ordered FIXUPP and both MZ images, whole.
            blob = whole_source(blocks, start, size)
            actions = [x for x in fixups if start <= x['site'] < start + size]
            if name in EXPECTED_NATIVE_FIXUPS:
                need(len(actions) == EXPECTED_NATIVE_FIXUPS[name],
                     'original Master source OMF fixup count changed: '+name)
            cal, native, linked, mz = rebind(blob, actions, start, offsets, segments,
                                            groups, cg, og)
            need(cal == calibration.program_image[start:start+size] and
                 native == original.program_image[start:start+size],
                 'complete linked native Master function differs: '+art+':'+name)
            need(relative_fixups(calibration, start, size) ==
                 relative_fixups(original, start, size) == mz,
                 'original ordered MZ relocations differ: '+name)
            need(original.program_image.find(native) == start and
                 original.program_image.find(native, start+1) == -1,
                 'original complete CODE occurrence not unique: '+name)
            results.append({
                'artifact': 'th05-'+art, 'member': name, 'start': start,
                'end': start + size, 'size': size, 'source': source,
                'original_archive_member': author, 'source_adaptation': adaptation,
                'native_OMF_sha256': sha(object_bytes), 'native_MAP_sha256': sha(map_data),
                'native_source_sha256': sha(content),
                'native_procedure_sha256': sha(live[0]['text'].encode('utf8')),
                'original_procedure_sha256': sha(upstream['text'].encode('utf8')),
                'unlinked_CODE_sha256': sha(blob), 'calibrated_CODE_sha256': sha(cal),
                'native_CODE_sha256': sha(native), 'original_ordered_MZ': mz,
                'ordered_OMF_actions': linked, 'authored_credit': 0,
            })
        # The full PFEND native procedure is 408 bytes but has two *real*
        # unwritten runtime state bytes. Determine those bytes from the
        # original OMF LEDATA coverage, not from target content or a guessed
        # gap. Every remaining byte and FIXUPP must be source-linked exactly.
        parent_start = PFEND_PARENT[art]
        parent_offset = parent_start - 0x272
        written = bytearray(PFEND_SIZE)
        for pos, data in blocks:
            low = max(parent_offset, pos)
            high = min(parent_offset + PFEND_SIZE, pos + len(data))
            if low >= high:
                continue
            begin, end = low - parent_offset, high - parent_offset
            need(not any(written[begin:end]), 'PFEND source LEDATA overlaps')
            written[begin:end] = b'\1' * (end - begin)
        expected_mask = bytearray(PFEND_SIZE)
        for _, begin, length in PFEND_WRITTEN:
            expected_mask[begin:begin+length] = b'\1' * length
        need(written == expected_mask,
             'complete PFEND CODE source-written / runtime slot split changed')
        gap_at = parent_start + PFEND_UNWRITTEN[0]
        need(calibration.program_image[gap_at:gap_at+2] ==
             original.program_image[gap_at:gap_at+2] == b'\0\0',
             'PFEND runtime-written dispatch words differ from original zero state')
        need(publics.get('PFEND') == {parent_start} and
             publics.get('PFOPEN') == {parent_start + PFEND_SIZE},
             'original PFEND whole-function public boundaries changed')
        pf_source = 'libs/master.lib/pfint21.asm'
        pf_content = (root / pf_source).read_bytes()
        pf_live = [b for b in source_blocks(pf_content, 'utf8') if b['name'] == 'PFEND']
        need(len(pf_live) == 1 and 'if GAME eq 5' in pf_live[0]['text'],
             'real GAME=5 PFEND source not preserved')
        pf_author = upstream_procedure(archive, 'PFINT21.ASM', 'PFEND')
        for role, begin, length in PFEND_WRITTEN:
            start = parent_start + begin
            blob = whole_source(blocks, start, length)
            actions = [x for x in fixups if start <= x['site'] < start+length]
            cal, native, linked, mz = rebind(blob, actions, start,
                                            offsets, segments, groups, cg, og)
            need(cal == calibration.program_image[start:start+length] and
                 native == original.program_image[start:start+length],
                 'native original PFEND source-written CODE differs: '+art+':'+role)
            need(relative_fixups(calibration, start, length) ==
                 relative_fixups(original, start, length) == mz,
                 'PFEND ordered source-written MZ relocations differ')
            need(original.program_image.find(native) == start and
                 original.program_image.find(native, start+1) == -1,
                 'original PFEND full source-written subextent not unique')
            results.append({
                'artifact': 'th05-'+art, 'member': role, 'start': start,
                'end': start+length, 'size': length, 'source': pf_source,
                'original_archive_member': 'PFINT21.ASM',
                'source_adaptation': 'game5-archive-port-omf-written',
                'complete_parent': [parent_start, PFEND_SIZE],
                'unwritten_slot': [gap_at, 2],
                'native_OMF_sha256': sha(object_bytes), 'native_MAP_sha256': sha(map_data),
                'native_source_sha256': sha(pf_content),
                'native_procedure_sha256': sha(pf_live[0]['text'].encode('utf8')),
                'original_procedure_sha256': sha(pf_author['text'].encode('utf8')),
                'unlinked_CODE_sha256': sha(blob), 'calibrated_CODE_sha256': sha(cal),
                'native_CODE_sha256': sha(native), 'original_ordered_MZ': mz,
                'ordered_OMF_actions': linked, 'authored_credit': 0,
            })
    # Both uninitialized four-byte stretches immediately follow genuine
    # complete RETs; prove the original native TASM LEDATA never wrote them.
    # Comparing target zero bytes alone would not prove their source origin.
    for art,low,high in TEXT_UNWRITTEN_HOLES:
        croot=ROOT / f'.analysis/builds/{art.removeprefix("th05-")}-calibration-a/source'
        module='op' if art=='th05-op' else 'mainem'
        obj=(croot / f'obj/th05/{module}.obj').read_bytes()
        segs,bodies,fixups,groups=real_omf(obj)
        need(all(pos+len(buf) <= low-0x272 or pos >= high-0x272 for pos,buf in bodies) and
             not any(low<=f['site']<high for f in fixups),
             'native TASM unexpectedly writes original text CODE scratch slots')
        ctx=UnitContext(ROOT, art.removeprefix('th05-'))
        original=load_unit_target(ctx,ctx.config())[1]
        cal=parse_mz((croot / f'bin/th05/{art.removeprefix("th05-")}.exe').read_bytes())
        need(original.program_image[low:high] == cal.program_image[low:high] == b'\0'*(high-low),
             'unwritten original text helper bytes are no longer zero')
        need(all(r['end']<=low or r['start']>=high for r in results if r['artifact']==art),
             'original text helper claim swallows unreviewed CODE hole')
    return {
        'schema_version': 1, 'kind': 'original-OP-MAINE-Master-derived-file-and-display',
        'scopes': results, 'source_written_CODE_bytes': sum(x['size'] for x in results),
        'text_unwritten_holes': [list(x) for x in TEXT_UNWRITTEN_HOLES],
        'target_view_sha256': target_views,
        'author_archive_sha256': parent['inputs']['inner_archive']['sha256'],
        'parent_Master_sha256': digest_file(MASTER),
        'verifier_sha256': digest_file(ROOT/'scripts/review_context_master_hooks.py'),
        'authored_credit': 0, 'non_CODE_claimed': 0,
    }


def validate(record):
    parent = json.loads(MASTER.read_text())
    expected = [row for art in ARTIFACTS
                for row in ([('th05-'+art, name, positions[art][0], positions[art][1])
                             for name, _, _, positions, _ in SCOPES if art in positions] +
                            [('th05-'+art, role, PFEND_PARENT[art]+start, length)
                             for role, start, length in PFEND_WRITTEN])]
    need(record.get('schema_version') == 1 and
         record.get('kind') == 'original-OP-MAINE-Master-derived-file-and-display' and
         record.get('source_written_CODE_bytes') == sum(t[3] for t in expected) and
         record.get('author_archive_sha256') == parent['inputs']['inner_archive']['sha256'] and
         record.get('parent_Master_sha256') == digest_file(MASTER) and
         record.get('verifier_sha256') == digest_file(ROOT/'scripts/review_context_master_hooks.py') and
         record.get('authored_credit') == record.get('non_CODE_claimed') == 0,
         'source-linked Master review metadata changed')
    views = record.get('target_view_sha256', {})
    need(set(views) == set(ARTIFACTS) and all(
         isinstance(views[a], str) and re.fullmatch('[0-9a-f]{64}', views[a])
         for a in ARTIFACTS), 'native decoded artifact identities absent')
    need(record.get('text_unwritten_holes') == [list(x) for x in TEXT_UNWRITTEN_HOLES],
         'unowned original text helper CODE holes altered or claimed')
    rows = record.get('scopes', [])
    need([(r['artifact'],r['member'],r['start'],r['size']) for r in rows] == expected,
         'source-listed original complete Master function extents changed')
    for art,low,high in TEXT_UNWRITTEN_HOLES:
        need(all(r['artifact']!=art or r['end']<=low or r['start']>=high for r in rows),
             'source claim intersects unknown original text command bytes')
    for r in rows:
        known = next((scope for scope in SCOPES if scope[0] == r['member']), None)
        if known is None:
            art = r['artifact'].removeprefix('th05-')
            role = next((x for x in PFEND_WRITTEN if x[0] == r['member']), None)
            need(role is not None and art in ARTIFACTS and
                 r['complete_parent'] == [PFEND_PARENT[art], PFEND_SIZE] and
                 r['unwritten_slot'] == [PFEND_PARENT[art]+PFEND_UNWRITTEN[0], 2] and
                 r['source'] == 'libs/master.lib/pfint21.asm' and
                 r['original_archive_member'] == 'PFINT21.ASM',
                 'PFEND source-write provenance / excluded runtime hole changed')
        else:
            need(r['source'] == known[1] and r['original_archive_member'] == known[2],
                 'Master source/author member changed')
        if r['member'] in EXPECTED_NATIVE_FIXUPS:
            need(len(r['ordered_OMF_actions']) == EXPECTED_NATIVE_FIXUPS[r['member']],
                 'complete native Master OMF fixup evidence is missing')
        need(r['end'] == r['start']+r['size'] and r['authored_credit'] == 0 and
             r['original_ordered_MZ'] ==
             [a['site'] for a in r['ordered_OMF_actions'] if a['kind'] == 2] and
             r['source_adaptation'] == (known[4] if known else
                                         'game5-archive-port-omf-written'),
             'source FIXUPP/complete boundary or GAME port declaration differs')
        for k in ('native_OMF_sha256','native_MAP_sha256','native_source_sha256',
                  'native_procedure_sha256','original_procedure_sha256',
                  'unlinked_CODE_sha256','calibrated_CODE_sha256','native_CODE_sha256'):
            need(isinstance(r.get(k), str) and re.fullmatch('[0-9a-f]{64}',r[k]),
                 'Master original source evidence missing')
    if DECISION.exists():
        d = json.loads(DECISION.read_text())
        need(d.get('schema_version') == 1 and
             d.get('decision') == 'ADOPT_ONLY_COMPLETE_MASTER_FILE_DISPLAY_CODE' and
             d.get('evidence_sha256') == digest_file(PROOF) and
             d.get('scopes') == [[r['artifact'],r['member']] for r in rows] and
             d.get('CODE_bytes') == record['source_written_CODE_bytes'] and
             d.get('authored_credit') == 0 and d.get('other_claims') == 0,
             'master context original CODE decision changed')


def reviewed_claims(root, artifact, view, *, verify_targets=False):
    if not DECISION.exists():
        return [], None
    need(root.resolve() == ROOT.resolve(), 'wrong Master source checkout')
    record = json.loads(PROOF.read_text()); validate(record)
    need(record['target_view_sha256'][artifact] == view['sha256'],
         'decoded original target identity changed')
    if verify_targets:
        need(source_linked() == record, 'original native Master code differs')
    rows = [r for r in record['scopes'] if r['artifact'] == 'th05-'+artifact]
    return ([{'start':r['start'],'end':r['end'], 'kind':'verified-vendor-code',
              'library':'Master 0.23-derived GAME=5', 'member':r['member'],
              'authored_credit':0} for r in rows],digest_file(DECISION))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    m = p.add_mutually_exclusive_group(required=True)
    m.add_argument('--write', action='store_true')
    m.add_argument('--check', action='store_true')
    m.add_argument('--structural-check', action='store_true')
    a = p.parse_args()
    if a.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'will not overwrite accepted original source evidence')
        result = source_linked()
        PROOF.write_text(json.dumps(result, indent=2)+'\n')
        print('PASS original Master file/display scope',result['source_written_CODE_bytes'])
    else:
        record=json.loads(PROOF.read_text());validate(record)
        if a.check:
            need(source_linked()==record, 'original source-linked Master CODE changed')
            print('PASS original Master hooks native bytes and ordered fixups')
        else:print('PASS original Master hook source-current structural proof')

if __name__ == '__main__':
    main()
