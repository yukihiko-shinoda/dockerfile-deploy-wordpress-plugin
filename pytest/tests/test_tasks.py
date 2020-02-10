import ansible_runner
import pytest

from tests.testlibraries.event_analyzer import EventAnalyzer


class TestTasks:
    @pytest.mark.parametrize('src, dest, regex, arrow_no_lines, expect', [
        ['readme-example.txt', '/tmp/readme-example.txt', r'[ \t\/*#@]*Stable\stag:.*$', True, '4.3'],
        ['plugin-main-example-1.php', '/tmp/plugin-main-example-1.php', r'[ \t\/*#@]*Version:.*$', True, '1.10.3'],
        ['plugin-main-example-2.php', '/tmp/plugin-main-example-2.php', r'[ \t\/*#@]*Version:.*$', True, '1.0.0'],
        ['plugin-main-example-3.php', '/tmp/plugin-main-example-3.php', r'[ \t\/*#@]*Version:.*$', True, '1.10.4'],
    ])
    def test_grep_plugin_data(
        self, git_repository_url, clear_artifacts, playbook_tasks, fixture_file, regex, arrow_no_lines, expect
    ):
        # @see https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/#example-readme
        # @see https://developer.wordpress.org/plugins/plugin-basics/header-requirements/#header-fields
        result_debug = self.run_include_task(
            'roles/checkout/tasks/grep_plugin_data.yml', 
            list_debug_variable=['result_grep'],
            vars={
                'path_to_file': fixture_file,
                'regex': regex,
                'arrow_no_lines': arrow_no_lines,
            }
        )
        assert result_debug['result_grep']['stdout'] == expect

    def run_include_task(self, task_file_name, *, list_debug_variable=None, vars=None):
        extra_vars = {'task_file_name': task_file_name}
        if list_debug_variable is not None:
            extra_vars['list_debug_variable'] = list_debug_variable
        if vars is not None:
            extra_vars.update(vars)
        runner = ansible_runner.run(
            private_data_dir='/runner',
            playbook='playbook_tasks.yml',
            extravars=extra_vars
        )
        assert runner.status == 'successful'
        assert runner.rc == 0
        responce = EventAnalyzer.get_response(runner.events)
        return EventAnalyzer.extract_result_debug(responce, list_debug_variable)
