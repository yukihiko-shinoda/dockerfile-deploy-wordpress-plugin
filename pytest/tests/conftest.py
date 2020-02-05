import os
import shutil

import pytest
from pathlib import Path
import ansible_runner


@pytest.fixture
def subversion_dump(playbook_set_up_fixture, playbook_tear_down_fixture):
    # @see https://unfuddle.com/stack/docs/help/svnrdump/
    runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook_set_up_fixture.yml', verbosity=3)
    assert runner.status == 'successful'
    assert runner.rc == 0
    yield
    runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook_tear_down_fixture.yml', verbosity=3)
    assert runner.status == 'successful'
    assert runner.rc == 0


@pytest.fixture
def playbook_set_up_fixture():
    yield from playbook('playbook_set_up_fixture.yml', 'set_up_fixture')


@pytest.fixture
def playbook_tear_down_fixture():
    yield from playbook('playbook_tear_down_fixture.yml', 'tear_down_fixture')


@pytest.fixture
def playbook_test():
    yield from playbook('playbook_test.yml', 'test')


def playbook(playbook, role):
    path_ansible_home = Path('/runner/project')
    path_ansible_test_resource = Path(__file__).parent / 'testresources/project'
    dest_playbook = path_ansible_home / playbook
    dest_role = path_ansible_home / 'roles' / role
    shutil.copy(path_ansible_test_resource / playbook, dest_playbook)
    shutil.copytree(path_ansible_test_resource / 'roles' / role, dest_role)
    yield
    os.remove(dest_playbook)
    shutil.rmtree(dest_role)
