"""COM units keep original container coordinates and real tiny CRT linkage."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lib import tiny_com as uc
from lib.launcher import parse_launcher
from lib.tiny_com import compare_mapped_unit
from replay_units import mapped_control_comparison
from test_launcher import synthetic_launcher


class TinyCOMTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def target_fixture(self):
        context = uc.UnitContext(self.root, 'zun')
        context.cache.mkdir(parents=True, exist_ok=True)
        raw, _ = synthetic_launcher()
        member = parse_launcher(raw)['payloads'][0]
        relocations = b'[]\n'
        receipt = dict(artifact=context.artifact, target_sha256=uc.sha(raw), target_size=len(raw),
            method='plain-com-container', checks={'plain_com': True}, address_bias=256, entry_ip=256,
            payload_sha256=uc.sha(raw), payload_size=len(raw), relocation_count=0,
            relocations_sha256=uc.sha(relocations))
        receipt_bytes = json.dumps(receipt).encode()
        for name, data in [('receipt.json', receipt_bytes), ('payload.bin', raw), ('relocations.json', relocations)]:
            (context.cache / name).write_bytes(data)
        proof = dict(artifact=context.artifact, kind='embedded-plain-com-source-view',
            packed_target_sha256=uc.sha(raw), receipt_sha256=uc.sha(receipt_bytes),
            payload_sha256=uc.sha(raw), payload_size=len(raw), relocations_sha256=uc.sha(relocations),
            relocation_count=0, member=member['name'], member_start=member['file_start'],
            member_end=member['file_end'], member_sha256=member['sha256'], child_address_bias=256)
        config = dict(artifact=context.artifact, units=[dict(target_start=member['file_start'], size=4)],
            target_view={key: proof[key] for key in ('receipt_sha256', 'member', 'member_start', 'member_end', 'member_sha256')})
        config['target_view']['proof_sha256'] = uc.proof_sha256(proof)
        return context, config, dict(id=context.artifact, sha256=uc.sha(raw)), raw, proof

    def load(self, fixture):
        context, config, artifact, raw, _ = fixture
        with patch.object(uc, 'load_target_manifest', return_value={'artifacts': [artifact]}), \
             patch.object(uc, 'read_verified_artifact', return_value=raw):
            return uc.load_unit_target(context, config)

    def test_full_container_stays_unmodified_and_member_is_only_a_boundary(self):
        fixture = self.target_fixture()
        _, image, proof = self.load(fixture)
        self.assertEqual(image.program_image, fixture[3])
        self.assertFalse(hasattr(image, "address_bias"))
        self.assertEqual(image.relocations, ())
        self.assertEqual(proof, fixture[4])
        self.assertFalse(hasattr(image, 'header'))

    def test_child_metadata_and_unit_escape_are_rejected(self):
        for field, value in [('member', '-B'), ('member_start', 0), ('member_sha256', '0' * 64)]:
            fixture = self.target_fixture()
            fixture[1]['target_view'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.load(fixture)
        fixture = self.target_fixture()
        fixture[1]['units'][0]['size'] = len(fixture[3])
        with self.assertRaisesRegex(ValueError, 'leaves'):
            self.load(fixture)

    def test_plain_com_receipt_cannot_hide_decoding_or_relocations(self):
        for field, value in [('method', 'target-owned-diet-decoder'), ('address_bias', 0), ('relocation_count', 1)]:
            fixture = self.target_fixture()
            path = fixture[0].cache / 'receipt.json'
            receipt = json.loads(path.read_bytes()); receipt[field] = value
            path.write_text(json.dumps(receipt))
            fixture[1]['target_view']['receipt_sha256'] = uc.sha(path.read_bytes())
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'plain COM'):
                self.load(fixture)

    def candidate_fixture(self):
        source = self.root / 'source'; source.mkdir(exist_ok=True)
        (source / 'c0t.obj').write_bytes(b'synthetic CRT identity')
        (source / 'compiler-arguments.json').write_text(json.dumps({'th05/a.cpp': uc.compiler_arguments({'module': 'th05/a.cpp'}, None)}))
        (source / 'link.rsp').write_bytes(b'-c -s -t c0t.obj a.obj bindings.obj, units.com, units.map,\r\n')
        (source / 'units.map').write_text(
            ' 0000:0000 0367 C=CODE S=_TEXT G=DGROUP M=c0.ASM ACBP=28\n'
            ' 0000:0367 0004 C=CODE S=_TEXT G=DGROUP M=th05/a.cpp ACBP=28\n'
            ' 0000:1650 006E C=DATA S=_DATA G=DGROUP M=c0.ASM ACBP=68\n')
        (source / 'units.com').write_bytes(bytes(0x267) + b'ABCD' + bytes(32))
        return source

    def candidate(self, source):
        with patch.object(uc, 'TINY_CRT_SHA256', uc.sha(b'synthetic CRT identity')):
            return uc.load_unit_candidate(source, None)

    def test_map_runtime_coordinates_are_converted_once_without_prefix_bytes(self):
        source = self.candidate_fixture()
        candidate = self.candidate(source)
        self.assertEqual(candidate.program_image, (source / 'units.com').read_bytes())
        target = uc.DecodedUnitImage(b'--ABCD--', ())
        entry = dict(id='u', module='th05/a.cpp', segment='_TEXT', target_start=2, size=4)
        result = compare_mapped_unit(target, candidate, source / 'units.map', entry)
        self.assertTrue(result['exact'])
        self.assertEqual(result['candidate_start'], 0x267)
        self.assertEqual(result['map_scope']['start'], 0x367)
        self.assertEqual(result['candidate_address_bias'], 256)
        (source / 'units.com').write_bytes(bytes(0x267) + b'ABXD' + bytes(32))
        negative = mapped_control_comparison(target, self.candidate(source), entry, source / 'units.map')
        self.assertFalse(negative['raw_exact'])
        self.assertEqual(negative['candidate_start'], 0x267)

    def test_startup_link_order_group_and_output_format_are_enforced(self):
        for name, before, after in [
            ('c0t.obj', b'synthetic CRT identity', b'foreign CRT'),
            ('link.rsp', b'c0t.obj a.obj bindings.obj', b'bindings.obj c0t.obj a.obj'),
            ('link.rsp', b'-t ', b'-E '),
            ('units.map', b'G=DGROUP', b'G=FOREIGN'),
            ('units.map', b'0000:1650', b'0001:1650'),
            ('units.map', b'006E C=DATA', b'006D C=DATA'),
            ('units.com', bytes(2), b'MZ'),
        ]:
            source = self.candidate_fixture()
            path = source / name
            path.write_bytes(path.read_bytes().replace(before, after, 1))
            with self.subTest(file=name, mutation=after), self.assertRaises(ValueError):
                self.candidate(source)

    def test_tiny_context_has_own_flags_and_disallows_binary_override(self):
        context = uc.UnitContext(self.root, 'zun')
        argv = uc.compiler_arguments({'module': 'th05/a.cpp'}, context.binary)
        self.assertIn('-mt', argv)
        self.assertFalse(any(x.startswith('-DBINARY=') for x in argv))
        with self.assertRaises(ValueError):
            uc.compiler_arguments({'module': 'th05/a.cpp', 'binary': 'M'}, context.binary)
        self.assertNotEqual(context.ledger, uc.UnitContext(self.root).ledger)


if __name__ == '__main__':
    unittest.main()
