import pathlib
import unittest
import logging

from fidsmod import Fids


class TestFids(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tempPath = pathlib.Path.cwd() / "temp"
        cls.tempPath.mkdir()
        cls.tempFolderPath1 = pathlib.Path(cls.tempPath / "temp_folder1")
        cls.tempFolderPath1.mkdir()

    def setUp(self):
        self.tempFile1 = pathlib.Path(self.tempPath / "temp_file1.txt")
        self.tempFile1.write_text("asdfghjkl")
        self.tempFile1Checksum = "5c80565db6f29da0b01aa12522c37b32f121cbe47a861ef7f006cb22922dffa1"

        self.tempFile2 = pathlib.Path(self.tempFolderPath1 / "temp_file2.txt")
        self.tempFile2.write_text("qazwsxedc")
        self.tempFile2Checksum = "80d41c54a8ce6d26ae0bdd509db6b187140cae39b4b771269a0d006b0620e2d2"

        self.tempChecksumsFile = pathlib.Path(self.tempPath / "checksums.txt")

    def tearDown(self):
        if self.tempChecksumsFile.exists():
            self.tempChecksumsFile.unlink()
        self.tempFile1.unlink()
        self.tempFile2.unlink()

    @classmethod
    def tearDownClass(cls):
        cls.removeDir(cls.tempPath)

    @classmethod
    def removeDir(cls, dirPath):
        for child in dirPath.iterdir():
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                cls.removeDir(child)

        dirPath.rmdir()

    def testInit(self):
        # TODO
        self.fail()

    def testDoOperation(self):
        # TODO
        self.fail()

    def testTrack(self):
        # TODO
        self.fail()

    def testRtrack(self):
        # TODO
        self.fail()

    def testUntrack(self):
        # TODO
        self.fail()

    def testRuntrack(self):
        # TODO
        self.fail()

    def testRename(self):
        # TODO
        self.fail()

    def testMove(self):
        # TODO
        self.fail()

    def testDelete(self):
        # TODO
        self.fail()

    def testCheck(self):
        # TODO
        self.fail()

    def testRcheck(self):
        # TODO
        self.fail()

    def testUpdate(self):
        # TODO
        self.fail()

    def testRupdate(self):
        # TODO
        self.fail()

    def testList(self):
        # TODO
        self.fail()

    def testHelp(self):
        # TODO
        self.fail()

    def testCalculateChecksum(self):
        newChecksumString = Fids.calculateChecksum(self.tempFile1)
        self.assertEqual(self.tempFile1Checksum, newChecksumString, "Calculated checksum of tempFile1 is not valid")

        newChecksumString2 = Fids.calculateChecksum(self.tempFile2)
        self.assertEqual(self.tempFile2Checksum, newChecksumString2, "Calculated checksum of tempFile2 is not valid")


if __name__ == '__main__':
    handler = logging.NullHandler()
    logger = logging.getLogger("fids_test_logger")
    logger.addHandler(handler)
    unittest.main()