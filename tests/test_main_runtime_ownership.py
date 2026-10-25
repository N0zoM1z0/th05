"""Native CL runtime review cannot turn relocation matches into authored credit."""
import copy
import json
from pathlib import Path
import struct
import shutil
import tempfile
import sys
import unittest
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import review_main_runtime as review


class RuntimeOwnershipTests(unittest.TestCase):
    def proof(self):
        return json.loads((ROOT / review.PROOF).read_text())

    def test_current_proposal_is_complete_zero_credit_and_needs_no_private_bytes(self):
        result = review.validate_metadata(self.proof())
        self.assertEqual((result['contribution_count'], result['bytes']), (24, 18129))
        self.assertEqual(result['authored_credit'], 0)
        self.assertIsNone(result['authored_denominator'])
        self.assertFalse(result['byte_proof_replayed'])

    def test_every_real_far_call_relaxation_nop_has_checked_zero_credit_padding_role(self):
        proof = self.proof()
        rows = []
        for row in proof['contributions']:
            offsets = [a['write_start'] for a in row['native']['fixup_actions']
                       if a['operation'] == 'TLINK same-segment far-call NOP/PUSHCS/CALL']
            if offsets:
                rows.append(dict(member=row['member'], start=row['native']['start'],
                                 offsets_in_original_record_order=offsets))
        roles = json.loads((ROOT / 'config/main_runtime_padding.json').read_text())
        self.assertEqual(roles, dict(schema_version=1, kind='checked-vendor-padding-roles',
            owner='third-party-runtime', role='checked-padding',
            reason='TLINK same-segment far-call relaxation', authored_credit=0,
            evidence_sha256=review.sha((ROOT / review.PROOF).read_bytes()), bytes=116, members=rows))
        self.assertEqual(sum(len(r['offsets_in_original_record_order']) for r in rows), 116)
        self.assertTrue(all(0 <= off < review.SCOPES[row['member']][1]
                            for row in rows for off in row['offsets_in_original_record_order']))

    def test_credit_provenance_and_fixed_input_pins_cannot_be_relabelled(self):
        for key, value in [('authored_credit', 1), ('authored_credit', False),
                           ('compiler_invocations', 2), ('artifact', 'th05-op'),
                           ('authored_denominator', 18129), ('decision', 'ACCEPTED')]:
            meta = self.proof(); meta[key] = value
            with self.subTest(field=key, value=value), self.assertRaises(ValueError):
                review.validate_metadata(meta)
        meta = self.proof(); meta['inputs']['library_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'pin drift'):
            review.validate_metadata(meta)

    def test_only_the_whole_reviewed_unique_members_are_eligible(self):
        for mutate in (lambda rows: rows.pop(), lambda rows: rows.append(copy.deepcopy(rows[0])),
                       lambda rows: rows[0].update(member='farheap')):
            meta = self.proof(); mutate(meta['contributions'])
            with self.assertRaises(ValueError):
                review.validate_metadata(meta)
        for key in ('start', 'end', 'size'):
            meta = self.proof()
            for side in ('calibration', 'native'):
                meta['contributions'][0][side][key] += 1
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, 'boundary'):
                review.validate_metadata(meta)

    def test_frame_data_bss_and_anchor_members_are_separate_invariants(self):
        for key, value in [('data_offset_change', -20), ('bss_offset_change', -18),
                           ('data_calibration_start', 0), ('bss_calibration_end', 65536)]:
            meta = self.proof(); meta['binding_model'][key] = value
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, 'binding model'):
                review.validate_metadata(meta)
        for mutate in (lambda m: m['native'].update(dgroup=0x209e0),
                       lambda m: m['native'].update(initial_ss=0x209d),
                       lambda m: m['data_anchor_ids'].pop(),
                       lambda m: m['bss_suffix'][0].update(size=126)):
            meta = self.proof(); mutate(meta['binding_model'])
            with self.assertRaisesRegex(ValueError, 'binding model'):
                review.validate_metadata(meta)

    def test_fixup_binding_or_linker_transformation_cannot_be_inferred_per_operand(self):
        for key in ('resolved_target_offset', 'resolved_target_frame', 'resolved_frame'):
            meta = self.proof()
            row = next(r for r in meta['contributions'] if r['member'] == 'xx')
            row['native']['fixup_actions'][0][key] += 1
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, 'binding model'):
                review.validate_metadata(meta)
        meta = self.proof()
        row = next(r for r in meta['contributions'] if r['member'] == 'xx')
        row['native']['fixup_actions'][0]['operation'] = 'mask-target-operand'
        with self.assertRaisesRegex(ValueError, 'transformation'):
            review.validate_metadata(meta)

    def test_actual_order_and_full_ledatas_cannot_be_sorted_clipped_or_padded(self):
        meta = self.proof()
        row = next(r for r in meta['contributions'] if r['member'] == 'xx')
        row['native']['ordered_MZ_fixups'].sort()
        with self.assertRaisesRegex(ValueError, 'relocation identity'):
            review.validate_metadata(meta)
        for mutate in (lambda p: p['CODE_LEDATA'][0].update(offset=1),
                       lambda p: p['CODE_LEDATA'][0].update(size=0),
                       lambda p: p.update(complete_gapless_CODE_LEDATA=False)):
            meta = self.proof()
            for side in ('calibration', 'native'):
                mutate(meta['contributions'][0][side])
            with self.assertRaises(ValueError):
                review.validate_metadata(meta)

    def test_fixup_writes_and_byte_identities_remain_bounded(self):
        for mutate in (lambda a: a.update(write_start=20000),
                       lambda a: a.update(write_size=3)):
            meta = self.proof()
            row = next(r for r in meta['contributions'] if r['member'] == 'xx')
            for side in ('calibration', 'native'):
                mutate(row[side]['fixup_actions'][0])
            with self.assertRaisesRegex(ValueError, 'FIXUPP writes'):
                review.validate_metadata(meta)
        meta = self.proof(); meta['contributions'][0]['native']['linked_CODE_sha256'] = 'not a digest'
        with self.assertRaisesRegex(ValueError, 'digest malformed'):
            review.validate_metadata(meta)

    def test_translation_changes_only_reviewed_dgroup_bindings_and_keeps_stack(self):
        old = 0x209e0
        original = SimpleNamespace(groups={'dgroup': old},
            contribs=[dict(group='DGROUP', segment='_DATA', start=old+0x2564, frame=old),
                      dict(group='(none)', segment='_STACK', start=0x2d130, frame=0x2d130)],
            segbases={'_data': old, '_stack': 0x2d130},
            pubmap={'data': {(old, 0x2564)}, 'code': {(0, 0x7077)}, 'stack': {(0x2d130, 0)}},
            rawpub={'data': [(old, 0x2564, 'xx')], 'code': [(0, 0x7077, 'xx')]},
            mods={'xx': {'program_records': b'unmodified distributed object'}}, cal='actual control', target='actual control')
        native = review.translate_review(original, 'actual target', review.expected_model())
        self.assertEqual(native.segbases['_stack'], 0x2d130)
        self.assertEqual(native.contribs[1], original.contribs[1])
        self.assertEqual(native.pubmap['code'], original.pubmap['code'])
        self.assertEqual(native.pubmap['data'], {(0x209d0, 0x2552)})
        self.assertEqual(native.mods, original.mods)
        self.assertEqual(original.pubmap['data'], {(old, 0x2564)})
        self.assertEqual(original.cal, 'actual control')

    def adoption_fixture(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for name in review.SOURCES + [review.PROOF]:
            destination = root / name; destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)
        decision = dict(schema_version=1, decision='ADOPT_ONLY_LISTED_MEMBERS',
            classification='third-party-library-code', artifact='th05-main',
            evidence_sha256=review.sha((root / review.PROOF).read_bytes()), members=list(review.SCOPES),
            authored_credit=0, authored_denominator=None, other_scopes_policy='unknown',
            notes='docs/reconstruction/MAIN_RUNTIME_OWNERSHIP.md')
        (root / review.DECISION).write_text(json.dumps(decision))
        views = {'main': dict(size=145958, sha256=review.legacy.PINS['target_payload_sha256'])}
        return root, decision, views

    def test_explicit_adoption_covers_only_all_listed_complete_vendor_members(self):
        root, _, views = self.adoption_fixture()
        claims, _ = review.reviewed_claims(root, views)
        self.assertEqual(len(claims), 24)
        self.assertEqual(sum(row['end']-row['start'] for row in claims), 18129)
        self.assertTrue(all(row['kind'] == 'verified-vendor-code' for row in claims))
        (root / review.DECISION).unlink()
        self.assertEqual(review.reviewed_claims(root, views), ([], None))

    def test_adoption_rejects_unknown_members_wrong_view_stale_proof_and_credit(self):
        for key, value in [('members', ['xx', 'farheap']), ('members', []),
                           ('classification', 'authored-cxx-code'), ('authored_credit', False),
                           ('authored_credit', 18129), ('schema_version', True),
                           ('other_scopes_policy', 'exclude-all-runtime'), ('evidence_sha256', '0'*64)]:
            root, decision, views = self.adoption_fixture(); decision[key] = value
            (root / review.DECISION).write_text(json.dumps(decision))
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, 'adoption'):
                review.reviewed_claims(root, views)
        root, _, views = self.adoption_fixture(); views['main']['size'] += 1
        with self.assertRaisesRegex(ValueError, 'coordinate'):
            review.reviewed_claims(root, views)

    def crt_object(self, targets=None):
        from test_initialized_data_replay import record
        names = ['_TEXT', 'CODE', '_BSS', '_BSSEND', '_INIT_', '_INITEND_', '_EXIT_', '_EXITEND_', 'DGROUP', 'BSS']
        raw = record(0x80, b'\x03crt')
        raw += record(0x96, b''.join(bytes([len(n)]) + n.encode() for n in names))
        for number, name in enumerate((1, 3, 4, 5, 6, 7, 8), 1):
            size = 0x200 if number == 1 else 0
            raw += record(0x98, bytes([0x28]) + struct.pack('<H', size) + bytes([name, 2, 0]))
        raw += record(0x9a, bytes([9, 255, 2, 255, 3, 255, 4, 255, 5, 255, 6, 255, 7]))
        raw += record(0xa0, b'\x01\x00\x00' + bytes(0x200))
        targets = targets if targets is not None else [(0xb6, 2), (0xb9, 3), (0x11f, 4), (0x122, 5), (0x14e, 6), (0x151, 7)]
        fixups = b''.join(bytes([0xc4 | (site >> 8), site & 255, 0x14, 1, segment]) for site, segment in targets)
        return raw + record(0x9c, fixups) + record(0x8a, b'\x00')

    def test_crt_omf_requires_real_segment_roles_and_all_six_boundaries(self):
        roles = review.crt_roles(self.crt_object())
        self.assertEqual(roles, self.proof()['crt_segment_roles'])
        correct = [(0xb6, 2), (0xb9, 3), (0x11f, 4), (0x122, 5), (0x14e, 6), (0x151, 7)]
        for targets in (correct[:-1], correct + [correct[0]],
                        [(0xb6, 2), (0xb9, 2)] + correct[2:],
                        [(0xb7, 2)] + correct[1:]):
            with self.assertRaisesRegex(ValueError, 'CRT'):
                review.crt_roles(self.crt_object(targets))

    def startup(self, *, native=True):
        values = review.expected_model()['native' if native else 'calibration']
        body = bytearray(0x200)
        body[0] = 0xba; body[0x14:0x16] = b'\x8e\xda'
        body[0x5d] = 0xbf; body[0xa4] = 0xb8
        for off in (1, 0x5e, 0xa5):
            struct.pack_into('<H', body, off, values['dgroup'] // 16)
        body[0xb0:0xb6] = b'\x2e\x8e\x06\x6d\x02\xbf'
        body[0xb8] = 0xb9; body[0xbb:0xc0] = b'\x2b\xcf\xfc\xf3\xaa'
        for off, key in ((0xb6, 'bss_start'), (0xb9, 'bss_end'), (0x11f, 'init_start'),
                         (0x122, 'init_end'), (0x14e, 'exit_start'), (0x151, 'exit_end')):
            struct.pack_into('<H', body, off, values[key])
        body[0x11e] = body[0x14d] = 0xbe
        body[0x121] = body[0x150] = 0xbf
        return SimpleNamespace(valid=True, program_image=bytes(body),
            header=SimpleNamespace(initial_relative_cs=0, initial_ip=0, initial_relative_ss=values['initial_ss']),
            relocations=[SimpleNamespace(linear=off) for off in (1, 0x5e, 0xa5)])

    def test_startup_reads_real_ds_and_bss_roles_without_equating_ss(self):
        image = self.startup()
        model = review.startup(image)
        self.assertEqual(model, review.expected_model()['native'])
        self.assertNotEqual(model['initial_ss'], model['dgroup'] // 16)
        self.assertEqual(review.startup(self.startup(native=False)), review.expected_model()['calibration'])

    def test_startup_role_opcode_topology_and_actual_relocations_are_mandatory(self):
        for offset in (0, 0x14, 0x5e, 0xb0, 0xb6, 0xb8, 0xbd, 0x11e, 0x151):
            image = self.startup(); body = bytearray(image.program_image); body[offset] ^= 1
            image.program_image = bytes(body)
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                review.startup(image)
        image = self.startup(); image.relocations.pop()
        with self.assertRaisesRegex(ValueError, 'MZ relocations'):
            review.startup(image)


if __name__ == '__main__':
    unittest.main()
