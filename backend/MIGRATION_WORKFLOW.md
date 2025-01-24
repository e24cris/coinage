# Database Migration Workflow

## Prerequisites
- Python 3.8+
- Virtual Environment activated
- Flask-Migrate installed

## Migration Commands

### 1. Initialize Migrations
```bash
# Initialize migration repository
python flask_migrate_manager.py init
```

### 2. Create Migration Script
```bash
# Generate migration script based on model changes
python flask_migrate_manager.py migrate
```

### 3. Apply Migrations
```bash
# Upgrade database to latest schema
python flask_migrate_manager.py upgrade
```

## Workflow Scenarios

### Adding New Model
1. Update model in `app/models/`
2. Create migration script
   ```bash
   python flask_migrate_manager.py migrate
   ```
3. Apply changes
   ```bash
   python flask_migrate_manager.py upgrade
   ```

### Reverting Changes
```bash
# Downgrade to previous migration
flask db downgrade
```

## Troubleshooting

### Common Issues
- **No migrations found**: 
  - Ensure models are imported
  - Check database connection
  - Verify Flask-Migrate setup

- **Migration conflicts**:
  - Delete existing migrations
  - Reinitialize migration repository

### Reset Migration (Caution!)
```bash
# Remove existing migrations
rm -rf migrations/*

# Reinitialize
python flask_migrate_manager.py init
python flask_migrate_manager.py migrate
python flask_migrate_manager.py upgrade
```

## Best Practices
- Always backup database before migrations
- Test migrations in staging environment
- Use version control for migration files

## Advanced Techniques
- Manual migration generation
- Custom migration scripts
- Database schema comparison
