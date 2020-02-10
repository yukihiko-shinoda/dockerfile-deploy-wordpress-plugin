import os
import shutil
from pathlib import Path

import ansible_runner
import pytest

from tests.testlibraries.workspace import Workspace


@pytest.fixture
def git_repository_url():
    os.environ['GIT_REPOSITORY_URL'] = 'https://github.com/yukihiko-shinoda/staticpress.git'
    yield
    del os.environ['GIT_REPOSITORY_URL']


@pytest.fixture
def git_path_checked_out():
    os.environ['GIT_PATH_CHECKED_OUT'] = '/path/to/workspace'
    yield
    del os.environ['GIT_PATH_CHECKED_OUT']


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
def git_svn_checkout_workspace(subversion_dump, workspace):
    workspace.checkout_git('0.4.8')
    workspace.checkout_svn('HEAD')
    yield workspace
    workspace.remove_directory_svn()
    workspace.remove_directory_git()


@pytest.fixture
def workspace():
    yield Workspace()


@pytest.fixture
def subversion_dump(playbook_set_up_fixture, role_set_up_fixture, playbook_tear_down_fixture, role_tear_down_fixture):
    # @see https://unfuddle.com/stack/docs/help/svnrdump/
    runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook_set_up_fixture.yml')
    assert runner.status == 'successful'
    assert runner.rc == 0
    yield
    runner = ansible_runner.run(private_data_dir='/runner', playbook='playbook_tear_down_fixture.yml')
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


@pytest.fixture
def fixture_file(src, dest):
    yield from fixture_file_process(src, dest)


@pytest.fixture
def fixture_directory(src, dest):
    yield from fixture_directory_process(src, dest)


def playbook(playbook):
    yield from fixture_file_process(
        Path('project') / playbook, path_ansible_home() / playbook
    )


def role(role):
    yield from fixture_directory_process(
        Path('project/roles') / role, path_ansible_home() / 'roles' / role
    )


def fixture_file_process(src, dest):
    shutil.copy(path_test_resource() / src, dest)
    yield dest
    os.remove(dest)


def fixture_directory_process(src, dest):
    shutil.copytree(path_test_resource() / src, dest)
    yield dest
    shutil.rmtree(dest)


def path_ansible_home():
    return Path('/runner/project')


def path_test_resource():
    return Path(__file__).parent / 'testresources'
