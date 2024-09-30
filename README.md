## dotenvx

This project lets you encrypt your environment variables so that you can check in your .env file as an encrypted .env.vault.
This allows a strict separation of config from code as per "The Twelve-Factor App" [1].

Install

```
brew install dotenvx/brew/dotenvx
```

Make sure you've added your environment variables to `.env.prod` config file.

Encrypt your .env.prod in one go

```
cp .env.prod .env.vault
dotenvx encrypt -f .env.vault
```

or

```
make env
```

Set your DOTENV_PRIVATE_KEY_VAULT key on github.com so that the key can be used to decrypt your environment vars.

```
cd admin
./set_github_secret.sh
```

Note: If you use a cloud service like fly.io, make sure you set the DOTENV_PRIVATE_KEY_VAULT as a secret there too.

Learn more here
https://github.com/dotenvx/dotenvx

Now you have your encrypted environment variables in both github.com and fly.io or anywhere you roll out the codebase to. No more secrets required.

[1] https://12factor.net/config
