import argparse
import os
import sys

from git import Repo

from xh_py_project_versioning.PyProject import PyProject
from xh_py_project_versioning.PyPiRepo import PyPiRepo
from xh_py_project_versioning.versioning import SemVer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="py-project-versioner",
        description="snippet update version of python `pyproject.toml`"
    )

    parser.add_argument("--project-file", type=str, default="pyproject.toml")
    parser.add_argument("--version-mod", type=str, choices=["major", "minor", "patch"], default="",
                        help="the mode of modification")
    parser.add_argument("--diff", action="store_true", help="diff the version between online and local")
    parser.add_argument("-d", "--direct", action="store_true", help="upgrade")
    parser.add_argument("--patch", dest="version_mod", action="store_const", const="patch",
                        help="update the patch level[default option]")
    parser.add_argument("--minor", dest="version_mod", action="store_const", const="minor",
                        help="update the minor level")
    parser.add_argument("--major", dest="version_mod", action="store_const", const="major",
                        help="update the mjaro level")
    parser.add_argument("-r", "--release", action="store_true", default=False,
                        help="release with any build meta removed")


    argv = parser.parse_args(sys.argv[1:])
    project_file = argv.project_file
    if not os.path.exists(project_file) and not os.path.is_file(project_file):
        raise Exception(f"project-file[{project_file}] not exists")

    version_mod = argv.version_mod

    py_project = PyProject.from_toml(project_file)
    version_str = py_project.get_version()
    project_name = py_project.get_project_name()

    online_version = PyPiRepo(project_name).getVersion()

    if not argv.diff and not argv.release and version_mod == "":
        print(f"Remote version[{str(online_version)}]\nLocal version[{version_str}]")
        exit(0)

    if argv.diff:
        if str(online_version) == version_str:
            raise Exception(f"Remote version[{online_version}] is the same as local version[{version_str}]")
        else:
            print(f"Remote version[{str(online_version)}] != Local version[{version_str}]")
        exit()

    sem_ver = SemVer.from_str(version_str)
    old_version = str(sem_ver)
    op_tag = ""
    if argv.release:
        py_project.update_version(sem_ver)
        op_tag = "release"
    elif sem_ver.is_not_dev():
        if version_mod == "major":
            sem_ver.increase_major()
        elif version_mod == "minor":
            sem_ver.increase_minor()
        elif version_mod == "patch":
            sem_ver.increase_patch()

        sem_ver.set_pre_release("dev")
        sem_ver.set_build(0)
        py_project.update_version(sem_ver)
        op_tag="dev start"

    else:
        sem_ver.increase_build()
        py_project.update_version(sem_ver)
        op_tag="dev progress"


    py_project.persist(project_file)

    Repo(".").git.add(project_file)
    print(f"[{op_tag}]{old_version} -> {str(sem_ver)}")

