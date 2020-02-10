FROM futureys/ansible-runner-python3:20191127153000 as production
RUN yum -y install  https://centos7.iuscommunity.org/ius-release.rpm && \
    yum install -y git2u subversion && yum clean all
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
COPY pytest/Pipfile pytest/Pipfile.lock /root/pytest/
# @see https://github.com/pypa/pipenv/issues/451#issuecomment-366155882
ENV PIP_NO_CACHE_DIR false
# @see https://pipenv-fork.readthedocs.io/en/latest/advanced.html#using-pipenv-for-deployments
RUN python3 -m pipenv install --dev --deploy
CMD ["pipenv", "run", "test"]
