import ansible_runner
import pytest


class TestTasks:
    @pytest.mark.parametrize('src, dest, regex, arrow_no_lines, expect', [
        ['readme-example.txt', '/tmp/readme-example.txt', r'[ \t\/*#@]*Stable\stag:.*$', True, '4.3'],
        ['plugin-main-example-1.php', '/tmp/plugin-main-example-1.php', r'[ \t\/*#@]*Version:.*$', True, '1.10.3'],
        ['plugin-main-example-2.php', '/tmp/plugin-main-example-2.php', r'[ \t\/*#@]*Version:.*$', True, '1.0.0'],
        ['plugin-main-example-3.php', '/tmp/plugin-main-example-3.php', r'[ \t\/*#@]*Version:.*$', True, '1.10.4'],
    ])
    def test_grep_plugin_data(
        self, clear_artifacts, playbook_tasks, file_staged_workspace, regex, arrow_no_lines, expect
    ):
        # @see https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/#example-readme
        # @see https://developer.wordpress.org/plugins/plugin-basics/header-requirements/#header-fields
        runner = ansible_runner.run(
            private_data_dir='/runner',
            playbook='playbook_tasks.yml',
            extravars={
                'task_file_name': 'roles/deploy-wordpress-plugin/tasks/grep_plugin_data.yml',
                'path_to_file': file_staged_workspace.staged_file,
                'regex': regex,
                'arrow_no_lines': arrow_no_lines,
            },
            verbosity=0)
        assert runner.status == 'successful'
        assert runner.rc == 0
        for event in runner.events:
            if event['event'] == 'runner_on_ok' and event['event_data']['task_action'] == 'debug':
                responce = event['event_data']['res']
                break
        assert responce['result_grep']['stdout'] == expect
