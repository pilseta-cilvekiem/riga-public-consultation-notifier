# Riga Public Consultation Notifier

Docker app written in Python which checks for new public consultations on the Riga municipality website and posts notifications in Slack.

## Set up development environment

1. [VS Code](https://code.visualstudio.com/) with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
1. Clone this repository. On Windows, press Ctrl+Shift+P and choose **WSL: Connect to WSL** to clone inside the Windows Subsystem for Linux first.
1. Open the repository folder in VS Code, then press Ctrl+Shift+P and choose **Dev Containers: Reopen in Container**.
1. Once the container is running, open a terminal and run the app with `run.bash`. The script will prompt you for any missing configuration values on first run.
1. After that you can also launch app via the Run menu.

## Installation and configuration

## Docker

Install Docker/Podman and optionally Docker Compose/Podman Compose.

### Create and install a Slack app

1. [Create a new app](https://api.slack.com/apps) and open its configuration.
1. In **OAuth & Permissions** tab, in **Scopes** section and **Bot Token Scopes** subsection, add an OAuth scopes. If you want to post to a public channel, you will need **chat:write** and **chat:write.public**.
1. In **App Home** tab, in **Your App’s Presence in Slack** section, click **Edit**, fill both **Display Name (Bot Name)** and **Default username** and click **Save**.
1. In **Install App** tab, in **OAuth Tokens** section, install the app to your workspace and note the **Bot User OAuth Token** (you will need it later).

### Database directory

If you don't configure your own database connection, you will need to have mounted persistent storage (Docker volume or bind mount) to /app/data. Storage is needed to prevent duplicate notifications.

### Build arguments

**EXTRA_PIP_INSTALL_ARGS** - provide list of additional PyPI packages to install to support databases other than SQLite.

### Environment variables

Can be set in the **.env** file in the repository directory. When running via **scripts/run.bash**, missing required values are prompted for interactively and saved to **.env** automatically.

#### Required

- **SLACK_BOT_USER_OAUTH_TOKEN_FILE** - path to a file containing the Slack Bot User OAuth Token. Defaults to **secrets/slack_bot_user_oauth_token** in the repository directory. If the file does not exist, the script will prompt for the token and create the file.
- **SLACK_CHANNEL_ID** - Slack channel ID ([how to find it](https://duckduckgo.com/?q=slack+channel+id)). The script will prompt for this value if it is not set.

#### Optional

- **DATABASE_DRIVER** - [SQLAlchemy database driver](https://docs.sqlalchemy.org/en/latest/core/engines.html#backend-specific-urls). If not set, the app will create (if doesn't exist) and use the SQLite database located in **data/sqlite.db** in app directory.
- **DATABASE_HOST** - database host.
- **DATABASE_NAME** - database name.
- **DATABASE_PASSWORD_FILE** - database password file path.
- **DATABASE_PORT** - database port.
- **DATABASE_QUERY_STRING_PARAMETERS** - [database query string parameters](https://docs.sqlalchemy.org/en/latest/core/engines.html#add-parameters-to-the-url-query-string).
- **DATABASE_USERNAME** - database username.
- **DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS** - after retrieving public consultations, delete public consultations from database if they aren't present on website for more than X days. Set to empty value to keep indefinitely. Default: 365.
- **ENABLED_PUBLIC_CONSULTATION_TYPES** - comma separated list of public consultation types (leading and trailing whitespaces are ignored) to fetch. Supported types: **attistibas-planosanas-dokumenti**, **publiskas-apspriesanas** and **saistoso-noteikumu-projekti**. Default: all.

### Build and run with Docker Compose

- To build and run, in the repository directory, run **docker compose up --build**.
- You will want to schedule execution of **docker compose up** in your favorite task scheduler.
