from logging import getLogger
import os
from pathlib import Path
import shutil
from typing import Generator

import ansible_runner

import pytest
from tests.testlibraries.workspace import Workspace


@pytest.fixture
def git_repository_url() -> Generator[None, None, None]:
    os.environ["GIT_REPOSITORY_URL"] = "https://github.com/yukihiko-shinoda/staticpress.git"
    yield
    del os.environ["GIT_REPOSITORY_URL"]


@pytest.fixture
def git_path_checked_out() -> Generator[None, None, None]:
    os.environ["GIT_PATH_CHECKED_OUT"] = "/path/to/workspace"
    yield
    del os.environ["GIT_PATH_CHECKED_OUT"]


@pytest.fixture
def clear_artifacts() -> None:
    """To prevent to get event of the test which executed last time.

    see: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder/185941#185941
    """
    logger = getLogger(__name__)
    folder = "/runner/artifacts"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as error:  # Reason: To debug. pylint: disable=broad-except
            logger.exception(error)
            logger.error("Failed to delete %s. Reason: %s", file_path, error, exc_info=error)
            raise


@pytest.fixture
# Reason: Fixture can't use @pytest.marks.usefixture(). pylint: disable=unused-argument,redefined-outer-name
def git_svn_checkout_workspace(subversion_dump: None, workspace: Workspace) -> Generator[Workspace, None, None]:
    workspace.checkout_git("0.4.8")
    workspace.checkout_svn("HEAD")
    yield workspace
    workspace.remove_directory_svn()
    workspace.remove_directory_git()


@pytest.fixture
def workspace() -> Generator[Workspace, None, None]:
    yield Workspace()


@pytest.fixture
def subversion_dump(
    # Reason: Fixture can't use @pytest.marks.usefixture(). pylint: disable=unused-argument,redefined-outer-name
    playbook_set_up_fixture: Path,
    role_set_up_fixture: Path,
    playbook_tear_down_fixture: Path,
    role_tear_down_fixture: Path,
) -> Generator[None, None, None]:
    # @see https://unfuddle.com/stack/docs/help/svnrdump/
    runner = ansible_runner.run(private_data_dir="/runner", playbook="playbook_set_up_fixture.yml")
    assert runner.status == "successful"
    assert runner.rc == 0
    yield
    runner = ansible_runner.run(private_data_dir="/runner", playbook="playbook_tear_down_fixture.yml")
    assert runner.status == "successful"
    assert runner.rc == 0


@pytest.fixture
def playbook_tasks() -> Generator[Path, None, None]:
    yield from playbook("playbook_tasks.yml")


@pytest.fixture
def playbook_set_up_fixture() -> Generator[Path, None, None]:
    yield from playbook("playbook_set_up_fixture.yml")


@pytest.fixture
def role_set_up_fixture() -> Generator[Path, None, None]:
    yield from role("set_up_fixture")


@pytest.fixture
def playbook_tear_down_fixture() -> Generator[Path, None, None]:
    yield from playbook("playbook_tear_down_fixture.yml")


@pytest.fixture
def role_tear_down_fixture() -> Generator[Path, None, None]:
    yield from role("tear_down_fixture")


@pytest.fixture
def fixture_file(src: Path, dest: Path) -> Generator[Path, None, None]:
    yield from fixture_file_process(src, dest)


@pytest.fixture
def fixture_directory(src: Path, dest: Path) -> Generator[Path, None, None]:
    yield from fixture_directory_process(src, dest)


def playbook(playbook_file_name: str) -> Generator[Path, None, None]:
    yield from fixture_file_process(Path("project") / playbook_file_name, path_ansible_home() / playbook_file_name)


def role(role_directory_name: str) -> Generator[Path, None, None]:
    src = Path("project/roles") / role_directory_name
    yield from fixture_directory_process(src, path_ansible_home() / "roles" / role_directory_name)


def fixture_file_process(src: Path, dest: Path) -> Generator[Path, None, None]:
    shutil.copy(path_test_resource() / src, dest)
    yield dest
    os.remove(dest)


def fixture_directory_process(src: Path, dest: Path) -> Generator[Path, None, None]:
    shutil.copytree(path_test_resource() / src, dest)
    yield dest
    shutil.rmtree(dest)


def path_ansible_home() -> Path:
    return Path("/runner/project")


def path_test_resource() -> Path:
    return Path(__file__).parent / "testresources"
