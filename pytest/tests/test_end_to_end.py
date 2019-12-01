"""Tests for end to end."""
import os

import ansible_runner


class TestEndToEnd:
    def test(self, environment_variable):
        self.run_production('0.4.1')
        self.run_production('0.4.2')
        self.run_production('0.4.5')
        runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook_test.yml', verbosity=3)
        assert runner.status == 'successful'
        assert runner.rc == 0
        print(runner.stats)

    @staticmethod
    def run_production(deploy_version):
        os.environ['DEPLOY_VERSION'] = deploy_version
        runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook.yml', verbosity=3)
        assert runner.status == 'successful'
        assert runner.rc == 0
