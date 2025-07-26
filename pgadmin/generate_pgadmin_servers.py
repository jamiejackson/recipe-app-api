import os
import json

servers = {
    "Servers": {
        "1": {
            "Name": "Recipe DB",
            "Group": "Servers",
            "Host": os.getenv("DB_HOST", "db"),
            "Port": 5432,
            "Username": os.getenv("POSTGRES_USER", "user"),
            "Password": os.getenv("POSTGRES_PASSWORD", "pass"),
            "SSLMode": "prefer",
            "MaintenanceDB": os.getenv("POSTGRES_DB", "db")
        }
    }
}

with open("/tmp/servers.json", "w") as f:
    json.dump(servers, f, indent=4)
