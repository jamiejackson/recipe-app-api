# pgAdmin Setup for Recipe App API

## pgAdmin Login Bypass

pgAdmin is configured to bypass the web login screen. This is achieved by setting the following environment variables in the `docker-compose.yml` for the `pgadmin` service:

- `PGADMIN_DEFAULT_EMAIL`: Sets the default admin email (e.g., `admin@admin.com`).
- `PGADMIN_DEFAULT_PASSWORD`: Sets the default admin password (e.g., `admin`).
- `PGADMIN_CONFIG_SERVER_MODE: 'False'`: Enables DESKTOP mode, which disables multi-user login and always logs in as the default user.
- `PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: 'False'`: Disables the master password prompt.

With these settings, you will be automatically logged in to pgAdmin when you access the web UI at `http://localhost:5050`.

## Why Bypassing Database Password Entry Is Hard

There are no known, documented ways to fully bypass the database connection password prompt in pgAdmin. This is a deliberate security feature.

Bypassing the database connection password prompt in pgAdmin is difficult because:
- pgAdmin stores server connection info (including passwords) in its internal SQLite database (`pgadmin4.db`), which is created on first run.
- Importing server definitions from `servers.json` only works on the very first run, and does not import passwords unless the file is encrypted and matches the internal user/master password setup.
- If the internal database already exists, pgAdmin ignores `servers.json`.
- Passwords for server connections are encrypted and tied to the master password/user credentials.

### Workarounds Attempted
- **Custom entrypoint script:** Tried deleting `/var/lib/pgadmin` to force a fresh import from `servers.json` on every start. This led to permission issues and was not robust.
- **Direct SQLite manipulation:** Attempted to update the password in `pgadmin4.db` via `sqlite3` after startup. This is fragile, not recommended, and ultimately doesn't work, anyway.
- **Custom build and scripting:** Created custom Dockerfile and entrypoint scripts to automate import and password setup, but these approaches were unreliable and complicated.


### Conclusion
- The only reliable automation is bypassing the pgAdmin web login.
- Database server connections must be added manually in the UI, or you must use a persistent volume and set up connections once.
- Automating server password entry is not supported by pgAdmin's import process and is intentionally restricted for security reasons.

#### Note on Persisting pgAdmin Data
You could persist the pgAdmin data directory (e.g., `/var/lib/pgadmin`) using a Docker volume. This would retain manual server configurations and passwords across container restarts. However, for this project, we prefer to keep things clean and rely on configuration-as-code (such as environment variables and `servers.json`) rather than persisting manual configurations. This approach makes the setup reproducible and avoids hidden state. Persisting pgAdmin data may be considered in the future if a compelling reason arises (such as complex, non-reproducible manual setupsm or causes undue friction/reduced productivity).

---
For most users, the current setup (automatic web login, manual server connection) is the simplest and most reliable approach.

## Reference
- [pgAdmin prompts for password despite correctly configured pgpass file](https://stackoverflow.com/questions/78965895/pgadmin-prompts-for-password-despite-correctly-configured-pgpass-file)
