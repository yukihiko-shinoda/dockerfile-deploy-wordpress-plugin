import os


class Workspace:
    PATH_GIT_CHECKOUT = '/root/workdir/git-working-dir'
    PATH_SVN_CHECKOUT = '/root/workdir/my-local-dir'

    def __init__(self, host):
        self.host = host
        self.git_repository_url = os.environ['GIT_REPOSITORY_URL']
        self.svn_repository_url = os.environ['SVN_REPOSITORY_URL']
        self.staged_file = None

    def checkout_git(self, version, *, path=None):
        if path is None:
            path = self.PATH_GIT_CHECKOUT
        result = self.host.ansible(
            'git',
            ' '.join([
                f'repo={self.git_repository_url}',
                f'dest={path}',
                f'version={version}',
            ]),
            check=False
        )
        print(result)
        assert 'changed' in result, result['msg']

    def checkout_svn(self, revision, *, path=None):
        if path is None:
            path = self.PATH_SVN_CHECKOUT
        result = self.host.ansible(
            'subversion',
            ' '.join([
                f'repo={self.svn_repository_url}',
                f'dest={path}',
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

    def remove_directory_git(self):
        self.remove_file_or_directory(self.PATH_GIT_CHECKOUT)

    def remove_directory_svn(self):
        self.remove_file_or_directory(self.PATH_SVN_CHECKOUT)

    def remove_file(self, path):
        self.remove_file_or_directory(path)
        self.staged_file = None

    def remove_file_or_directory(self, path):
        result = self.host.ansible(
            'file',
            ' '.join([
                f'path={path}',
                f'state=absent',
            ]),
            check=False
        )
        assert 'changed' in result, result['msg']
