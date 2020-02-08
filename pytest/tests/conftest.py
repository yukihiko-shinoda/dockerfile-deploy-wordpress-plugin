import os
import shutil
from pathlib import Path

import ansible_runner
import pytest
import testinfra

from tests.testlibraries.workspace import Workspace


@pytest.fixture
def clear_artifacts():
    # To prevent to get event of the test which executed last time.
    # @see https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder/185941#185941
    folder = '/runner/artifacts'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@pytest.fixture
def file_staged_workspace(workspace, src, dest):
    workspace.stage_file(Path(__file__).parent / 'testresources' / src, dest)
    yield workspace


@pytest.fixture
def workspace():
    yield Workspace(testinfra.get_host('ansible://all', ansible_inventory='/runner/inventory'))


@pytest.fixture
def subversion_dump(playbook_set_up_fixture, role_set_up_fixture, playbook_tear_down_fixture, role_tear_down_fixture):
    # @see https://unfuddle.com/stack/docs/help/svnrdump/
    runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook_set_up_fixture.yml', verbosity=3)
    assert runner.status == 'successful'
    assert runner.rc == 0
    yield
    runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook_tear_down_fixture.yml', verbosity=3)
    assert runner.status == 'successful'
    assert runner.rc == 0


@pytest.fixture
def playbook_tasks():
    yield from playbook('playbook_tasks.yml')


@pytest.fixture
def playbook_set_up_fixture():
    yield from playbook('playbook_set_up_fixture.yml')


@pytest.fixture
def role_set_up_fixture():
    yield from role('set_up_fixture')


@pytest.fixture
def playbook_tear_down_fixture():
    yield from playbook('playbook_tear_down_fixture.yml')


@pytest.fixture
def role_tear_down_fixture():
    yield from role('tear_down_fixture')


def playbook(playbook):
    dest_playbook = path_ansible_home() / playbook
    shutil.copy(path_ansible_test_resource() / playbook, dest_playbook)
    yield
    os.remove(dest_playbook)


def role(role):
    dest_role = path_ansible_home() / 'roles' / role
    shutil.copytree(path_ansible_test_resource() / 'roles' / role, dest_role)
    yield
    shutil.rmtree(dest_role)


def path_ansible_home():
    return Path('/runner/project')


def path_ansible_test_resource():
    return Path(__file__).parent / 'testresources/project'
