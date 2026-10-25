"""Artifact-specific vendor proposals; no private targets or DOS tools needed."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import review_vendor_context as vc
import ownership
from lib.pc98 import digest_bytes
from lib.unit_context import proof_sha256
from lib.unit_oracle import relative_fixups
import test_unit_context as fixtures


def metadata(name):
    return json.loads(vc.metadata_path(ROOT, name).read_text())


class ContextMetadataTests(unittest.TestCase):
    def test_both_public_proposals_validate_without_private_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in vc.REVIEWER_SOURCES + ["config/toolchain.toml"]:
                destination = root / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, destination)
            self.assertFalse((root / ".analysis").exists())
            for name, count, size in [("op", 63, 23708), ("maine", 55, 20870)]:
                result = vc.validate_metadata(metadata(name), root=root, context=name)
                self.assertEqual((result["contributions"], result["proposed_bytes"]), (count, size))
                self.assertFalse(result["byte_proof_replayed"])
            (root / "scripts/lib/unit_context.py").write_text("changed decoded loader\n")
            with self.assertRaisesRegex(ValueError, "source drift"):
                vc.validate_metadata(metadata("op"), root=root, context="op")

    def test_wrong_artifact_context_and_calibration_identity_reject(self):
        for key, value in [("artifact", "th05-maine"), ("context", "maine")]:
            bad = metadata("op"); bad[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                vc.validate_metadata(bad, context="op")
        bad = metadata("op")
        bad["calibration"] = metadata("maine")["calibration"]
        with self.assertRaisesRegex(ValueError, "calibration"):
            vc.validate_metadata(bad, context="op")

    def test_gap_overlap_and_original_order_cannot_be_normalized(self):
        for mode in ("gap", "overlap", "order"):
            bad = metadata("op")
            if mode == "gap":
                bad["contributions"][0]["CODE_LEDATA"][0]["offset"] = 1
            elif mode == "overlap":
                row = bad["contributions"][0]
                row["CODE_LEDATA"].append(copy.deepcopy(row["CODE_LEDATA"][0]))
            else:
                row = next(row for row in bad["contributions"] if len(row["ordered_MZ_fixups"]) > 1)
                row["ordered_MZ_fixups"].reverse()
            bad["evidence_digest"] = vc.evidence_digest(bad)
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, "LEDATA|ordered"):
                vc.validate_metadata(bad, context="op")

    def test_omf_fixup_flags_methods_and_indices_are_strict(self):
        mutations = [
            {"relative":"not-an-OMF-flag"}, {"relative":1},
            {"relative":True,"kind":2,"operation":"segment16"},
            {"relative":True,"operation":"far-pointer16:16"},
            {"relative":False,"kind":1,"operation":"self-relative16"},
            {"frame_method":False}, {"target_method":False}, {"kind":True},
            {"frame_method":1,"frame_index":-1},
            {"frame_method":0,"frame_index":False},
            {"frame_method":1,"frame_index":0x8000},
            {"frame_method":5,"frame_index":1},
            {"target_index":True}, {"target_index":0x8000}, {"segment":0},
        ]
        for change in mutations:
            bad = metadata("op")
            bad["contributions"][0]["fixup_actions"][0].update(change)
            bad["evidence_digest"] = vc.evidence_digest(bad)
            with self.subTest(change=change), self.assertRaises(ValueError):
                vc.validate_metadata(bad,context="op")

    def test_changed_program_or_ledata_hash_stales_evidence(self):
        for key in ("member_program_sha256", "linked_CODE_sha256"):
            bad = metadata("op"); bad["contributions"][0][key] = "0" * 64
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "digest"):
                vc.validate_metadata(bad, context="op")
        bad = metadata("op")
        bad["contributions"][0]["CODE_LEDATA"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "digest"):
            vc.validate_metadata(bad, context="op")

    def test_missing_or_promoted_deferred_case_rejects(self):
        bad = metadata("op"); bad["deferred"].pop()
        with self.assertRaisesRegex(ValueError, "deferred"):
            vc.validate_metadata(bad, context="op")
        bad = metadata("maine"); bad["deferred"][0]["decision"] = "VERIFIED"
        with self.assertRaisesRegex(ValueError, "deferred"):
            vc.validate_metadata(bad, context="maine")

    def test_boolean_credit_and_private_source_are_rejected(self):
        bad = metadata("op"); bad["authored_credit"] = False
        with self.assertRaisesRegex(ValueError, "proposal"):
            vc.validate_metadata(bad, context="op")
        bad = metadata("op"); bad["contributions"][0]["source_text"] = "private source"
        bad["evidence_digest"] = vc.evidence_digest(bad)
        with self.assertRaisesRegex(ValueError, "private vendor"):
            vc.validate_metadata(bad, context="op")

    def test_main_default_delegates_unchanged_contract(self):
        sentinel = object()
        with patch.object(vc.legacy, "review_inputs", return_value=sentinel) as replay:
            self.assertIs(vc.review_inputs(ROOT), sentinel)
            replay.assert_called_once_with(ROOT)
        self.assertEqual(vc.metadata_path(ROOT), ROOT / "config/vendor_ownership.json")
        proof = metadata("main")
        self.assertEqual(digest_bytes((ROOT / "scripts/review_vendor.py").read_bytes()), proof["verifier_sha256"])


class DecodedIdentityTests(unittest.TestCase):
    def setUp(self):
        self.fixture_case = fixtures.UnitContextTests()
        self.fixture_case.setUp()
        self.addCleanup(self.fixture_case.doCleanups)

    def test_reordered_relocations_reject_even_when_two_load_bytes_commute(self):
        first = self.fixture_case.fixture("op")
        artifact, image, proof = self.fixture_case.load(first)
        context, config, _, _ = first
        pins = {**vc.PINS["op"], "packed": artifact["sha256"],
                "payload": digest_bytes(image.program_image), "size": len(image.program_image),
                "receipt": proof["receipt_sha256"], "proof": proof_sha256(proof),
                "relocations": proof["relocations_sha256"]}
        with patch.dict(vc.PINS, {"op": pins}):
            vc.validate_target_context(context, config, artifact, image, proof)
            self.assertFalse(hasattr(image, "header"))
            reverse = self.fixture_case.fixture("op", reverse=True)
            other_artifact, other, other_proof = self.fixture_case.load(reverse)
            self.assertEqual(proof["runs"], other_proof["runs"])
            self.assertEqual(image.program_image, other.program_image)
            self.assertNotEqual(relative_fixups(image, 0, 32), relative_fixups(other, 0, 32))
            with self.assertRaisesRegex(ValueError, "proof|relocation"):
                vc.validate_target_context(reverse[0], reverse[1], other_artifact, other, other_proof)

    def test_private_calibration_map_executable_and_library_are_reread(self):
        # Isolate the private-byte identity gate after independently tested
        # decoded-context validation; no fabricated MZ is passed to a verifier.
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / ".analysis/builds/op-calibration-a/source"
            paths = {"calibration_exe": base / "bin/th05/op.exe",
                     "calibration_map": base / "obj/th05/op.map",
                     "library_sha256": root / ".analysis/toolchain/installed/tc40j/LIB/CL.LIB"}
            expected = {key: ("retained " + key).encode() for key in paths}
            for key,path in paths.items():
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(expected[key])
            pins = dict(vc.PINS["op"], **{key:digest_bytes(expected[key])
                         for key in ("calibration_exe", "calibration_map")})
            config = {"target_view": {"receipt_sha256":pins["receipt"],"proof_sha256":pins["proof"]}}
            context = SimpleNamespace(config=lambda: config)
            for key,path in paths.items():
                path.write_bytes(expected[key] + b"changed")
                with self.subTest(private_input=key), patch.dict(vc.PINS,{"op":pins}), \
                     patch.dict(vc.legacy.PINS,{"library_sha256":digest_bytes(expected["library_sha256"])}), \
                     patch.object(vc,"UnitContext",return_value=context), \
                     patch.object(vc,"load_unit_target",return_value=({},object(),{})), \
                     patch.object(vc,"validate_target_context"), \
                     patch.object(vc.legacy,"VendorReview") as verifier:
                    with self.assertRaisesRegex(ValueError,"calibration/MAP/library pin"):
                        vc.review_inputs(root,context="op")
                    verifier.assert_not_called()
                path.write_bytes(expected[key])

    def test_packed_target_and_context_have_separate_identities(self):
        first = self.fixture_case.fixture("op")
        artifact, image, proof = self.fixture_case.load(first)
        with self.assertRaisesRegex(ValueError, "packed"):
            vc.validate_target_context(first[0], first[1], artifact, image, proof)
        bad = dict(artifact, id="th05-maine")
        with self.assertRaisesRegex(ValueError, "artifact"):
            vc.validate_target_context(first[0], first[1], bad, image, proof)


class OptionalDecisionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.meta = metadata("op")
        for path in vc.REVIEWER_SOURCES + ["config/toolchain.toml"]:
            destination = self.root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, destination)
        self.proof_path = vc.metadata_path(self.root, "op")
        self.proof_path.write_text(json.dumps(self.meta))
        self.view = {"size": self.meta["target_payload_size"], "sha256": self.meta["target_payload_sha256"]}
        self.decision_path = self.root / "config/reviewed_vendor_units.op.json"
        self.decision = dict(schema_version=1,artifact="th05-op",decision="ADOPT_ONLY_LISTED_MEMBERS",
            classification="third-party-library-code",evidence_sha256=digest_bytes(self.proof_path.read_bytes()),
            target_sha256=self.meta["target_sha256"],target_payload_sha256=self.meta["target_payload_sha256"],
            authored_credit=0,authored_denominator=None,other_members_policy="unknown",uncovered_gaps_policy="unknown",
            members=[self.meta["contributions"][0]["member"]])

    def call(self, verify=False):
        return ownership.reviewed_context_vendor(self.root,context="op",view=self.view,verify_targets=verify)

    def write(self):
        self.decision_path.write_text(json.dumps(self.decision))

    def test_proposal_without_explicit_decision_has_no_claims(self):
        with patch.object(vc,"review_inputs") as replay:
            self.assertEqual(self.call(verify=True), ([],None))
            replay.assert_not_called()

    def test_native_decision_verification_replays_real_context(self):
        self.write()
        with patch.object(vc,"review_inputs",return_value=self.meta) as replay:
            claims, digest = self.call(verify=True)
            replay.assert_called_once_with(self.root,context="op")
            self.assertEqual(len(claims),1)
            self.assertEqual(digest,digest_bytes(self.decision_path.read_bytes()))
        with patch.object(vc,"review_inputs",return_value={"saved_status": "PASS"}):
            with self.assertRaisesRegex(ValueError,"replay"):
                self.call(verify=True)

    def test_unknown_deferred_duplicate_and_wrong_artifact_decisions_reject(self):
        for members in (["does_not_exist"], ["farheap"], self.decision["members"]*2, []):
            self.decision["members"] = members; self.write()
            with self.subTest(members=members), self.assertRaises(ValueError):
                self.call()
        self.decision["members"] = [self.meta["contributions"][0]["member"]]
        self.decision["artifact"] = "th05-maine"; self.write()
        with self.assertRaisesRegex(ValueError,"context|stale"):
            self.call()

    def test_stale_proof_packed_payload_and_authored_credit_reject(self):
        for key,value in [("evidence_sha256","0"*64),("target_payload_sha256",self.meta["target_sha256"]),
                          ("authored_credit",1),("authored_denominator",100)]:
            bad = dict(self.decision, **{key:value})
            self.decision_path.write_text(json.dumps(bad))
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.call()

    def test_vendor_overlap_with_accepted_source_is_not_clipped(self):
        self.write(); claims,_ = self.call()
        a,b = claims[0]["start"],claims[0]["end"]
        pieces = [{"start":0,"end":a,"kind":"unknown"},
                  {"start":a,"end":b,"kind":"accepted-cxx-instructions","unit":"fixture"},
                  {"start":b,"end":self.view["size"],"kind":"unknown"}]
        with self.assertRaisesRegex(ValueError,"overlap"):
            ownership.overlay_vendor(self.view["size"],pieces,claims)


if __name__ == "__main__":
    unittest.main()
