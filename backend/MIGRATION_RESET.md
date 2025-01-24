# Database Migration Reset Guide

## When to Reset Migrations

You may need to reset migrations if:
- You're starting a new project
- Migrations are in an inconsistent state
- You want to completely rebuild your database schema

## Reset Procedure

### 1. Backup Existing Data
- Export any critical database data
- Take a backup of your current database file

### 2. Delete Existing Migrations
```bash
# Remove migrations directory
rm -rf migrations/*

# Or on Windows
rmdir /s /q migrations
```

### 3. Reinitialize Migrations
```bash
# Initialize new migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

## Troubleshooting

### Common Issues
- **Alembic Version Conflicts**: Delete all files in `migrations/versions/`
- **Database Connection Problems**: Check database URI in configuration
- **Model Changes**: Ensure all model changes are reflected in your models

### Force Reset
```bash
# Completely reset database and migrations
flask db stamp head
flask db migrate
flask db upgrade
```

## Best Practices
- Always backup data before resetting
- Test migrations in a staging environment
- Use version control for migration files

## Warning
🚨 Resetting migrations will **DELETE ALL EXISTING DATABASE DATA**. 
Ensure you have backups before proceeding.
