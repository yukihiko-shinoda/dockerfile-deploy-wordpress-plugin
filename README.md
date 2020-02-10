<!-- markdownlint-disable first-line-h1 -->
[![docker build automated?](https://img.shields.io/docker/cloud/automated/futureys/deploy-wordpress-plugin.svg)](https://hub.docker.com/r/futureys/deploy-wordpress-plugin/builds)
[![docker build passing?](https://img.shields.io/docker/cloud/build/futureys/deploy-wordpress-plugin.svg)](https://hub.docker.com/r/futureys/deploy-wordpress-plugin/builds)
[![image size and number of layers](https://images.microbadger.com/badges/image/futureys/deploy-wordpress-plugin.svg)](https://hub.docker.com/r/futureys/deploy-wordpress-plugin/dockerfile)

# Quick reference

- **operating procedure**:

  [Using Subversion | Plugin Developer Handbook | WordPress Developer Resources](https://developer.wordpress.org/plugins/wordpress-org/how-to-use-subversion/)

- **Reference materials**:

  [Plugin Readmes | Plugin Developer Handbook | WordPress Developer Resources](https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/#how-the-readme-is-parsed)

  [The Plugins directory and readme.txt files – Make WordPress Plugins](https://make.wordpress.org/plugins/2012/06/09/the-plugins-directory-and-readme-txt-files/)

<!-- markdownlint-disable no-trailing-punctuation -->
# What is Deploy WordPress Plugin?
<!-- markdownlint-enable no-trailing-punctuation -->

This is deployment job for WordPress Plugin
from public Git repository to SubVersion on WordPress.org.

## requirement

- Tagging revision on Git is done before deploy into WordPress.org
- Tag name of revision on source Git repository to deploy is the same as version number of plugin’s main PHP file on tagged revision of source Git repository

## out of scope

- Deploying old version than latest version
- [Deploying Assets](https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/)
  (Even if Git repository includes assets, this project will deploy
   the revision content as it is under trunk and tags
   of SubVersion repository on WordPress.org.)

## excluding strategy

The process executes rsync from Git working tree to SubVersion working tree with ```.rsync-filter```.

### default behavior

rsync will read [default .rsync-filter file](https://github.com/yukihiko-shinoda/dockerfile-deploy-wordpress-plugin/blob/master/runner/project/roles/deploy-wordpress-plugin/templates/.rsync-filter.j2).

### customizing behavior

If ```.rsync-filter``` file is exist on the root of Git working tree, rsync will read it. The most primitive how to write it is to list up files and directories you want to exclude. For more details, following contents will be helpful.

- [linux - Using Rsync filter to include/exclude files - Stack Overflow](https://stackoverflow.com/questions/35364075/using-rsync-filter-to-include-exclude-files)
- [rsync(1) - Linux man page](https://linux.die.net/man/1/rsync)

# How to use this image

This image is depend on [futureys/ansible-workspace-deploy-wordpress-plugin](https://hub.docker.com/r/futureys/ansible-workspace-deploy-wordpress-plugin).
It will be easier to understand
if you look at the Docker Compose files in the GitHub code.

<https://github.com/yukihiko-shinoda/dockerfile-deploy-wordpress-plugin>

## ... via docker-compose

### 1. Download project files

Clone or download project files from GitHub.

```shell script
git clone https://github.com/yukihiko-shinoda/dockerfile-deploy-wordpress-plugin.git
```

### 2. Set environment variable

If you prefer, there is template to set environment variables,
Copy .env.dist to .env, then open by editor and edit variable definitions.

ref: [Environment variables in Compose | Docker Documentation](https://docs.docker.com/compose/environment-variables/#the-env-file)

### 3. Dry run

By running SubVersion container for mock in local.
Enter following command:

```shell script
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d && docker logs -f operator
```

### 4. Check dry run result

When process succeed to finish, check result by checking out from mock:

```shell script
svn checkout svn://(your-docker-host-name)/project-in-svn
cd project-in-svn
svn log HEAD:1
```

### 5. Shutdown containers once

Once you have checked that it works as expected, shutdown containers once.

```shell script
docker-compose -f docker-compose.yml -f docker-compose.staging.yml down
```

### 6. Run as production

```shell script
docker-compose -f docker-compose.yml up --abort-on-container-exit
```

### 7. Check on WordPress.org

Check on WordPress.org that it has been deployed successfully.

[WordPress Plugins | WordPress.org](https://wordpress.org/plugins/)

### 8. Shutdown containers

After checking that the deployment was succeed, shutdown the container.

```shell script
docker-compose -f docker-compose.yml down
```

## Environment Variables

### ```GIT_REPOSITORY_URL```

The source Git repository URL for public repository.
Only either of ```GIT_REPOSITORY_URL``` or ```GIT_PATH_CHECKED_OUT``` can define.

### ```GIT_PATH_CHECKED_OUT```

The source GIT_PATH_CHECKED_OUT.
This is intended to mount the directory where checked out the private repository.
Only either of ```GIT_REPOSITORY_URL``` or ```GIT_PATH_CHECKED_OUT``` can define.

### ```SVN_REPOSITORY_URL```

The destination SubVersion repository URL.

Ex: ```https://plugins.svn.wordpress.org/????```

### ```SVN_USER_NAME```

User name of SubVersion on WordPress.org.

> Your account for SVN will be the same username (not the email) of
> the account you used when you submitted the plugin.
> This is the user ID you use for the WordPress forums as well.

### ```SVN_USER_PASSWORD```

User password of SubVersion on WordPress.org.

> If you need to reset your password, go to [login.wordpress.org](https://login.wordpress.org/)

### ```DEPLOY_VERSION```

The tag name of revision on source Git repository to deploy.
This string also has to be the same as the version number of
plugin’s main PHP file on tagged revision of source Git repository.

### ```SHOW_ALL_LOG```

By default, this image hide logs about steps using secret for example when commit.
When debug, you can check log by setting this ```true```.
