import tempfile
import unittest
from pathlib import Path

from file_manager import FileManagerError, create_file, delete_file, list_files, read_file, write_file
from utils import format_bytes


class FileManagerTests(unittest.TestCase):
    def test_create_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "note.txt"
            create_file(path)
            self.assertTrue(path.exists())
            with self.assertRaises(FileManagerError):
                create_file(path)

    def test_write_read_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "note.txt"
            write_file(path, "hello\n")
            self.assertEqual(read_file(path), "hello\n")
            write_file(path, "world\n", append=True)
            self.assertEqual(read_file(path), "hello\nworld\n")

    def test_delete_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "note.txt"
            path.write_text("data", encoding="utf-8")
            delete_file(path)
            self.assertFalse(path.exists())

    def test_directory_listing(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "b.txt").write_text("abc", encoding="utf-8")
            entries = list_files(tmp)
            self.assertEqual([e.name for e in entries], ["b.txt"])
            self.assertEqual(entries[0].size, 3)

    def test_cannot_delete_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileManagerError):
                delete_file(tmp)


class UtilityTests(unittest.TestCase):
    def test_format_bytes(self):
        self.assertEqual(format_bytes(0), "0.00 B")
        self.assertEqual(format_bytes(1024), "1.00 KB")


if __name__ == "__main__":
    unittest.main()
