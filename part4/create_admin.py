from app import create_app, db
from app.models.user import User


def seed_admin():
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(email="admin@hbnb.io").first()

        if not admin:
            admin = User(
                first_name="Admin",
                last_name="HBnB",
                email="admin@hbnb.io",
                password="admin1234",
                is_admin=True,
            )
            admin.id = "36c9050e-ddd3-4c3b-9731-9f487208bbc1"

            db.session.add(admin)
            db.session.commit()
            print("Successfully created admin user (admin@hbnb.io).")
        else:
            print("Admin user already exists. Skipping seed.")


if __name__ == "__main__":
    seed_admin()
