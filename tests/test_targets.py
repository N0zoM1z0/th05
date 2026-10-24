"""Target identity and MZ structure must reject corrupted private inputs."""
import hashlib
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.pc98 import parse_mz
from lib.targets import TargetError, find_artifact, read_verified_artifact


def mz_fixture() -> bytes:
    # 32-byte header, 16-byte code, initial SP fitting one extra paragraph.
    fields = [0x5A4D, 48, 1, 0, 2, 1, 0xFFFF, 0, 16, 0, 0, 0, 28, 0]
    return struct.pack("<14H", *fields) + bytes(4) + bytes(16)


class TargetTests(unittest.TestCase):
    def test_mz_layout(self):
        image = parse_mz(mz_fixture())
        self.assertTrue(image.valid, image.errors)
        self.assertEqual(image.header.header_size, 32)
        self.assertEqual(len(image.program_image), 16)

    def test_mz_rejects_truncated_image(self):
        self.assertFalse(parse_mz(mz_fixture()[:-1]).valid)

    def test_mz_rejects_invalid_relocation_table(self):
        data = bytearray(mz_fixture())
        struct.pack_into("<H", data, 6, 2)
        self.assertFalse(parse_mz(bytes(data)).valid)

    def test_target_mutation_rejected(self):
        data = mz_fixture()
        artifact = {"id": "fixture", "private_path": "test.exe", "size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "md5": hashlib.md5(data).hexdigest(), "format": "mz"}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "test.exe"
            path.write_bytes(data)
            self.assertEqual(read_verified_artifact(root, artifact), data)
            path.write_bytes(data[:-1] + b"\x01")
            with self.assertRaises(TargetError):
                read_verified_artifact(root, artifact)

    def test_artifact_ambiguity_rejected(self):
        with self.assertRaises(TargetError):
            find_artifact({"artifacts": [{"id": "x"}, {"id": "x"}]}, "x")


if __name__ == "__main__":
    unittest.main()
