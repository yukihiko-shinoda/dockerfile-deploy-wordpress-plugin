# Quick reference

- **operating procedure**:

  [Using Subversion | Plugin Developer Handbook | WordPress Developer Resources](https://developer.wordpress.org/plugins/wordpress-org/how-to-use-subversion/)

- **Reference materials**:

  [Plugin Readmes | Plugin Developer Handbook | WordPress Developer Resources](https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/#how-the-readme-is-parsed)
  [The Plugins directory and readme.txt files – Make WordPress Plugins](https://make.wordpress.org/plugins/2012/06/09/the-plugins-directory-and-readme-txt-files/)

# What is Deploy WordPress Plugin?

This is deployment job for WordPress Plugin
from public Git repository to SubVersion on WordPress.org.

## requirement

- Source Git repository is public
- Tagging revision on Git is done before deploy into WordPress.org
- Tag name of revision on source Git repository to deploy is the same as version number of plugin’s main PHP file on tagged revision of source Git repository

## out of scope

- Deploying old version than latest version
- [Deploying Assets](https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/)
  (Even if Git repository includes assets, this project will deploy
   the revision content as it is under trunk and tags
   of SubVersion repository on WordPress.org.)

# How to use this image

This image is depend on [futureys/ansible-workspace-deploy-wordpress-plugin](https://hub.docker.com/r/futureys/ansible-workspace-deploy-wordpress-plugin).
It will be easier to understand
if you look at the Docker Compose files in the GitHub code.

https://github.com/yukihiko-shinoda/dockerfile-deploy-wordpress-plugin

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

### ```ANSIBLE_SSH_HOST```

Host name to ssh connect by Ansible.

### ```ANSIBLE_SSH_USER```

Host name to ssh user name by Ansible.

### ```ANSIBLE_SSH_PASS```

Host name to ssh user password by Ansible.

### ```ANSIBLE_PYTHON_INTERPRETER```

Path to Python interpreter on **host side** which Ansible use.

### ```GIT_REPOSITORY_URL```

The source Git repository URL.

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