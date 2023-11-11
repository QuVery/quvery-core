import os
import sys
import fnmatch
from typing import List, Optional


class IgnoreParser:
    def __init__(self, ignore_file_path: str):
        self.__ignore_file_path = ignore_file_path
        self.__ignore_patterns = []
        self.__base_path = ""
        self.parse_ignore_file()

    def parse_ignore_file(self):
        try:
            with open(self.__ignore_file_path, 'r') as file:
                self.__ignore_patterns = [line.strip()
                                          for line in file if line.strip()]
            # make sure that the patterns are in normpath format
            self.__ignore_patterns = [os.path.normpath(
                pattern) for pattern in self.__ignore_patterns]
        except FileNotFoundError:
            print(
                f"Warning: No .ignore file found at {self.__ignore_file_path}")

    def set_base_path(self, base_path: str):
        self.__base_path = base_path

    def is_ignored(self, path: str) -> bool:
        relative_path = os.path.relpath(path, self.__base_path)
        print(f"relative path: {relative_path}")
        for pattern in self.__ignore_patterns:
            if fnmatch.fnmatch(path, pattern) or relative_path.startswith(pattern):
                return True
        return False

    def add_patterns(self, patterns: List[str]):
        """
        Add custom patterns to the ignore list.
        Patterns should be in the format used by .gitignore.
        For pattern format, refer to: https://git-scm.com/docs/gitignore
        """
        self.__ignore_patterns.extend(patterns)

    def remove_patterns(self, patterns: List[str]):
        """
        Remove patterns from the ignore list.
        Patterns should match the format in the .ignore file.
        """
        self.__ignore_patterns = [
            p for p in self.__ignore_patterns if p not in patterns]

    def get_patterns(self) -> List[str]:
        return self.__ignore_patterns
