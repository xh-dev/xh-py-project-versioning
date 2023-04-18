import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class SemVer:
    major: int
    minor: int
    patch: int
    pre_release: Optional[str]
    build: Optional[int]

    def increase_major(self):
        self.major = self.major+1

    def increase_minor(self):
        self.minor = self.minor+1

    def increase_patch(self):
        self.patch = self.patch+1

    def set_pre_release(self, pre_release: str):
        self.pre_release = pre_release

    def increase_build(self):
        self.build = 0 if self.build is None else self.build

    def set_build(self, build: Optional[int]):
        self.build = build

    def is_not_dev(self):
        return not self.is_dev()

    def is_dev(self):
        if self.pre_release is None:
            return False
        elif self.pre_release == "dev":
            return True
        else:
            return False

    def __str__(self):
        pre_release_str = f"-{self.pre_release}" if self.pre_release is not None else ""
        build_str = f"-{self.build}" if self.build is not None else ""
        return f"{self.major}.{self.minor}.{self.patch}{pre_release_str}{build_str}"

    def __repr__(self):
        self.__str__()

    @staticmethod
    def from_str(sem_ver_string: str) -> 'SemVer':
        pattern = re.compile("^(\\d+)\\.(\\d+)\\.(\\d+)(-dev)?(\\+[^ ]+)?$")
        matcher = pattern.match(sem_ver_string)
        if matcher:
            major = int(matcher.group(1))
            minor = int(matcher.group(2))
            patch = int(matcher.group(3))
            pre_release = matcher.group(4)[1:] if matcher.group(4) else None
            build = int(matcher.group(5)[1:]) if matcher.group(5) else None
            return SemVer(major, minor, patch, pre_release, build)
        else:
            raise Exception("not match version")


