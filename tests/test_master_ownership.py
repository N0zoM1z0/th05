"""Explicit Master adoption policy and inventory integration, public inputs only."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import tomllib
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ci
import ownership
from lib.pc98 import digest_bytes


class MasterDecisionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.proof = json.loads((ROOT / "config/master_vendor_ownership.json").read_text())
        self.decision = json.loads((ROOT / "config/reviewed_master_procedures.json").read_text())
        self.view = {"size": 145958, "sha256": self.proof["target_payload_sha256"]}
        for relative in ["config/master_vendor_ownership.json", "config/reviewed_master_procedures.json",
                         *[x["file"] for x in self.proof["reviewer_sources"]]]:
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((ROOT / relative).read_bytes())

    def write_decision(self, value):
        (self.root / "config/reviewed_master_procedures.json").write_text(json.dumps(value))

    def claims(self, **kwargs):
        return ownership.reviewed_master(self.root, view=kwargs.get("view", self.view),
                                         verify_targets=kwargs.get("verify_targets", False))

    def native_summary(self):
        return dict(kind="native-master-procedure-review", decision="PROPOSAL",
                    byte_proof_replayed=True, procedures=20, full_bytes=376,
                    instruction_bytes=367, padding_bytes=9, authored_credit=0,
                    denominator_changed=False)

    def test_no_optional_decision_leaves_every_procedure_unclassified(self):
        (self.root / "config/reviewed_master_procedures.json").unlink()
        (self.root / "config/master_vendor_ownership.json").unlink()
        self.assertEqual(self.claims(), ([], None))

    def test_exact_twenty_full_extents_include_library_padding_without_credit(self):
        claims, digest = self.claims()
        self.assertEqual(len(claims), 20)
        self.assertEqual(sum(x["end"]-x["start"] for x in claims), 376)
        self.assertEqual({x["member"] for x in claims}, set(self.decision["procedures"]))
        self.assertEqual(digest, digest_bytes((self.root / "config/reviewed_master_procedures.json").read_bytes()))
        pieces = ownership.overlay_vendor(145958, ownership.partition(145958, []), claims)
        for procedure in self.proof["procedures"]:
            for pad in procedure["padding"]:
                row = next(x for x in pieces if x["start"] <= pad["start"] < x["end"])
                self.assertEqual(row["kind"], "verified-vendor-code")
        for gap in self.proof["uncovered_gaps"]:
            self.assertTrue(all(x["kind"] == "unknown" for x in pieces
                                if x["start"] < gap["end"] and gap["start"] < x["end"]))
        self.assertEqual(self.decision["authored_credit"], 0)
        self.assertIsNone(self.decision["authored_denominator"])

    def test_stale_proof_target_artifact_and_classification_are_rejected(self):
        for key, value in (("schema_version", True), ("evidence_sha256", "0"*64), ("target_sha256", "0"*64),
                           ("target_payload_sha256", "0"*64), ("artifact", "th05-op"),
                           ("classification", "authored-code"), ("decision", "ADOPT_PREFIX")):
            with self.subTest(key=key):
                bad=copy.deepcopy(self.decision);bad[key]=value;self.write_decision(bad)
                with self.assertRaisesRegex(ValueError, "stale|classification"):
                    self.claims()
        self.write_decision(self.decision)
        with self.assertRaisesRegex(ValueError, "different target"):
            self.claims(view={**self.view, "sha256":"0"*64})
        proof_path = self.root / "config/master_vendor_ownership.json"
        proof_path.write_bytes(proof_path.read_bytes()+b"\n")
        with self.assertRaisesRegex(ValueError, "stale"):
            self.claims()

    def test_unknown_deferred_duplicate_and_partial_procedure_lists_reject(self):
        names=self.decision["procedures"]
        for selected in (names[:-1], names+["UNKNOWN"], names[:-1]+[names[0]],
                         names[:-1]+["UNKNOWN"], names[:-1]+[self.proof["deferred_source_mismatches"][0]["name"]],
                         names[:-1]+[["not-a-name"]]):
            with self.subTest(selected=selected):
                bad=copy.deepcopy(self.decision);bad["procedures"]=selected;self.write_decision(bad)
                with self.assertRaisesRegex(ValueError, "unique|unknown|deferred"):
                    self.claims()

    def test_credit_unknown_policy_and_extent_totals_cannot_change(self):
        for key,value in (("authored_credit",367), ("authored_credit",False),
                          ("authored_denominator",10000), ("other_procedures_policy","vendor"),
                          ("uncovered_gaps_policy","excluded"), ("full_bytes",367),
                          ("instruction_bytes",376), ("padding_bytes",0)):
            with self.subTest(key=key):
                bad=copy.deepcopy(self.decision);bad[key]=value;self.write_decision(bad)
                with self.assertRaises(ValueError):self.claims()

    def test_verify_targets_calls_actual_reviewer_entry_with_full_proof(self):
        with patch("review_master.review_inputs", return_value=self.native_summary()) as review:
            self.claims(verify_targets=True)
            review.assert_called_once_with(self.proof, root=self.root)
        with patch("review_master.review_inputs", side_effect=ValueError("actual input drift")):
            with self.assertRaisesRegex(ValueError,"actual input drift"):
                self.claims(verify_targets=True)
        for result in (None, {**self.native_summary(), "byte_proof_replayed":False},
                       {**self.native_summary(), "full_bytes":375}):
            with patch("review_master.review_inputs", return_value=result):
                with self.assertRaisesRegex(ValueError,"native private Master"):
                    self.claims(verify_targets=True)
        with patch("review_master.review_inputs", side_effect=AssertionError("private replay in public mode")):
            self.claims()

    def test_combined_claims_cannot_overlap_cl_or_accepted_source(self):
        claims,_=self.claims();first=claims[0]
        duplicate={**first,"library":"CL.LIB","member":"synthetic-cl"}
        with self.assertRaisesRegex(ValueError,"overlaps"):
            ownership.overlay_vendor(145958, ownership.partition(145958, []), [duplicate]+claims)
        source=dict(id="source", target_start=first["start"], size=1)
        with self.assertRaisesRegex(ValueError,"overlaps accepted source"):
            ownership.overlay_vendor(145958, ownership.partition(145958, [source]), claims)

    def test_main_inventory_combines_decisions_with_separate_digests(self):
        for relative in ("config/ownership.toml", "config/targets.toml"):
            (self.root / relative).write_bytes((ROOT / relative).read_bytes())
        config=tomllib.loads((self.root / "config/ownership.toml").read_text())
        def context(root,name):
            ledger=self.root / (name+"-ledger.json")
            view=config["views"][name]
            ledger.write_text(json.dumps(dict(units=[], target_view=dict(payload_size=view["size"],payload_sha256=view["sha256"]))))
            return SimpleNamespace(ledger=ledger,config=lambda:dict(units=[]))
        cl_claim=dict(start=0,end=1,kind="verified-vendor-code",library="CL.LIB",member="synthetic-cl")
        summary=dict(instruction_bytes=0,code_data_bytes=0,authored_data_bytes=0,padding_bytes=0)
        with patch.object(ownership,"UnitContext",side_effect=context), \
                patch.object(ownership,"summarize_all",return_value=summary), \
                patch.object(ownership,"reviewed_vendor",return_value=([cl_claim],"existing-cl-digest")):
            result=ownership.inventory(self.root)
        main=result["views"]["main"]
        self.assertEqual(main["byte_counts"]["verified-vendor-code"],377)
        self.assertEqual(main["vendor_review_sha256"],"existing-cl-digest")
        self.assertEqual(main["master_vendor_review_sha256"],self.claims()[1])
        self.assertEqual(main["byte_counts"]["unknown"],145958-377)
        self.assertIsNone(result["authored_denominator"])
        self.assertIsNone(result["percentage"])
        for name in ("op","maine","zun"):
            self.assertNotIn("master_vendor_review_sha256",result["views"][name])


class MasterPublicCITests(unittest.TestCase):
    def test_public_ci_dispatches_structure_only_without_private_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ("scripts","config","tests"):(root/name).mkdir()
            (root / "config/master_vendor_ownership.json").write_text("{}")
            with patch.object(ci,"ROOT",root), patch.object(ci.subprocess,"run",return_value=SimpleNamespace(returncode=0)) as run:
                self.assertEqual(ci.main(),0)
            commands=[x.args[0] for x in run.call_args_list]
            self.assertIn([sys.executable,"scripts/review_master.py","--structural-check"],commands)
            self.assertNotIn([sys.executable,"scripts/review_master.py","--check"],commands)


if __name__ == "__main__":
    unittest.main()
