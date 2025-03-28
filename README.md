# riga-public-consultation-notifier

Docker app which checks for new public consultations on the Riga municipality website and posts notifications in Slack

## Configuration

## Docker

- Install Docker and optionally Docker Compose

### Create and install a Slack app

- [Create a new app](https://api.slack.com/apps) and open its configuration
- In **OAuth & Permissions** tab, in **Scopes** section and **Bot Token Scopes** subsection, add an OAuth scopes. If you want to post to a public channel, you will need **chat:write** and **chat:write.public**
- In **OAuth & Permissions** tab, in **OAuth Tokens** section, install the app to your workspace and copy the **Bot User OAuth Token** (you will need it later)

### Database directory

- If you don't configure your own database connection, you will need to have mounted persistent storage (Docker volume or bind mount) to /app/data

### Environment variables

- Can be set in the **.env** file in the repository directory

### Secrets directory

- You need to have mounted persistent storage with secrets (see below) to **/run/secrets**. File name is secret key and file contents (leading and trailing whitespaces are ignored) are secret value

### Required environment variables

- **SLACK_CHANNEL_ID** - Slack channel ID ([how to find it](https://duckduckgo.com/?q=slack+channel+id))

### Required secrets

- **slack_bot_user_oauth_token** - Slack Bot User OAuth Token you copied earlier

### Optional environment variables

- **DATABASE_DRIVER** - [SQLAlchemy database driver](https://docs.sqlalchemy.org/en/latest/core/engines.html#backend-specific-urls). If not set, the app will create (if doesn't exist) and use the SQLite database located in **data/sqlite.db** in app directory
- **DATABASE_HOST** - database host
- **DATABASE_NAME** - database name
- **DATABASE_PORT** - database port
- **DATABASE_QUERY_STRING_PARAMETERS** - [database query string parameters](https://docs.sqlalchemy.org/en/latest/core/engines.html#add-parameters-to-the-url-query-string)
- **DATABASE_USERNAME** - database username
- **DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS** - after retrieving public consultations, delete public consultations from database if they aren't present on website for more than X days. Set to empty value to keep indefinitely. Default: 365
- **ENABLED_PUBLIC_CONSULTATION_TYPES** - comma separated list of public consultation types (leading and trailing whitespaces are ignored) to fetch. Supported types: **attistibas-planosanas-dokumenti**, **publiskas-apspriesanas** and **saistoso-noteikumu-projekti**. Default: all
- **SECRET_DIR** - secret directory. Default: **/run/secrets** in Docker and **secrets** in app directory when running locally
- **TIME_ZONE** - [time zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) in which to store timestamps in database. Default: Europe/Riga

### Optional secrets

- **database_password** - database password

### Build and run with Docker Compose

- To build and run, in the repository directory, run **docker compose up --build**
- You will want to schedule execution of **docker compose up** in your favorite task scheduler
