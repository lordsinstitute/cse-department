# VERY IMPORTANT — import models FIRST

import app.models  # if you have __init__.py that imports all models

from app.database import init_db

print("Initializing database...")
init_db()
print("Database initialized successfully!")