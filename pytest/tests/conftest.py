import os
import shutil

import pytest


@pytest.fixture
def environment_variable():
    dest_playbook = '/runner/project/playbook_test.yml'
    dest_role = '/runner/project/roles/test'
    shutil.copy('testresources/project/playbook_test.yml', dest_playbook)
    shutil.copytree('testresources/project/roles/test', dest_role)
    yield
    os.remove(dest_playbook)
    shutil.rmtree(dest_role)
