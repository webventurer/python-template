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
