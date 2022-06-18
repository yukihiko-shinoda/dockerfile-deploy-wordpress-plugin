from pathlib import Path
from typing import Any, Dict, List, Optional

import ansible_runner

import pytest
from tests.testlibraries.event_analyzer import EventAnalyzer


class TestTasks:
    @pytest.mark.usefixtures("git_repository_url", "clear_artifacts", "playbook_tasks")
    @pytest.mark.parametrize(
        "src, dest, regex, arrow_no_lines, expect",
        [
            ["readme-example.txt", "/tmp/readme-example.txt", r"[ \t\/*#@]*Stable\stag:.*$", True, "4.3"],
            ["plugin-main-example-1.php", "/tmp/plugin-main-example-1.php", r"[ \t\/*#@]*Version:.*$", True, "1.10.3"],
            ["plugin-main-example-2.php", "/tmp/plugin-main-example-2.php", r"[ \t\/*#@]*Version:.*$", True, "1.0.0"],
            ["plugin-main-example-3.php", "/tmp/plugin-main-example-3.php", r"[ \t\/*#@]*Version:.*$", True, "1.10.4"],
        ],
    )
    def test_grep_plugin_data(self, fixture_file: Path, regex: str, arrow_no_lines: bool, expect: str) -> None:
        # @see https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/#example-readme
        # @see https://developer.wordpress.org/plugins/plugin-basics/header-requirements/#header-fields
        result_debug = self.run_include_task(
            "roles/checkout/tasks/grep_plugin_data.yml",
            list_debug_variable=["result_grep"],
            ansible_vars={"path_to_file": fixture_file, "regex": regex, "arrow_no_lines": arrow_no_lines},
        )
        assert result_debug["result_grep"]["stdout"] == expect

    def run_include_task(
        self,
        task_file_name: str,
        *,
        list_debug_variable: Optional[List[str]] = None,
        ansible_vars: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        list_debug_variable = [] if not list_debug_variable else list_debug_variable
        extra_vars: Dict[str, Any] = {"task_file_name": task_file_name}
        extra_vars["list_debug_variable"] = list_debug_variable
        if ansible_vars is not None:
            extra_vars.update(ansible_vars)
        runner = ansible_runner.run(private_data_dir="/runner", playbook="playbook_tasks.yml", extravars=extra_vars)
        assert runner.status == "successful"
        assert runner.rc == 0
        response = EventAnalyzer.get_response(runner.events)
        return EventAnalyzer.extract_result_debug(response, list_debug_variable)
