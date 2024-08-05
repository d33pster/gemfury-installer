# Overview

`furypie` lets u download your private python packages from [`Gemfury`](https://manage.fury.io/dashboard) securely.

> Requirements: You need to create a Deploy Token from your tokens tab in GemFury website.

## Steps

> Install `furypie`

```bash
pip install furypie
```

> Install your packages

```bash
furypie --install <package-name>
# or furypie -i <package-name>
```

### `Important Notes to consider.`

1. First time setup will ask for your deploy token generated from gemfury website and your gemfury username.

2. You need to choose a password to encrypt these credentials and enter it when prompted to do so.

3. `furypie` in no way saves your password which makes it safe.

4. `furypie` will only install python packages that are uploaded in your gemfury packages.