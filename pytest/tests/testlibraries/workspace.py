import os
from typing import Optional

import testinfra


class Workspace:
    PATH_GIT_CHECKOUT = "/root/workdir/git-working-dir"
    PATH_SVN_CHECKOUT = "/root/workdir/my-local-dir"

    def __init__(self) -> None:
        self.host = testinfra.get_host("ansible://all", ansible_inventory="/runner/inventory")
        self.git_repository_url = os.environ["GIT_REPOSITORY_URL"]
        self.svn_repository_url = os.environ["SVN_REPOSITORY_URL"]
        self.staged_file = None

    def checkout_git(self, version: str, *, path: Optional[str] = None) -> None:
        if path is None:
            path = self.PATH_GIT_CHECKOUT
        parameters = " ".join([f"repo={self.git_repository_url}", f"dest={path}", f"version={version}"])
        result = self.host.ansible("git", parameters, check=False)
        print(result)
        assert "changed" in result, result["msg"]

    def checkout_svn(self, revision: str, *, path: Optional[str] = None) -> None:
        if path is None:
            path = self.PATH_SVN_CHECKOUT
        parameters = " ".join([f"repo={self.svn_repository_url}", f"dest={path}", f"revision={revision}"])
        result = self.host.ansible("subversion", parameters, check=False)
        print(result)
        assert "changed" in result and result["changed"], result["msg"]

    def check_line_in_file(self, name: str, line: str) -> bool:
        result = self.host.ansible("lineinfile", " ".join([f"name={name}", f"line={line}"]))
        print(result)
        return bool(result["changed"])

    def remove_directory_git(self) -> None:
        self.remove_file_or_directory(self.PATH_GIT_CHECKOUT)

    def remove_directory_svn(self) -> None:
        self.remove_file_or_directory(self.PATH_SVN_CHECKOUT)

    def remove_file_or_directory(self, path: str) -> None:
        result = self.host.ansible("file", " ".join([f"path={path}", "state=absent"]), check=False)
        assert "changed" in result, result["msg"]
