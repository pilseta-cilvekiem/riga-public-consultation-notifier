# riga-public-consultation-notifier

Docker app which checks for new public consultations on the Riga municipality website and posts notifications in Slack

## Installation and configuration

## Docker

- Install Docker and optionally Docker Compose

### Create and install a Slack app

- [Create a new app](https://api.slack.com/apps) and open its configuration
- In **OAuth & Permissions** tab, in **Scopes** section and **Bot Token Scopes** subsection, add an OAuth scopes. If you want to post to a public channel, you will need **chat:write** and **chat:write.public**
- In **OAuth & Permissions** tab, in **OAuth Tokens** section, install the app to your workspace and copy the **Bot User OAuth Token** (you will need it later)

### Database directory

- If you don't configure your own database connection, you will need to have mounted persistent storage (Docker volume or bind mount) to /app/data

### Build arguments

- **EXTRA_PIP_INSTALL_ARGS** - provide list of additional PyPI packages to install to support databases other than SQLite.

### Environment variables

- Can be set in the **.env** file in the repository directory

#### Required

- **SLACK_BOT_USER_OAUTH_TOKEN_FILE** - Slack Bot User OAuth Token file path with token you copied earlier
- **SLACK_CHANNEL_ID** - Slack channel ID ([how to find it](https://duckduckgo.com/?q=slack+channel+id))

#### Optional

- **DATABASE_DRIVER** - [SQLAlchemy database driver](https://docs.sqlalchemy.org/en/latest/core/engines.html#backend-specific-urls). If not set, the app will create (if doesn't exist) and use the SQLite database located in **data/sqlite.db** in app directory
- **DATABASE_HOST** - database host
- **DATABASE_NAME** - database name
- **DATABASE_PASSWORD_FILE** - database password file path
- **DATABASE_PORT** - database port
- **DATABASE_QUERY_STRING_PARAMETERS** - [database query string parameters](https://docs.sqlalchemy.org/en/latest/core/engines.html#add-parameters-to-the-url-query-string)
- **DATABASE_USERNAME** - database username
- **DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS** - after retrieving public consultations, delete public consultations from database if they aren't present on website for more than X days. Set to empty value to keep indefinitely. Default: 365
- **ENABLED_PUBLIC_CONSULTATION_TYPES** - comma separated list of public consultation types (leading and trailing whitespaces are ignored) to fetch. Supported types: **attistibas-planosanas-dokumenti**, **publiskas-apspriesanas** and **saistoso-noteikumu-projekti**. Default: all
- **TIME_ZONE** - [time zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) in which to store timestamps in database. Default: Europe/Riga

### Build and run with Docker Compose

- To build and run, in the repository directory, run **docker compose up --build**
- You will want to schedule execution of **docker compose up** in your favorite task scheduler
