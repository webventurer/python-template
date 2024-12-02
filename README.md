# Python Project Template

You can use this repository as a template when creating a new repository on GitHub, to get my preferred setup for a Python project.

After creating the new project, there are a few things you'll need to configure.

## Install brew (if you haven't already)

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Or install using the .pkg installer from [here](https://github.com/Homebrew/brew/releases/).

[1] https://brew.sh

## Install direnv

Load/unload environment variables from your .envrc. In this case we use it to set the $PYTHONPATH without resorting to sys.path.insert hacks.

```sh
brew install direnv
```

[1] https://formulae.brew.sh/formula/direnv

## Rename the main package

You'll need to rename the package from "mylib" to something sensible:

```sh
git mv mylib newname
sed -i '' -e 's/mylib/newname/' tests/* .projections.json .github/workflows/python-app.yml .envrc pyproject.toml pyrightconfig.json
```

## Choosing the Python version

The version of Python that your project uses is needed by the GitHub Action that runs the tests, and perhaps by your local Python installation tool.

You can create it like this:

```sh
echo 3.12.6 > .python-version
```

## Reviewing the license

The open source MIT license is used by default (see the `LICENSE` file). [Is it appropriate](https://choosealicense.com/) for this project?

If it is, don't forget to set the year and the name of the copyright holder:

```sh
sed -i '' -e "s,<YEAR>,$(date +%Y)," LICENSE
FULL_NAME="$(getent passwd $USER | cut -d : -f 5 | cut -d , -f 1)"
sed -i '' -e "s,<COPYRIGHT HOLDER>,$FULL_NAME," LICENSE
```

If you're on OS X use:

```sh
FULL_NAME="$(bin/osx/getent-passwd.sh $USER | cut -d : -f 5 | cut -d , -f 1)"
```

## Install packages

You need to get everything installed, and that first test running. Start by creating a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Now we can install our development tools:

```sh
pip install --upgrade pip
pip install pip-tools
make install
```

As you add new development or production dependencies (or both), you can run this command to install them:

```sh
make update
```

## Run a linter & format your code on check in

Ruff is a standalone package which runs a linter and a formatter over your code, replacing the need for Black, isort or flake8. Althoug you can add the Ruff extension to your VSCode (editor), you can also add it to your .pre-commit-config.yaml to check your code on a git commit.

```sh
pre-commit install
```

## VS Code plugins

Make sure you install

- ruff
- pylance

Note: Pylance incorporates the Pyright type checker so you only need to install Pylance. When Pylance is installed, the Pyright extension will disable itself.

## VIM plugins

The .projections.json is config for Vim projectionist plugin [1].

This config makes it easy to switch between "alternate" files in the Vim
editor; you can easily jump between a Python module and its test file.

[1] https://github.com/tpope/vim-projectionist.

## Deploy project to fly.io via Docker

This commit helps you roll out your app to fly.io. We've added in some additional features like:

- Ability to add 'thirdparty' pip modules inside the repo.
- Use of Nginx to switch between multiple apps (& servers).

It's easy to strip out these extra features if they're not needed.

Note: We've only included `dotenvx` command/s that relate to fly.io deployment. The rest of the `dotenvx` installation notes can be found in the `dotenvx` Git branch.

### Allow GitHub.com to speak to fly.io

Create a FLY_API_TOKEN:

`fly tokens create deploy -x 999999h`

Add this token to GitHub settings of your repository as a new secret called FLY_API_TOKEN.

Check the token is on GitHub:

`gh secret list`

### Add DOTENV_PRIVATE_KEY_VAULT secret to GitHub.com & fly.io

Once `dotenv` is setup, you'll need this private env variable to decrypt the env variables in .env.vault:

You can set the token programatically on GitHub.com like this:

`admin/set_github_secret.sh`

You can set the token on fly.io like this:

`flyctl secrets set DOTENV_PRIVATE_KEY_VAULT=your_private_key`

You only need this one secret. All the rest of the encrypted environment variables will now be decrypted using `dotenvx`.

### Use PYTHONPATH in Dockerfile

Although .envrc is useful for your dev box we don't need it inside the Docker container. You can set the PYTHONPATH in your Dockerfile.

### Use 'thirdparty' directory for modules you have imported

Sometimes a module stops being developed. In which case you need to download the latest working copy and add it to your 'thirdparty' directory. You can then access that directory from the Makefile to install/uninstall the modules from inside your app.

This is especially useful if you need to make changes to the apps to get them working with updates to later versions of Python.

### Custom domain

Go to your DNS e.g. Amazon Route 53 and add a CNAME entry as per [1].
Point your CNAME record from your `subdomain.website.com` (or `website.com`) to `yourapp.fly.dev` with a TTL 600.

[1] https://fly.io/docs/networking/custom-domain/

### Check DNS propagation

Flush your DNS on your Mac with:

`sudo killall -HUP mDNSResponder`

Check propagration around the world with https://whatsmydns.net.

whatsmydns.net lets you instantly perform a DNS lookup to check a domain name's current IP address and DNS record information against multiple nameservers located in different parts of the world.

### A note on Nginx

If you have multiple apps on different ports you can use Nginx as a reverse proxy to switch between them. Define the routes in your nginx.conf. Or strip out all the Nginx config out if you don't need it.

## Update the README

Now delete all the docs that you've just followed, and write something suitable for your new project!
