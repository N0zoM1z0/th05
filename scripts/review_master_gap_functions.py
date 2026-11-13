#!/usr/bin/env python3
"""Complete source-backed Master functions and initialized literal data.

The original Master 0.23 archive, unchanged native TASM OMF and real MAIN MZ
must all agree. Accept only explicitly named full procedures, never nearby
alignment or game-authored bytes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.omf import parse_omf
from lib.pc98 import parse_mz, digest_file
from lib.unit_oracle import relative_fixups
from review_master import object_text, source_blocks, stored_lzh, pinned, need, sha, idx
from review_master_bgm import linked_scope
from review_main_runtime import startup

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'config/master_vendor_ownership.json'
PROOF = ROOT / 'config/master_gap_functions_ownership.json'
DECISION = ROOT / 'config/reviewed_master_gap_functions.json'
# Original listing boundaries, not discovered from matching target bytes.
MEMBERS = (
    ('rtc_int_set',       0x0454, 145),
    ('RTC_INT',           0x04f8, 68),
    ('BFNT_PALETTE_SET',  0x0590, 64),
    ('GAIJI_PUTCA',      0x1d7a, 68),
    ('FILE_ROPEN',       0x0df2, 60),
    ('GET_MACHINE',      0x1d5e, 28),
    ('GRAPH_CLEAR',      0x1e62, 36),
    ('JS_END',           0x1fa6, 6),
    ('LARGEPUT_DISP8',    0x20dc, 69),
    ('make_linework',     0x2122, 54),
    ('PFCLOSE',          0x2262, 26),
    ('PFGETX1',          0x231e, 13),
    ('PALETTE_ENTRY_RGB', 0x23f0, 66),
    ('IRAND',            0x23c6, 42),
    ('TEXT_FILLCA',      0x2508, 56),
    ('TEXT_PUTSA',       0x2598, 114),
    ('VSYNC_START',      0x260e, 106),
    ('VSYNC_COUNT',      0x2682, 58),
    ('VSYNC_END',        0x26bc, 72),
    ('VSYNC_WAIT',       0x2704, 38),
    ('PALETTE_WHITE_IN', 0x272a, 64),
    ('PALETTE_WHITE_OUT',0x276a, 64),
    ('MEM_UNASSIGN',      0x29c6, 36),
    ('EMS_EXIST',        0x4000, 34),
    ('EMS_SETNAME',      0x4052, 26),
    ('EMS_SPACE',        0x40ce, 24),
    ('SUPERPT8_DISP',     0x4162, 79),
)

# The retained native-source names of three *actual private procedures*
# differ from their independently preserved Master 0.23 archive names.
PRIVATE_AUTHOR = {
    'LARGEPUT_DISP8': ('LARGEPUT.ASM', 'DISP8'),
    'SUPERPT8_DISP': ('SUPERPT8.ASM', 'DISP'),
    'make_linework': ('MAKE_LIN.ASM', 'make_linework'),
    'FILE_ROPEN': ('FILROPEN.ASM', 'FILE_ROPEN'),
    'GET_MACHINE': ('GETMACHI.ASM', 'GET_MACHINE'),
    'JS_END': ('JSEND.ASM', 'JS_END'),
    'PFCLOSE': ('PFCLOSE.ASM', 'PFCLOSE'),
    'PFGETX1': ('PFGETC.ASM', 'PFGETX1'),
    'PALETTE_ENTRY_RGB': ('RGBLOAD.ASM', 'PALETTE_ENTRY_RGB'),
    'MEM_UNASSIGN': ('MEMUNASI.ASM', 'MEM_UNASSIGN'),
}
# The two real single-byte *non-procedure* positions stay unknown. The first
# differs between the calibration EVEN NOP and original zero; the second is
# an original alignment zero at the end of the SUPERPT8 helper.
UNOWNED_BOUNDARIES = (0x2121, 0x41b1)
PRIVATE_OMF_ACTION_COUNTS = {
    'LARGEPUT_DISP8': 2, 'make_linework': 0, 'SUPERPT8_DISP': 0,
    'FILE_ROPEN': 8, 'GET_MACHINE': 0, 'JS_END': 0, 'PFCLOSE': 0,
    'PFGETX1': 0, 'PALETTE_ENTRY_RGB': 3, 'MEM_UNASSIGN': 4,
}

# EMS_EXIST references this source-written signature immediately after its
# PROC. It is initialized DATA in the same original _TEXT SEGDEF, not part of
# the 34-byte instruction extent.
INITIALIZED_DATA = ('emm_device_name', 8, 'libs/master.lib/ems_exist.asm',
                    'EMSEXIST.ASM', 'EMS_EXIST')


def source_data_declaration(raw, encoding, label):
    """Return one complete, source-authored DB declaration outside any PROC."""
    text = raw.decode(encoding).replace('\r\n', '\n').replace('\r', '\n')
    lines = text.splitlines()
    endfunc = [i for i, line in enumerate(lines)
               if line.split(';', 1)[0].strip().lower().startswith('endfunc')]
    matches = []
    for i, line in enumerate(lines):
        body = line.split(';', 1)[0].strip()
        canonical = re.sub(r'\s+', '', body).lower()
        if canonical.startswith(label.lower() + 'db'):
            matches.append((i + 1, canonical))
    need(len(endfunc) == 1 and len(matches) == 1 and matches[0][0] - 1 > endfunc[0],
         'EMS signature must be one separate post-PROC source declaration')
    need(matches[0][1] == "emm_device_namedb'emmxxxx0'",
         'original EMS device signature declaration changed')
    return matches[0]


def omf_text_data_scope(raw, symbol, segment_offset, size):
    """Recover a complete literal range from the actual source-linked CODE LEDATA."""
    records = parse_omf(raw)
    names = ['']
    segments = [None]
    for record in records:
        b = record.data
        if record.name == 'LNAMES':
            pos = 0
            while pos < len(b):
                count = b[pos]; pos += 1
                need(pos + count <= len(b), 'truncated actual OMF LNAMES')
                names.append(b[pos:pos + count].decode('ascii')); pos += count
        elif record.name == 'SEGDEF':
            need(len(b) >= 6 and not b[0] & 2, 'unsupported actual OMF SEGDEF')
            name_index, pos = idx(b, 3)
            class_index, pos = idx(b, pos)
            overlay_index, pos = idx(b, pos)
            need(pos == len(b) and name_index < len(names) and class_index < len(names),
                 'malformed actual OMF SEGDEF names')
            segments.append((names[name_index], names[class_index],
                             int.from_bytes(b[1:3], 'little')))
    text_segments = [i for i, segment in enumerate(segments)
                     if segment and segment[:2] == ('_TEXT', 'CODE')]
    need(len(text_segments) == 1, 'original Master _TEXT CODE segment is not unique')
    segment_index = text_segments[0]

    symbols = []
    for record in records:
        if record.name != 'PUBDEF':
            continue
        b = record.data
        group_index, pos = idx(b, 0)
        si, pos = idx(b, pos)
        if si == 0:
            need(pos + 2 <= len(b), 'truncated absolute PUBDEF frame')
            pos += 2
        while pos < len(b):
            count = b[pos]; pos += 1
            need(pos + count + 2 <= len(b), 'truncated actual OMF PUBDEF symbol')
            name = b[pos:pos + count].decode('ascii'); pos += count
            offset = int.from_bytes(b[pos:pos + 2], 'little'); pos += 2
            type_index, pos = idx(b, pos)
            if name.casefold() == symbol.casefold():
                symbols.append((si, offset))
    need(len(symbols) == 1 and symbols[0][0] == segment_index,
         'EMS_EXIST PUBDEF does not identify the original _TEXT segment')

    content = bytearray(size)
    coverage = bytearray(size)
    ledatas = []
    for record in records:
        if record.name in ('LIDATA', 'LIDATA32'):
            b = record.data
            si, pos = idx(b, 0)
            if si == segment_index:
                raise ValueError('EMS signature unexpectedly comes from iterated data')
        if record.name != 'LEDATA':
            continue
        b = record.data
        si, pos = idx(b, 0)
        need(pos + 2 <= len(b) and si < len(segments), 'malformed actual OMF LEDATA')
        if si != segment_index:
            continue
        offset = int.from_bytes(b[pos:pos + 2], 'little'); pos += 2
        payload = b[pos:]
        low, high = max(offset, segment_offset), min(offset + len(payload), segment_offset + size)
        if low >= high:
            continue
        left, right = low - segment_offset, high - segment_offset
        need(not any(coverage[left:right]), 'overlapping source LEDATA for EMS signature')
        chunk = payload[low - offset:high - offset]
        content[left:right] = chunk
        coverage[left:right] = b'\1' * len(chunk)
        ledatas.append({
            'record_offset': record.offset, 'segment_offset': offset,
            'record_size': len(payload), 'scope_offset': left,
            'scope_size': len(chunk), 'record_sha256': sha(payload),
            'scope_content_sha256': sha(chunk),
        })
    need(all(coverage) and ledatas, 'original EMS signature lacks complete CODE LEDATA')
    return segment_index, segments[segment_index][2], symbols[0][1], bytes(content), ledatas


def private_source_author(old, member):
    """Apply only verified alpha-renames and typed-word aliases to author PROC."""
    text=source_spelling(old)
    if member == 'LARGEPUT_DISP8':
        # The actual TASM port prefixes all *private* names. None of the
        # binary register or arithmetic instructions are modified.
        old_names=('disp8procnear','disp8endp','_ch_equ$-1','_di_equ$-2',
                   'largeput_add_di','largeput_di_','largeput_ch_')
        # Normalize original author-only private labels to the identical
        # downstream-local names used by the full source comparison.
        renamed=[]
        for line in text:
            line=line.replace('disp8procnear','largeput_disp8procnear')
            line=line.replace('disp8endp','largeput_disp8endp')
            line=line.replace('_ch_equ$-1','largeput_ch_equ$-1')
            line=line.replace('_di_equ$-2','largeput_di_equ$-2')
            line=line.replace('add_diequ$-2','largeput_add_diequ$-2')
            renamed.append(line)
        return renamed
    if member == 'SUPERPT8_DISP':
        return [line.replace('dispprocnear','superpt8_dispprocnear')
                    .replace('dispendp','superpt8_dispendp') for line in text]
    if member == 'make_linework':
        for old_piece in ('mov[bx+x],dx','mov[bx+d],ax','mov[bx+dlx],ax',
                          'mov[bx+s],8000h'):
            need(text.count(old_piece)==1,'original linework field missing: '+old_piece)
        return [line.replace('mov[bx+x],dx','mov[bx+make_lin_x],dx')
                    .replace('mov[bx+d],ax','mov[bx+make_lin_d],ax')
                    .replace('mov[bx+dlx],ax','mov[bx+make_lin_dlx],ax')
                    .replace('mov[bx+s],8000h','movwordptr[bx+make_lin_s],8000h')
                for line in text]
    if member in ('FILE_ROPEN','PALETTE_ENTRY_RGB'):
        # Explicit WORD argument types and the original conditional far
        # filename SEG push; they preserve the genuine DOS Pascal ABI.
        filename = 'filename' if member == 'FILE_ROPEN' else 'file_name'
        prefix = 'ss:' if member == 'PALETTE_ENTRY_RGB' else ''
        old_far = '_push'+prefix+'[bx+'+filename+'+2]' if prefix else '_push[bp+filename+2]'
        old_near = 'push'+prefix+'[bx+'+filename+']' if prefix else 'push[bp+filename]'
        new_far = 'pushwordptr'+prefix+'[bx+'+filename+'+2]' if prefix else 'pushwordptr[bp+filename+2]'
        new_near = 'pushwordptr'+prefix+'[bx+'+filename+']' if prefix else 'pushwordptr[bp+filename]'
        need(text.count(old_far)==text.count(old_near)==1,
             'original far file argument stack operands changed: '+member)
        return [word for line in text for word in
                (('ifldata',new_far,'endif') if line==old_far else
                 (new_near,) if line==old_near else (line,))]
    if member == 'GET_MACHINE':
        need(text.count('jeget_machine_98')==text.count('movax,fmr')==1,
             'original near machine detector branch or type changed')
        return [word for line in text for word in
                (('jnzzun1','nop','nop','jmpget_machine_98','zun1:') if line=='jeget_machine_98' else
                 ('movax,fmr_machine',) if line=='movax,fmr' else (line,))]
    if member == 'JS_END':
        # The normalizer already treats TASM NOPCALL and CALL as one true
        # near-call; the real OMF/raw target still checks the relaxation NOP.
        need(text.count('calldos_keyclear')==1,'original JS_END call missing')
        return text
    if member == 'PFCLOSE':
        need(text.count('push[bp+pf]')==1,'original packed file pointer push missing')
        return [line.replace('push[bp+pf]','pushwordptr[bp+pf]') for line in text]
    if member == 'PFGETX1':
        # TH05 intentionally omits the original post-XOR nibble rotation.
        # This is a real *semantic* change, not whitespace or name aliasing.
        need(text.count('roral,4')==1 and text.count('xoral,es:[pf_key]')==1 and
             text.index('roral,4')==text.index('xoral,es:[pf_key]')+1,
             'original archive key nibble rotation context changed')
        return [line for line in text if line!='roral,4']
    if member == 'MEM_UNASSIGN':
        # The native GAME=5 port surrounds exactly the two GAME=1-only heap
        # bounds checks with conditional assembler guards. The bytes linked
        # for GAME=5 remain source-written and independently compared.
        need(text.count('jneshortfailure')==2 and
             text.count('movax,mem_outseg')==1 and text.count('cmpmem_endmark,ax')==1,
             'original Master heap bounds checks differ')
        expanded=[]
        for line in text:
            if line in ('movax,mem_outseg','cmpmem_endmark,ax'):
                expanded.append('ifgameeq1')
            expanded.append(line)
            if line=='jneshortfailure':expanded.append('endif')
        return expanded
    raise ValueError('not an original private Master source procedure')


def source_spelling(raw):
    """Only equivalent Master macro, typed-offset and private-label spellings.

    ReC98's NOPCALL explicitly expresses TLINK's original near-FAR call
    relaxation. The other substitutions name the same I/O ports, fields and
    local branch destinations as the author's original assembler source.
    """
    content = raw.lower().replace('@@', '').replace('nopcall', 'call')
    for before, after in (
        ('rtc_timerorg', 'timerorg'), ('rtc_imr', 'imr'),
        ('vsync_imr', 'imr'),
        ('vsync_leavelabel proc', 'vsync_leavelabel callmodel'),
        ('bfnt_header.col', 'col'),
        ('skipslot11', 'skipslot1'),
    ):
        content = content.replace(before, after)
    lines = [re.sub(r'\s+', '', line.split(';', 1)[0])
             for line in content.splitlines() if line.split(';', 1)[0].strip()]
    return [line.replace('pushwordptr[bp+atrb]', 'push[bp+atrb]')
                .replace('vsync_leavelabelproc', 'vsync_leavelabelcallmodel')
            for line in lines]


def replay():
    parent = json.loads(BASE.read_text())
    frozen = {row['name']: row for row in parent['frozen_source_closure']}
    inventory = {row['name']: row for row in parent['active_procedure_inventory']}
    author_archive = stored_lzh(pinned(ROOT, parent['inputs']['inner_archive']))
    author = {}
    for filename, raw in author_archive.items():
        if not filename.upper().endswith('.ASM'):
            continue
        try:
            blocks = source_blocks(raw, 'cp932')
        except UnicodeDecodeError:
            continue
        for item in blocks:
            author.setdefault(item['name'].casefold(), []).append((filename, item))
    real_obj = pinned(ROOT, parent['inputs']['saved_object'])
    need(real_obj == pinned(ROOT, parent['inputs']['calibration_object']),
         'actual native source object differs from calibration')
    obj = object_text(real_obj)
    cal = parse_mz(pinned(ROOT, parent['inputs']['calibration_exe']))
    native = parse_mz(pinned(ROOT, parent['inputs']['target']))
    before, after = startup(cal), startup(native)
    need((before['dgroup'], after['dgroup'],
          after['init_start']-before['init_start']) == (0x209e0, 0x209d0, -18),
         'original Master native CRT/DGROUP frames not independently anchored')
    rows = []
    source_cache = {}
    for member, start, size in MEMBERS:
        listing = inventory[member]
        need((listing['start'], listing['end']) == (start, start + size),
             'original Master function listing boundary changed: ' + member)
        filename = listing['source']
        need(filename in frozen, 'actual TASM source file missing')
        if filename not in source_cache:
            content = (ROOT / parent['candidate_source_root'] / filename).read_bytes()
            need(sha(content) == frozen[filename]['sha256'],
                 'actual native Master producer source changed')
            source_cache[filename] = (sha(content), source_blocks(content, 'utf8'))
        source_hash, blocks = source_cache[filename]
        same = [b for b in blocks if b['name'] == member]
        need(len(same) == 1, 'whole original procedure absent/ambiguous: ' + member)
        canonical = source_spelling(same[0]['text'])
        if member in PRIVATE_AUTHOR:
            archive_filename, author_name = PRIVATE_AUTHOR[member]
            candidates = [(fn, block) for fn, block in author.get(author_name.casefold(), [])
                          if fn == archive_filename]
            matches = [(fn, block) for fn, block in candidates
                       if private_source_author(block['text'],member) == canonical]
        else:
            matches = [(fn, block) for fn, block in author.get(member.casefold(), [])
                       if source_spelling(block['text']) == canonical]
        need(len(matches) == 1, 'original author source differs from native routine: ' + member)
        original_filename, original_block = matches[0]
        control, linked, unlinked_hash, mz, actions = linked_scope(obj, start, size)
        if member in PRIVATE_OMF_ACTION_COUNTS:
            need(len(actions) == PRIVATE_OMF_ACTION_COUNTS[member],
                 'real original private Master OMF action count changed')
        observed = native.program_image[start:start+size]
        need(control == cal.program_image[start:start+size] and linked == observed,
             'complete original Master code differs from compiled source: ' + member)
        need(relative_fixups(cal, start, size) ==
             relative_fixups(native, start, size) == mz,
             'ordered original MZ relocations differ: ' + member)
        need(native.program_image.find(observed) == start and
             native.program_image.find(observed, start+1) < 0,
             'complete Master CODE extent not uniquely located: ' + member)
        rows.append({
            'member': member, 'start': start, 'end': start + size, 'size': size,
            'candidate_source': filename, 'source_file_sha256': source_hash,
            'original_archive_member': original_filename,
            'original_archive_procedure': PRIVATE_AUTHOR.get(member,(original_filename,member))[1],
            'original_block_sha256': sha(original_block['text'].encode('utf8')),
            'candidate_block_sha256': sha(same[0]['text'].encode('utf8')),
            'canonical_source_sha256': sha('\n'.join(canonical).encode('utf8')),
            'source_unlinked_CODE_sha256': unlinked_hash,
            'calibrated_CODE_sha256': sha(control),
            'original_CODE_sha256': sha(linked),
            'ordered_original_MZ_relocations': mz,
            'ordered_OMF_actions': actions, 'authored_credit': 0,
        })

    # The EMS signature is a separate eight-byte DB declaration after the
    # 34-byte EMS_EXIST PROC. Its own source LEDATA, same-segment PUBDEF,
    # function reference fixup and original/calibration bytes all agree.
    ems = next(row for row in rows if row['member'] == INITIALIZED_DATA[4])
    data_name, data_size, data_source, author_member, ref_symbol = INITIALIZED_DATA
    data_source_path = ROOT / parent['candidate_source_root'] / data_source
    data_source_raw = data_source_path.read_bytes()
    need(sha(data_source_raw) == frozen[data_source]['sha256'] and
         ems['candidate_source'] == data_source and
         ems['source_file_sha256'] == sha(data_source_raw),
         'EMS signature source is not the actual native TASM input')
    author_raw = author_archive[author_member]
    original_line, original_declaration = source_data_declaration(
        author_raw, 'cp932', data_name)
    candidate_line, candidate_declaration = source_data_declaration(
        data_source_raw, 'utf8', data_name)
    need(original_declaration == candidate_declaration,
         'native EMS signature differs from the original Master author declaration')
    segment_index, segment_size, symbol_offset, omf_data, ledatas = \
        omf_text_data_scope(real_obj, ref_symbol, 0x3db0, data_size)
    segment_base = ems['start'] - symbol_offset
    segment_offset = symbol_offset + ems['size']
    data_start = segment_offset + segment_base
    need(symbol_offset == 0x3d8e and segment_size == 0x4376 and
         segment_offset == 0x3db0 and data_start == ems['end'] == 0x4022 and
         omf_data == b'EMMXXXX0' and len(ledatas) == 1 and
         ledatas[0]['scope_offset'] == 0 and ledatas[0]['scope_size'] == data_size,
         'EMS signature original _TEXT/LEDATA boundary changed')
    reference_actions = ems['ordered_OMF_actions']
    need(len(reference_actions) == 1 and
         reference_actions[0]['source_site'] == 20 and
         reference_actions[0]['target_index'] == segment_index and
         reference_actions[0]['original_link_operation'] == 'native-offset16',
         'EMS_EXIST no longer references the source-written signature via its OMF fixup')
    reference_word = data_start.to_bytes(2, 'little')
    need(cal.program_image[ems['start'] + 20:ems['start'] + 22] == reference_word and
         native.program_image[ems['start'] + 20:ems['start'] + 22] == reference_word,
         'original EMS_EXIST offset operand no longer resolves to emm_device_name')
    need(cal.program_image[data_start:data_start + data_size] == omf_data and
         native.program_image[data_start:data_start + data_size] == omf_data and
         native.program_image.find(omf_data) == data_start and
         native.program_image.find(omf_data, data_start + 1) < 0 and
         relative_fixups(cal, data_start, data_size) ==
         relative_fixups(native, data_start, data_size) == [],
         'original/calibration EMS signature bytes or MZ relocation scope differ')
    data_rows = [{
        'member': data_name, 'start': data_start, 'end': data_start + data_size,
        'size': data_size, 'candidate_source': data_source,
        'source_file_sha256': sha(data_source_raw),
        'original_archive_member': author_member,
        'original_source_line': original_line,
        'original_source_declaration': original_declaration,
        'original_source_declaration_sha256': sha(original_declaration.encode('utf8')),
        'candidate_source_line': candidate_line,
        'candidate_source_declaration': candidate_declaration,
        'candidate_source_declaration_sha256': sha(candidate_declaration.encode('utf8')),
        'source_segment': '_TEXT', 'source_segment_class': 'CODE',
        'source_segment_index': segment_index, 'source_segment_size': segment_size,
        'source_segment_offset': segment_offset, 'source_segment_base': segment_base,
        'source_symbol': ref_symbol, 'source_symbol_offset': symbol_offset,
        'reference_OMF_actions': reference_actions,
        'OMF_LEDATAs': ledatas,
        'data_sha256': sha(omf_data),
        'calibrated_data_sha256': sha(cal.program_image[data_start:data_start + data_size]),
        'original_data_sha256': sha(native.program_image[data_start:data_start + data_size]),
        'ordered_original_MZ_relocations': [],
        'authored_credit': 0, 'instruction_bytes': 0,
    }]

    # Native CODE boundaries are always adopted as complete original PROC
    # extents, never absorbing a nearby EVEN byte just because it looks like
    # an alignment NOP. Both positions remain outside all credited scopes.
    for position in UNOWNED_BOUNDARIES:
        need(all(not (r['start'] <= position < r['end']) for r in rows),
             'native Master private PROC swallows unowned alignment byte')
    need(cal.program_image[0x2121] == 0x90 and
         native.program_image[0x2121] == 0x00 and
         native.program_image[0x41b1] == 0x00,
         'original Master private PROC post-RET boundary changed')
    return {
        'schema_version': 1, 'kind': 'original-master-gap-functions-and-literal-data-source-and-MZ',
        'artifact': 'th05-main', 'members': rows,
        'CODE_bytes': sum(n for _, _, n in MEMBERS),
        'initialized_data_members': data_rows, 'initialized_DATA_bytes': data_size,
        'original_target_sha256': parent['inputs']['target']['sha256'],
        'source_OMF_sha256': parent['inputs']['saved_object']['sha256'],
        'calibration_exe_sha256': parent['inputs']['calibration_exe']['sha256'],
        'author_archive_sha256': parent['inputs']['inner_archive']['sha256'],
        'parent_master_sha256': digest_file(BASE),
        'verifier_sha256': digest_file(ROOT / 'scripts/review_master_gap_functions.py'),
        'authored_credit': 0, 'other_bytes_claimed': 0,
        'unowned_boundary_offsets': list(UNOWNED_BOUNDARIES),
    }


def validate_public(proof):
    parent = json.loads(BASE.read_text())
    need(proof.get('schema_version') == 1 and
         proof.get('kind') == 'original-master-gap-functions-and-literal-data-source-and-MZ' and
         proof.get('artifact') == 'th05-main' and
         proof.get('CODE_bytes') == sum(n for _, _, n in MEMBERS) and
         proof.get('initialized_DATA_bytes') == INITIALIZED_DATA[1] and
         proof.get('authored_credit') == proof.get('other_bytes_claimed') == 0 and
         proof.get('unowned_boundary_offsets') == list(UNOWNED_BOUNDARIES) and
         proof.get('original_target_sha256') == parent['inputs']['target']['sha256'] and
         proof.get('source_OMF_sha256') == parent['inputs']['saved_object']['sha256'] and
         proof.get('calibration_exe_sha256') == parent['inputs']['calibration_exe']['sha256'] and
         proof.get('author_archive_sha256') == parent['inputs']['inner_archive']['sha256'] and
         proof.get('parent_master_sha256') == digest_file(BASE) and
         proof.get('verifier_sha256') == digest_file(ROOT / 'scripts/review_master_gap_functions.py'),
         'Master source/binary provenance changed')
    rows = proof.get('members', [])
    need([(r.get('member'), r.get('start'), r.get('size')) for r in rows] == list(MEMBERS),
         'complete Master source function list changed')
    for row in rows:
        if row['member'] in PRIVATE_OMF_ACTION_COUNTS:
            need(len(row.get('ordered_OMF_actions',[])) ==
                 PRIVATE_OMF_ACTION_COUNTS[row['member']],
                 'original private Master helper OMF actions missing')
        need(row.get('end') == row['start'] + row['size'] and
             row.get('original_archive_procedure') ==
             PRIVATE_AUTHOR.get(row['member'],(None,row['member']))[1] and
             (row['member'] not in PRIVATE_AUTHOR or
              row['original_archive_member'] == PRIVATE_AUTHOR[row['member']][0]) and
             row.get('authored_credit') == 0 and
             isinstance(row.get('ordered_OMF_actions'), list) and
             row.get('ordered_original_MZ_relocations') ==
             [f['source_site'] for f in row['ordered_OMF_actions']
              if f['original_link_operation'] == 'original-MZ-segment16'],
             'incomplete CODE extent or ordered relocation record')
        for field in ('source_file_sha256', 'original_block_sha256',
                      'candidate_block_sha256', 'canonical_source_sha256',
                      'source_unlinked_CODE_sha256', 'calibrated_CODE_sha256',
                      'original_CODE_sha256'):
            need(isinstance(row.get(field), str) and re.fullmatch('[0-9a-f]{64}', row[field]),
                 'original Master source/CODE evidence missing')
    data_rows = proof.get('initialized_data_members', [])
    need(len(data_rows) == 1, 'the original EMS device signature DATA scope is missing')
    data = data_rows[0]
    ems = next(row for row in rows if row['member'] == 'EMS_EXIST')
    need((data.get('member'), data.get('start'), data.get('end'), data.get('size')) ==
         ('emm_device_name', 0x4022, 0x402a, 8) and
         data.get('candidate_source') == INITIALIZED_DATA[2] and
         data.get('original_archive_member') == INITIALIZED_DATA[3] and
         data.get('source_segment') == '_TEXT' and
         data.get('source_segment_class') == 'CODE' and
         data.get('source_segment_offset') == 0x3db0 and
         data.get('source_segment_base') == 0x272 and
         data.get('source_symbol') == 'EMS_EXIST' and
         data.get('source_symbol_offset') == 0x3d8e and
         data.get('source_segment_offset') + data.get('source_segment_base') == data.get('start') and
         data.get('start') == ems['end'] and
         data.get('reference_OMF_actions') == ems['ordered_OMF_actions'] and
         len(data.get('reference_OMF_actions', [])) == 1 and
         data['reference_OMF_actions'][0]['source_site'] == 20 and
         data['reference_OMF_actions'][0]['target_index'] == data['source_segment_index'] and
         len(data.get('OMF_LEDATAs', [])) == 1 and
         data['OMF_LEDATAs'][0]['scope_offset'] == 0 and
         data['OMF_LEDATAs'][0]['scope_size'] == 8 and
         data['OMF_LEDATAs'][0]['scope_content_sha256'] == data.get('data_sha256') and
         data.get('data_sha256') == data.get('calibrated_data_sha256') ==
         data.get('original_data_sha256') == sha(b'EMMXXXX0') and
         data.get('ordered_original_MZ_relocations') == [] and
         data.get('authored_credit') == data.get('instruction_bytes') == 0,
         'original EMS initialized DATA source/OMF/MZ ownership evidence is incomplete')
    for field in ('source_file_sha256', 'original_source_declaration_sha256',
                  'candidate_source_declaration_sha256', 'data_sha256',
                  'calibrated_data_sha256', 'original_data_sha256'):
        need(isinstance(data.get(field), str) and re.fullmatch('[0-9a-f]{64}', data[field]),
             'original EMS initialized DATA digest missing')
    if DECISION.exists():
        adopted = json.loads(DECISION.read_text())
        need(adopted.get('schema_version') == 1 and adopted.get('artifact') == 'th05-main' and
             adopted.get('decision') == 'ADOPT_ONLY_COMPLETE_ORIGINAL_MASTER_GAP_FUNCTIONS_AND_LITERAL_DATA' and
             adopted.get('evidence_sha256') == digest_file(PROOF) and
             adopted.get('members') == [name for name, _, _ in MEMBERS] and
             adopted.get('CODE_bytes') == proof['CODE_bytes'] and
             adopted.get('initialized_DATA_bytes') == proof['initialized_DATA_bytes'] and
             adopted.get('initialized_data_members') == [data['member']] and
             adopted.get('authored_credit') == adopted.get('other_bytes_claimed') == 0,
             'original Master source decision missing or stale')


def reviewed_claims(root, view, *, verify_targets=False):
    if not DECISION.exists():
        return [], None
    need(root.resolve() == ROOT.resolve(), 'wrong reconstruction checkout')
    proof = json.loads(PROOF.read_text())
    validate_public(proof)
    need(view['sha256'] == json.loads(BASE.read_text())['target_payload_sha256'],
         'Master native source target identity changed')
    if verify_targets:
        need(replay() == proof, 'native original Master complete CODE no longer matches')
    claims = [{'start': row['start'], 'end': row['end'], 'kind': 'verified-vendor-code',
               'library': 'master.lib 0.23', 'member': row['member'], 'authored_credit': 0}
              for row in proof['members']]
    claims.extend({'start': row['start'], 'end': row['end'],
                   'kind': 'verified-vendor-initialized-data',
                   'content_kind': 'library-initialized-data', 'instruction_bytes': 0,
                   'library': 'master.lib 0.23', 'member': row['member'],
                   'authored_credit': 0}
                  for row in proof['initialized_data_members'])
    return claims, digest_file(DECISION)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    group.add_argument('--structural-check', action='store_true')
    args = parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'cannot overwrite accepted Master evidence')
        proof = replay()
        PROOF.write_text(json.dumps(proof, indent=2) + '\n')
        print('PASS original source-backed Master CODE/DATA', proof['CODE_bytes'], proof['initialized_DATA_bytes'])
    else:
        proof = json.loads(PROOF.read_text())
        validate_public(proof)
        if args.check:
            need(replay() == proof, 'original native Master byte comparison changed')
            print('PASS Master original gap functions and EMS signature: complete CODE/DATA and fixups')
        else:
            print('PASS Master gap functions and EMS signature public evidence')


if __name__ == '__main__':
    main()
