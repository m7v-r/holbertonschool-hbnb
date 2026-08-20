from app import create_app, db
from app.models.user import User


def seed_admin():
    app = create_app()

    with app.app_context():
        admin_email = "admin@hbnb.io"

        existing_admin = User.query.filter_by(
            email=admin_email
        ).first()

        if not existing_admin:
            admin = User(
                first_name="Admin",
                last_name="User",
                email=admin_email,
                password="admin123",
                is_admin=True
            )

            db.session.add(admin)
            db.session.commit()

            print("Admin user created successfully!")

        else:
            print("Admin user already exists.")


if __name__ == "__main__":
    seed_admin()
