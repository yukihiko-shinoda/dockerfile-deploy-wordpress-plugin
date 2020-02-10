#!/usr/bin/env sh
set -eu
if [ "${SVN_USER_NAME:-}" != '' ] && [ "${SVN_USER_PASS:-}" != '' ]; then
  # shellcheck disable=SC2093
  init-svn-repository
fi
exec entrypoint-ansible-runner "${@}"
