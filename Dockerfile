FROM ghcr.io/astral-sh/uv:0.9.5 AS uv
FROM quay.io/ansible/ansible-runner:stable-2.12-latest AS production
# - Could not resolve host: mirrorlist.centos.org; Unknown error #Docker - Qiita
#   https://qiita.com/vossibop/items/d4fc4c94e5b7714e3a8c
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* && \
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-* && \
    dnf -y update && dnf clean all && \
    dnf install -y \
    # Since this GitHub Action commit WordPress plugin into SVN in WordPress.org.
    subversion-1.10.2 \
    # Python 3.10: Since Ansible 7.0.0 doesn't support python3.8 that is default python version in this image.
    wget yum-utils make gcc openssl-devel bzip2-devel libffi-devel zlib-devel \
    # git (This image already be installed 2.31.1): Since this GitHub Action checks out WordPress plugin from GitHub.
 && dnf clean all
# Python 3.13: Since Ansible 7.0.0 doesn't support python3.8 that is default python version in this image.
WORKDIR /root/pytest
# - Using uv in Docker | uv
#   https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=uv /uv /uvx /bin/
# - Using uv in Docker | uv
#   https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy
# To simulate Python system installation:
# - Installing a package | Using uv in Docker | uv
#   https://docs.astral.sh/uv/guides/integration/docker/#installing-a-package
RUN uv venv /opt/venv
# Use the virtual environment automatically
ENV VIRTUAL_ENV=/opt/venv
# Place entry points in the environment at the front of the path
ENV PATH="/opt/venv/bin:$PATH"
# Official documentation lacks this setting, otherwise, installed binary isn't prioritized than /usr/local/bin/
ENV UV_PROJECT_ENVIRONMENT=/opt/venv/
# RUN uv python install 3.13 --default
COPY pytest/pyproject.toml pytest/uv.lock /root/pytest/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --python 3.13
WORKDIR /runner
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
# To create .venv in project directory to refer installed package's codes in development
ENV VIRTUAL_ENV= \
    UV_PROJECT_ENVIRONMENT=
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
CMD ["uv", "run", "invoke", "test"]
