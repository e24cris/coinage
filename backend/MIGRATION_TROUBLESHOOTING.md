# Database Migration Troubleshooting Guide

## Common Migration Errors

### 1. Missing Dependencies
**Symptoms:**
- `ModuleNotFoundError`
- Import errors for Flask extensions

**Solutions:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt

# Or install specific missing packages
pip install flask-login flask-migrate flask-sqlalchemy
```

### 2. Database Connection Issues
**Symptoms:**
- Unable to connect to database
- SQLAlchemy connection errors

**Troubleshooting:**
1. Check `.env` file for correct database configuration
2. Verify database server is running
3. Ensure correct database URI

### 3. Migration Version Conflicts
**Symptoms:**
- Alembic migration version errors
- Unable to apply migrations

**Solutions:**
```bash
# Remove existing migration history
rm -rf migrations/*
flask db init
flask db migrate
flask db upgrade
```

### 4. Circular Import Errors
**Symptoms:**
- Import errors in `__init__.py`
- Circular dependency warnings

**Solutions:**
- Restructure imports
- Use lazy imports
- Move complex logic to separate modules

### 5. Permission and Path Issues
**Symptoms:**
- Permission denied errors
- Unable to create/modify database files

**Solutions:**
- Run as administrator
- Check file/directory permissions
- Verify virtual environment is activated

## Debugging Checklist

1. **Verify Virtual Environment**
   ```bash
   # Check current Python path
   python -c "import sys; print(sys.path)"
   
   # Verify installed packages
   pip list
   ```

2. **Check Database Configuration**
   - Review `.env` file
   - Verify database connection settings

3. **Examine Full Error Traceback**
   - Look for specific error messages
   - Identify exact line causing the issue

## Advanced Troubleshooting

### Manual Database Initialization
```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()  # Force create tables
```

### Resetting Migrations
```bash
# Complete reset (USE WITH CAUTION)
rm coinage.db
rm -rf migrations/*
flask db init
flask db migrate
flask db upgrade
```

## Best Practices
- Always backup database before migrations
- Use version control for migration files
- Test migrations in a staging environment first

## Getting Help
- Check Flask and SQLAlchemy documentation
- Review project-specific configuration
- Consult project maintainers
