FROM quay.io/ansible/ansible-runner:stable-2.12-latest AS production
# - Could not resolve host: mirrorlist.centos.org; Unknown error #Docker - Qiita
#   https://qiita.com/vossibop/items/d4fc4c94e5b7714e3a8c
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* && \
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-* && \
    dnf -y update && dnf clean all && \
    dnf install -y \
    # Since this GitHub Action commit WordPress plugin into SVN in WordPress.org.
    subversion-1.10.2 \
    # Since Ansible 7.0.0 doesn't support python3.8 that is default python version in this image.
    python39-3.9.19 \
    # git (This image already be installed 2.31.1): Since this GitHub Action checks out WordPress plugin from GitHub.
 && dnf clean all
COPY runner /runner
ENV RUNNER_PLAYBOOK=playbook.yml \
    ANSIBLE_FORCE_COLOR='True'
ADD https://raw.githubusercontent.com/yukihiko-shinoda/shell-script-init-svn-repository/023f2917eb4f8a768092f0cd0ca764df06deb215/init-svn-repository.sh /bin/init-svn-repository
RUN mv /bin/entrypoint /bin/entrypoint-ansible-runner
COPY ./entrypoint.sh /bin/entrypoint
RUN chmod +x /bin/init-svn-repository /bin/entrypoint \
 && mkdir --parents /var/opt/svn \
 && chmod 0755 /var/opt/svn /var/opt /var

FROM production AS test
WORKDIR /root/pytest
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip --no-cache-dir install pipenv==2022.8.19
COPY pytest/Pipfile pytest/Pipfile.lock /root/pytest/
RUN pipenv install --dev --deploy
CMD ["pipenv", "run", "invoke", "test"]
