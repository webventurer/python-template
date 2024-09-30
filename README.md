## Add private repo access

Generate a classic Personal Access Token (PAT) on your account

- Go to your GitHub account settings.
- Navigate to "Developer settings" -> "Personal access tokens".
- Click "Generate new token" -> PRIVATE_REPO_ACCESS_TOKEN.
- Select the necessary scope "repo" for repository access.
- Generate the token and copy it.

Set the `PRIVATE_REPO_ACCESS_TOKEN` on GitHub.com:

```
gh secret set PRIVATE_REPO_ACCESS_TOKEN
```

Now you can add a private repo to your requirements.in like this:

```
git+https://github.com/account/repo.git
```
