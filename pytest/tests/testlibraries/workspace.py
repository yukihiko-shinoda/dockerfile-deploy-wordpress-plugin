import os


class Workspace:
    def __init__(self, host):
        self.host = host
        self.svn_repository_url = os.environ['SVN_REPOSITORY_URL']
        self.staged_file = None

    def checkout_svn(self, revision):
        result = self.host.ansible(
            'subversion',
            ' '.join([
                f'repo={self.svn_repository_url}',
                'dest=/root/workdir/project-in-svn',
                f'revision={revision}',
            ]),
            check=False
        )
        print(result)
        assert 'changed' in result and result['changed'], result['msg']

    def file_exists(self, path):
        result = self.host.ansible(
                'stat',
                f'path={path}'
        )
        print(result['stat']['exists'])
        return result['stat']['exists']

    def check_line_in_file(self, name, line):
        result = self.host.ansible(
            'lineinfile',
            ' '.join([
                f'name={name}',
                f'line={line}',
            ])
        )
        print(result)
        return result['changed']

    def stage_file(self, src, dest):
        result = self.host.ansible(
            'copy',
            ' '.join([
                f'src={src}',
                f'dest={dest}',
            ]),
            check=False
        )
        print(result)
        assert 'changed' in result, result['msg']
        self.staged_file = dest
