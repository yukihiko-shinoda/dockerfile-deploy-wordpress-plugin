"""Tests for end to end."""
import os

import ansible_runner
import testinfra

from tests.testlibraries.workspace import Workspace


class TestEndToEnd:
    def test(self, subversion_dump):
        self.run_production('0.4.1')
        self.run_production('0.4.2')
        self.run_production('0.4.5')

        host = Workspace(testinfra.get_host('ansible://all', ansible_inventory='/runner/inventory'))
        host.checkout_svn(4)
        assert host.file_exists('/root/workdir/project-in-svn/tags/0.4.5/images/options32.png')
        host.checkout_svn(3)
        assert not host.file_exists('/root/workdir/project-in-svn/trunk/includes/class-admin-menu.php')
        assert host.file_exists('/root/workdir/project-in-svn/trunk/images/staticpress.png')
        assert host.check_line_in_file(
            '/root/workdir/project-in-svn/trunk/includes/class-InputValidator.php',
            "require_once(dirname(__FILE__).'/class-WP_Function_Wrapper.php');"
        )
        assert not host.file_exists('/root/workdir/project-in-svn/tags/0.4.2/images/options32.png')
        host.checkout_svn(2)
        assert host.file_exists('/root/workdir/project-in-svn/trunk/includes/class-admin-menu.php')
        assert not host.check_line_in_file(
            '/root/workdir/project-in-svn/trunk/includes/class-InputValidator.php',
            "require_once(dirname(__FILE__).'/class-WP_Function_Wrapper.php');"
        )
        assert host.file_exists('/root/workdir/project-in-svn/tags/0.4.1/images/options32.png')


    @staticmethod
    def run_production(deploy_version):
        os.environ['DEPLOY_VERSION'] = deploy_version
        runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook.yml', verbosity=3)
        assert runner.status == 'successful'
        assert runner.rc == 0
