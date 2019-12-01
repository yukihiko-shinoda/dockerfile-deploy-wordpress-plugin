FROM futureys/ansible-runner-python3:20191127153000 as production
COPY runner /runner
ENV RUNNER_PLAYBOOK=playbook.yml \
    ANSIBLE_FORCE_COLOR='True'

FROM production as test
WORKDIR /root/pytest
COPY pytest/Pipfile pytest/Pipfile.lock /root/pytest/
# @see https://github.com/pypa/pipenv/issues/451#issuecomment-366155882
ENV PIP_NO_CACHE_DIR false
# @see https://pipenv-fork.readthedocs.io/en/latest/advanced.html#using-pipenv-for-deployments
RUN python3 -m pipenv install --dev --deploy
CMD ["pipenv", "run", "test"]
