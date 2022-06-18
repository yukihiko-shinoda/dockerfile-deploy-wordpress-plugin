import os

import ansible_runner

import pytest


class TestRole:
    @pytest.mark.usefixtures("git_repository_url", "git_svn_checkout_workspace", "clear_artifacts", "playbook_tasks")
    def test_rsync_git_to_svn_default_rsync_filter(self) -> None:
        self.run_role()
        assert os.path.exists("/root/workdir/my-local-dir/trunk/plugin.php")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/.git")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/.github")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/bin")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/tests")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/.gitignore")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/.phpcs.xml.dist")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/.travis.yml")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/phpunit.xml.dist")

    @pytest.mark.parametrize("src, dest", [[".rsync-filter", "/root/workdir/git-working-dir/.rsync-filter"]])
    @pytest.mark.usefixtures(
        "git_repository_url", "git_svn_checkout_workspace", "fixture_file", "clear_artifacts", "playbook_tasks"
    )
    def test_rsync_git_to_svn_project_rsync_filter(self) -> None:
        self.run_role()
        assert os.path.exists("/root/workdir/my-local-dir/trunk/plugin.php")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/.git")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/.github")
        assert os.path.exists("/root/workdir/my-local-dir/trunk/bin")
        assert os.path.exists("/root/workdir/my-local-dir/trunk/tests")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/.gitignore")
        assert os.path.exists("/root/workdir/my-local-dir/trunk/.phpcs.xml.dist")
        assert not os.path.exists("/root/workdir/my-local-dir/trunk/.travis.yml")
        assert os.path.exists("/root/workdir/my-local-dir/trunk/phpunit.xml.dist")

    def run_role(self) -> None:
        runner = ansible_runner.run(
            private_data_dir="/runner",
            playbook="playbook.yml",
            tags="rsync_git_to_svn",
            extravars={"path_checkout_git": "/root/workdir/git-working-dir"},
        )
        assert runner.status == "successful"
        assert runner.rc == 0
