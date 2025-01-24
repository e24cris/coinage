from app import create_app, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'app': app
    }

if __name__ == '__main__':
    # Verify all necessary modules are imported
    try:
        from flask_migrate import Migrate
        migrate = Migrate(app, db)
    except ImportError as e:
        print(f"Migration setup failed: {e}")
        print("Please install required dependencies: pip install flask-migrate")

    app.run(debug=True)
