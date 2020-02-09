"""Tests for end to end."""
import os

import ansible_runner


class TestEndToEnd:
    def test(self, subversion_dump, workspace):
        self.run_production('0.4.1')
        self.run_production('0.4.2')
        self.run_production('0.4.5')

        workspace.checkout_svn(4, path='/root/workdir/project-in-svn')
        assert workspace.file_exists('/root/workdir/project-in-svn/tags/0.4.5/images/options32.png')
        workspace.checkout_svn(3, path='/root/workdir/project-in-svn')
        assert not workspace.file_exists('/root/workdir/project-in-svn/trunk/includes/class-admin-menu.php')
        assert workspace.file_exists('/root/workdir/project-in-svn/trunk/images/staticpress.png')
        assert workspace.check_line_in_file(
            '/root/workdir/project-in-svn/trunk/includes/class-InputValidator.php',
            "require_once(dirname(__FILE__).'/class-WP_Function_Wrapper.php');"
        )
        assert not workspace.file_exists('/root/workdir/project-in-svn/tags/0.4.2/images/options32.png')
        workspace.checkout_svn(2, path='/root/workdir/project-in-svn')
        assert workspace.file_exists('/root/workdir/project-in-svn/trunk/includes/class-admin-menu.php')
        assert not workspace.check_line_in_file(
            '/root/workdir/project-in-svn/trunk/includes/class-InputValidator.php',
            "require_once(dirname(__FILE__).'/class-WP_Function_Wrapper.php');"
        )
        assert workspace.file_exists('/root/workdir/project-in-svn/tags/0.4.1/images/options32.png')

    @staticmethod
    def run_production(deploy_version):
        os.environ['DEPLOY_VERSION'] = deploy_version
        runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook.yml')
        assert runner.status == 'successful'
        assert runner.rc == 0
