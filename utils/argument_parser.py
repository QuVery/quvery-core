import sys
from utils.logger import logger


class ArgumentParser:
    def __init__(self):
        self.args = sys.argv[1:]  # Ignore the script name itself
        self.parsed_args = {}
        self.handlers = {
            '--help': self._handle_help,
            '--version': self._handle_version,
            '--input': self._handle_input_file
        }

    def parse(self):
        if not self.args:
            self._handle_help()

        while self.args:
            arg = self.args.pop(0)
            handler = self.handlers.get(arg)
            if handler:
                handler()
            else:
                logger.info(f"Unknown argument: {arg}")
                self._handle_help()

    def _handle_help(self):
        print("Usage: Quvery-Core.exe [OPTIONS]")
        print("Options:")
        print("  --help                Show this help message and exit")
        print("  --version             Show program's version number and exit")
        print("  --input FILE          Path to input file")
        sys.exit()

    def _handle_version(self):
        print("Quvery 0.1.0")
        sys.exit()

    def _handle_input_file(self):
        if not self.args:
            raise ValueError("Expected file name after --input")
        file_path = self.args.pop(0)
        self.parsed_args['input_file'] = file_path
