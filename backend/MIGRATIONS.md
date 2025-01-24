# Database Migrations Guide for Coinage Backend

## Prerequisites
- Python 3.8+
- Virtual Environment activated
- All dependencies installed

## Initial Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Migrations
```bash
# Windows
python -m flask db init

# macOS/Linux
flask db init
```

### 3. Create Migration
```bash
# Windows
python -m flask db migrate -m "Initial migration"

# macOS/Linux
flask db migrate -m "Initial migration"
```

### 4. Apply Migration
```bash
# Windows
python -m flask db upgrade

# macOS/Linux
flask db upgrade
```

## Common Migration Commands

- `flask db migrate`: Create a new migration
- `flask db upgrade`: Apply all migrations
- `flask db downgrade`: Revert last migration
- `flask db history`: Show migration history

## Troubleshooting

### Migration Conflicts
If you encounter migration conflicts:
1. Delete all files in the `migrations/versions/` directory
2. Re-run `flask db init`
3. Create a new migration

### Database Reset
To completely reset the database:
```bash
# Delete existing database
del coinage.db  # Windows
rm coinage.db   # macOS/Linux

# Re-initialize
flask db init
flask db migrate
flask db upgrade
```

## Best Practices
- Always commit your migration files to version control
- Test migrations in a staging environment first
- Keep migrations small and focused
