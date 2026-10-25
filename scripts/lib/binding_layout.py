"""Opt-in symbol-only OMF bindings on both sides of one genuine compiler TU.

Existing producers keep their original one-object linker layout. This profile
lets TLINK see a genuine common public segment without changing a far API.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from .omf import parse_omf
from .replay_toolchain import bindings_source

ALLOWED = {'THEADR', 'COMENT', 'LNAMES', 'SEGDEF', 'GRPDEF', 'PUBDEF', 'MODEND'}
SEMANTIC = ALLOWED - {'THEADR', 'COMENT'}


def after_compiler(entry: dict) -> bool:
    value = entry.get('bindings_after_compiler', False)
    if type(value) is not bool:
        raise ValueError('bindings_after_compiler must be an explicit boolean')
    return value


def sha(data):
    return hashlib.sha256(data).hexdigest()


def link_response(obj: str) -> bytes:
    return f'-c -s -E bindings.obj {obj} bindings_after.obj, units.exe, units.map,\r\n'.encode('ascii')


def symbol_only(raw: bytes) -> dict:
    records = parse_omf(raw)
    if any(record.name not in ALLOWED for record in records):
        raise ValueError('before/after binding objects must contain symbols only, without initialized bytes or fixups')
    for record in records:
        if record.name == 'COMENT':
            # Only the observed TASM translator/dependency/debug metadata forms.
            # Other COMENT classes can carry linker directives and fail closed.
            data = record.data
            metadata = (
                len(data) >= 3 and data[:2] == b'\0\0' and data[2] == len(data)-3 or
                data[:2] == b'\x40\xe9' and (len(data) == 2 or
                    len(data) >= 7 and data[6] == len(data)-7) or
                data in (b'\x40\xa1', b'\x40\xa2\x01'))
            if not metadata:
                raise ValueError('unreviewed binding COMENT may carry linker semantics')
        if record.name == 'SEGDEF' and (len(record.data) < 6 or
                record.data[0] >> 5 not in (1, 2, 3) or record.data[0] & 3):
            raise ValueError('before/after bindings require ordinary relocatable 16-bit segments')
    ends = [record for record in records if record.name == 'MODEND']
    if len(ends) != 1 or ends[0].data != b'\0':
        raise ValueError('symbol-only binding must not provide a synthetic program entry')
    model = b''.join(raw[r.offset:r.offset+3+r.length] for r in records if r.name in SEMANTIC)
    return {'sha256': sha(raw), 'symbol_model_sha256': sha(model)}


def observe(source: Path, entry: dict) -> dict:
    if not after_compiler(entry):
        raise ValueError('before/after evidence requires its explicit unit profile')
    args = json.loads((source / 'compiler-arguments.json').read_text())
    if list(args) != [entry['module']]:
        raise ValueError('before/after binding profile requires one real compiler translation unit')
    obj = Path(entry['module']).stem + '.obj'
    response = (source / 'link.rsp').read_bytes()
    if response != link_response(obj):
        raise ValueError('before/after binding linker order or flags differ')
    raw = (source / 'bindings.asm').read_bytes()
    if raw != (source / bindings_source(entry)).read_bytes():
        raise ValueError('both assembler views must use the canonical frozen binding source')
    return dict(kind='symbol-only-before-and-after-compiler', source_sha256=sha(raw),
                compiler_object=obj, link_response_sha256=sha(response),
                before=symbol_only((source / 'bindings.obj').read_bytes()),
                after=symbol_only((source / 'bindings_after.obj').read_bytes()))


def validate_evidence(entry: dict, evidence: dict) -> None:
    expected = dict(kind='symbol-only-before-and-after-compiler',
                    compiler_object=Path(entry['module']).stem+'.obj')
    if not isinstance(evidence, dict) or any(evidence.get(k) != v for k, v in expected.items()):
        raise ValueError('before/after binding evidence belongs to another compiler layout')
    if evidence.get('link_response_sha256') != sha(link_response(expected['compiler_object'])):
        raise ValueError('before/after binding response identity differs')
    hashes = [evidence.get('source_sha256')]
    for side in ('before', 'after'):
        data = evidence.get(side, {})
        if not isinstance(data, dict) or set(data) != {'sha256', 'symbol_model_sha256'}:
            raise ValueError('before/after binding OMF identity missing')
        hashes.extend(data.values())
    if any(not isinstance(h, str) or len(h) != 64 or any(c not in '0123456789abcdef' for c in h) for h in hashes):
        raise ValueError('before/after binding digest malformed')


def validate_result(entry: dict, result: dict) -> None:
    if not after_compiler(entry):
        if 'binding_context' in result:
            raise ValueError('before/after evidence cannot relabel a legacy linker layout')
        return
    contexts = result.get('binding_context')
    if not isinstance(contexts, list) or len(contexts) != 2:
        raise ValueError('two independent before/after binding producers are required')
    for evidence in contexts:
        validate_evidence(entry, evidence)
    if any(contexts[0][key] != contexts[1][key] for key in
           ('source_sha256', 'compiler_object', 'link_response_sha256')) or any(
            contexts[0][side]['symbol_model_sha256'] != contexts[1][side]['symbol_model_sha256']
            for side in ('before', 'after')):
        raise ValueError('before/after binding symbols, segments or linker order are nondeterministic')
    inputs = {item['path']: item['sha256'] for item in result.get('source_inputs', [])}
    if inputs.get(bindings_source(entry)) != contexts[0]['source_sha256']:
        raise ValueError('before/after binding source differs from the actual source closure')


def validate_control(entry: dict, positive: dict, negative: dict) -> None:
    """The CPP mutation must retain the positive binding and linker model."""
    validate_evidence(entry, negative)
    if any(positive[key] != negative[key] for key in
           ('source_sha256', 'compiler_object', 'link_response_sha256')) or any(
            positive[side]['symbol_model_sha256'] != negative[side]['symbol_model_sha256']
            for side in ('before', 'after')):
        raise ValueError('negative control changed the positive binding or linker model')
