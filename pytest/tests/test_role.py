import ansible_runner
# from ansible_runner import Runner
# from ansible_runner.runner_config import RunnerConfig


class TestRole:
    def test_rsync_git_to_svn_default_rsync_filter(self, git_svn_checkout_workspace, clear_artifacts, playbook_tasks):
        self.run_role()
        workspace = git_svn_checkout_workspace
        assert workspace.file_exists('/root/workdir/my-local-dir/trunk/plugin.php')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/.git')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/.github')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/bin')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/tests')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/.gitignore')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/.phpcs.xml.dist')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/.travis.yml')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/phpunit.xml.dist')

    def test_rsync_git_to_svn_project_rsync_filter(
        self, git_svn_checkout_rsync_filter_staged_workspace, clear_artifacts, playbook_tasks
    ):
        self.run_role()
        workspace = git_svn_checkout_rsync_filter_staged_workspace
        assert workspace.file_exists('/root/workdir/my-local-dir/trunk/plugin.php')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/.git')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/.github')
        assert workspace.file_exists('/root/workdir/my-local-dir/trunk/bin')
        assert workspace.file_exists('/root/workdir/my-local-dir/trunk/tests')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/.gitignore')
        assert workspace.file_exists('/root/workdir/my-local-dir/trunk/.phpcs.xml.dist')
        assert not workspace.file_exists('/root/workdir/my-local-dir/trunk/.travis.yml')
        assert workspace.file_exists('/root/workdir/my-local-dir/trunk/phpunit.xml.dist')

    def run_role(self):
        # runner_config = RunnerConfig(
        #     private_data_dir='/runner',
        #     playbook='playbook.yml',
        #     tags=['rsync_git_to_svn']
        # )
        # ansible_runner = Runner(config=runner_config)
        # runner = ansible_runner.run()
        runner = ansible_runner.run(
            private_data_dir='/runner',
            playbook='playbook.yml',
            tags='rsync_git_to_svn',
            extravars={'path_checkout_git': '/root/workdir/git-working-dir'}
        )
        assert runner.status == 'successful'
        assert runner.rc == 0
