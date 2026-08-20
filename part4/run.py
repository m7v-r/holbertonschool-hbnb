from app import create_app
from create_admin import seed_admin

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        seed_admin()

    app.run(debug=True)
