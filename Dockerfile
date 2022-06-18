FROM quay.io/ansible/ansible-runner:stable-2.12-latest as production
# git (This image already be installed 2.31.1): Since this GitHub Action checks out WordPress plugin from GitHub.
# subversion                                  : Since this GitHub Action commit WordPress plugin into SVN in WordPress.org.
RUN dnf install -y subversion && dnf clean all
COPY runner /runner
ENV RUNNER_PLAYBOOK=playbook.yml \
    ANSIBLE_FORCE_COLOR='True'
ADD https://raw.githubusercontent.com/yukihiko-shinoda/shell-script-init-svn-repository/023f2917eb4f8a768092f0cd0ca764df06deb215/init-svn-repository.sh /bin/init-svn-repository
RUN mv /bin/entrypoint /bin/entrypoint-ansible-runner
COPY ./entrypoint.sh /bin/entrypoint
RUN chmod +x /bin/init-svn-repository /bin/entrypoint
RUN mkdir --parents --mode=755 /var/opt/svn

FROM production as test
WORKDIR /root/pytest
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip --no-cache-dir install pipenv
COPY pytest/Pipfile pytest/Pipfile.lock /root/pytest/
RUN pipenv install --dev --deploy
CMD ["pipenv", "run", "invoke", "test"]
