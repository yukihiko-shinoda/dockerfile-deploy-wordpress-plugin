#!/usr/bin/env sh
set -eu
# shellcheck disable=SC2093
init-svn-repository
exec entrypoint-ansible-runner "${@}"
