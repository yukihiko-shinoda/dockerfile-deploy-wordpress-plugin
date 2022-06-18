"""Tests for end to end."""
import os

import ansible_runner

import pytest
from tests.testlibraries.workspace import Workspace


class TestEndToEnd:
    @pytest.mark.usefixtures("subversion_dump", "git_repository_url", "git_path_checked_out")
    def test(self, workspace: Workspace) -> None:
        self.run_production("0.4.1")
        workspace.checkout_git("0.4.2", path=os.environ["GIT_PATH_CHECKED_OUT"])
        self.run_production("0.4.2", checked_out=True)
        self.run_production("0.4.5")

        workspace.checkout_svn("4", path="/root/workdir/project-in-svn")
        assert os.path.exists("/root/workdir/project-in-svn/tags/0.4.5/images/options32.png")
        workspace.checkout_svn("3", path="/root/workdir/project-in-svn")
        assert not os.path.exists("/root/workdir/project-in-svn/trunk/includes/class-admin-menu.php")
        assert os.path.exists("/root/workdir/project-in-svn/trunk/images/staticpress.png")
        assert workspace.check_line_in_file(
            "/root/workdir/project-in-svn/trunk/includes/class-InputValidator.php",
            "require_once(dirname(__FILE__).'/class-WP_Function_Wrapper.php');",
        )
        assert not os.path.exists("/root/workdir/project-in-svn/tags/0.4.2/images/options32.png")
        workspace.checkout_svn("2", path="/root/workdir/project-in-svn")
        assert os.path.exists("/root/workdir/project-in-svn/trunk/includes/class-admin-menu.php")
        assert not workspace.check_line_in_file(
            "/root/workdir/project-in-svn/trunk/includes/class-InputValidator.php",
            "require_once(dirname(__FILE__).'/class-WP_Function_Wrapper.php');",
        )
        assert os.path.exists("/root/workdir/project-in-svn/tags/0.4.1/images/options32.png")

    @staticmethod
    def run_production(deploy_version: str, *, checked_out: bool = False) -> None:
        key_to_delete = "GIT_REPOSITORY_URL" if checked_out else "GIT_PATH_CHECKED_OUT"
        backup = os.environ[key_to_delete]
        del os.environ[key_to_delete]

        os.environ["DEPLOY_VERSION"] = deploy_version
        runner = ansible_runner.run(private_data_dir="/runner", playbook="playbook.yml")
        assert runner.status == "successful"
        assert runner.rc == 0

        os.environ[key_to_delete] = backup
