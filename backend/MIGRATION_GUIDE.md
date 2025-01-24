# Flask Database Migration Guide

## Prerequisites
- Python 3.8+
- Virtual Environment activated
- Flask-Migrate installed

## Dependency Installation
```bash
pip install flask-migrate flask-script flask-sqlalchemy
```

## Migration Workflow

### 1. Initialize Migrations
```bash
# Option 1: Using Flask-Migrate
python flask_migrate_manager.py db init

# Option 2: Using flask command
flask db init
```

### 2. Create Migration
```bash
# Option 1: Using Flask-Migrate Manager
python flask_migrate_manager.py db migrate -m "Initial migration"

# Option 2: Using flask command
flask db migrate -m "Initial migration"
```

### 3. Apply Migration
```bash
# Option 1: Using Flask-Migrate Manager
python flask_migrate_manager.py db upgrade

# Option 2: Using flask command
flask db upgrade
```

## Troubleshooting

### Common Issues
- **No such command 'db'**: 
  - Ensure Flask-Migrate is installed
  - Set FLASK_APP environment variable
  - Use `flask_migrate_manager.py`

- **Import Errors**:
  - Verify virtual environment is activated
  - Check Python path
  - Ensure all dependencies are installed

### Environment Setup
```bash
# Set Flask environment variables
set FLASK_APP=run.py
set FLASK_ENV=development
```

## Advanced Commands

### Rollback Migration
```bash
flask db downgrade
```

### View Migration History
```bash
flask db history
```

### Stamp Migration Version
```bash
flask db stamp head
```

## Best Practices
- Always backup database before migrations
- Test migrations in a staging environment
- Use version control for migration files

## Getting Help
- Check Flask-Migrate documentation
- Review project-specific configuration
- Consult project maintainers
