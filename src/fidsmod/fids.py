import pathlib
import hashlib
import json

from .instantiationerror import InstantiationError


class Fids(object):
    """
    Fids (File Intrusion Detection System) class.
    """

    def __init__(self, checksumsFilePathObject, logger):
        self.logger = logger

        if checksumsFilePathObject.is_dir():
            raise InstantiationError("Provided checksums filepath points to a directory.")

        if not checksumsFilePathObject.exists():
            self.logger.warning("Checksums file could not be found. Creating a new one: " + str(checksumsFilePathObject))
            try:
                with checksumsFilePathObject.open("w") as checksumsFile:
                    json.dump(dict(), checksumsFile)  # Initialize with an empty dict
            except BaseException:
                raise InstantiationError("An error occurred while creating the checksums file!")
        else:
            try:
                with checksumsFilePathObject.open("r+") as checksumsFile:
                    json.load(checksumsFile)  # Check if the file content is a valid dict
            except BaseException:
                raise InstantiationError("Checksums file content is not valid!")

        self.checksumsFilePath = checksumsFilePathObject

    def doOperation(self, params):
        if not len(params) > 0:
            self.logger.critical("No arguments provided!")
            return False

        if params[0] == 'track':
            return self.track(params[1:])
        elif params[0] == 'untrack':
            return self.untrack(params[1:])
        elif params[0] == 'check':
            return self.check(params[1:])
        elif params[0] == 'update':
            return self.update(params[1:])
        elif params[0] == 'list':
            return self.list()
        else:
            self.logger.critical("Operation type is not valid: " + params[0])
            return False

    def track(self, params):
        if len(params) != 1:
            self.logger.warning("Too many arguments!")
            return False

        filePathObject = pathlib.Path(params[0])
        filePathObject = filePathObject.resolve()

        if filePathObject.is_file():
            if not self.writeChecksum(filePathObject):
                return False
            else:
                return True
        elif filePathObject.is_dir():
            for child in filePathObject.iterdir():
                if child.is_file():
                    if not self.writeChecksum(child):
                        return False
            return True
        else:
            self.logger.warning("File does not exist!")
            return False

    def untrack(self, params):
        # TODO
        pass

    def check(self, params):
        if len(params) != 1:
            self.logger.warning("Too many arguments!")
            return False

        filePathObject = pathlib.Path(params[0])
        filePathObject = filePathObject.resolve()

        if not filePathObject.is_file():
            self.logger.warning("Not a file!")

        previousChecksum = self.readChecksum(filePathObject)
        currentChecksum = Fids.calculateChecksum(filePathObject)

        if not previousChecksum:
            return False

        if not currentChecksum:
            return False

        if previousChecksum != currentChecksum:
            self.logger.info("File has been modified outside the app!")
            return True

            self.logger.info("File has not been modified!")
        return True

    def update(self, params):
        # TODO
        pass

    def list(self):
        try:
            rootDictionary = dict(json.loads(self.checksumsFilePath.read_text()))

            for item in rootDictionary:
                self.logger.info(item)

            return True
        except BaseException:
            self.logger.error("An error occurred!")

        return False

    def readChecksum(self, filePathObject):
        if not filePathObject.is_file():
            return str()

        try:
            rootDictionary = dict(json.loads(self.checksumsFilePath.read_text()))

            if str(filePathObject) in rootDictionary.keys():
                return rootDictionary[str(filePathObject)]
        except BaseException:
            pass

            self.logger.warning("File has not been tracked")
        return dict()

    def writeChecksum(self, filePathObject):
        filePathObject = filePathObject.resolve()
        if not filePathObject.is_file():
            return False

        checksum = Fids.calculateChecksum(filePathObject)
        if not checksum:
            return False

        try:
            rootDictionary = dict(json.loads(self.checksumsFilePath.read_text()))

            if str(filePathObject) in rootDictionary.keys():
                self.logger.warning("File has already been tracked: " + str(filePathObject))
                self.logger.warning("To update it, use the 'update' option.")
                return False

            rootDictionary[str(filePathObject)] = checksum
            self.checksumsFilePath.write_text(json.dumps(rootDictionary))
        except BaseException:
            self.logger.warning("Checksum could not be saved for the file: " + str(filePathObject))
            return False

        return True

    @staticmethod
    def calculateChecksum(filePathObject):
        try:
            return hashlib.sha256(filePathObject.read_bytes()).hexdigest()
        except BaseException:
            self.logger.error("An error occurred while calculating the checksum for file: " + str(filePathObject))
            return str()