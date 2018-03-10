import sys
import pathlib
import logging

from fidsmod import Fids, InstantiationError

if __name__ == "__main__":
    formatter = logging.Formatter(fmt="%(message)s")
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger = logging.getLogger("fids_cli_logger")
    logger.addHandler(handler)

    checksumsFilePath = pathlib.Path(pathlib.Path.home() / "checksums.txt")

    try:
        fidsObject = Fids(checksumsFilePath, logger)
    except InstantiationError as err:
        logging.error(err.message)
        sys.exit(1)

    if not fidsObject.doOperation(sys.argv[1:]):
        sys.exit(1)

    sys.exit(0)