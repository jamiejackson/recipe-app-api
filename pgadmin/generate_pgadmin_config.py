import os
import json
import pathlib


# Get environment variables
host = os.environ.get('DB_HOST', 'db')
port = os.environ.get('PGADMIN_DB_PORT', '5432')
db = os.environ.get('POSTGRES_DB', 'db')
user = os.environ.get('POSTGRES_USER', 'user')
password = os.environ.get('POSTGRES_PASSWORD', 'pass')
email = os.environ.get('PGADMIN_DEFAULT_EMAIL', 'admin@example.com')
passfile_path = "/var/lib/pgadmin/servers.pass"


# Generate servers.json
servers = {
    "Servers": {
        "1": {
            "Name": "Recipe DB",
            "Group": "Servers",
            "Host": host,
            "Port": int(port),
            "Username": user,
            "PassFile": passfile_path,
            "SSLMode": "prefer",
            "MaintenanceDB": db
        }
    }
}
with open("/tmp/servers.json", "w") as f:
    json.dump(servers, f, indent=4)


# Build the pass file in passfile_path
passfile_content = f"*:{port}:{db}:{user}:{password}\n"
with open(passfile_path, "w") as pf:
    pf.write(passfile_content)
os.chmod(passfile_path, 0o600)
