# NOTE: Only run this script once

import os

folders = [
    "fastapi_app",
    "database",
    "sanctions",
    "sanctions/models",
    "sanctions/routes",
    "sanctions/schemas",
    "models",
    "schemas"
]

files = [
    "fastapi_app/main.py",
    "database/base.py",
    "database/database.py",
    "database/__init__.py",
    "sanctions/models/__init__.py",
    "sanctions/models/sanction.py",
    "sanctions/routes/__init__.py",
    "sanctions/routes/sanction.py",
    "sanctions/schemas/__init__.py",
    "sanctions/schemas/sanction.py",
    "models/__init__.py",
    "schemas/sanction.py"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, "w") as f:
        pass
