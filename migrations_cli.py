#!/usr/bin/env python
"""
Database migration CLI tool using Flask-Migrate/Alembic.
This allows database initialization without MySQL-specific SQL files.

Usage:
    python migrations_cli.py init      # Initialize migrations directory
    python migrations_cli.py migrate   # Generate migration from models
    python migrations_cli.py upgrade   # Apply migrations to database
    python migrations_cli.py downgrade # Rollback last migration
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from flaskr import create_app, db
from flask_migrate import Migrate, init as migrate_init, migrate as migrate_migrate, upgrade as migrate_upgrade, downgrade as migrate_downgrade

def main():
    app = create_app()
    migrate = Migrate(app, db, directory='migrations')
    
    with app.app_context():
        if len(sys.argv) < 2:
            print(__doc__)
            sys.exit(1)
        
        command = sys.argv[1]
        
        if command == 'init':
            migrate_init(directory='migrations')
            print("✅ Migrations directory initialized")
        elif command == 'migrate':
            message = sys.argv[2] if len(sys.argv) > 2 else 'Auto-generated migration'
            migrate_migrate(directory='migrations', message=message)
            print("✅ Migration generated")
        elif command == 'upgrade':
            migrate_upgrade(directory='migrations')
            print("✅ Database upgraded")
        elif command == 'downgrade':
            migrate_downgrade(directory='migrations')
            print("✅ Database downgraded")
        else:
            print(f"❌ Unknown command: {command}")
            print(__doc__)
            sys.exit(1)

if __name__ == '__main__':
    main()
