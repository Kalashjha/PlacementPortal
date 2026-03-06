from app import app, db, PortalUser
from werkzeug.security import generate_password_hash

with app.app_context():

    # Check if admin already exists
    existing_admin = PortalUser.query.filter_by(role_type="admin").first()

    if existing_admin:
        print("Admin already exists!")
        print("Admin Email:", existing_admin.email_address)

    else:
        name = input("Enter admin name: ")
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")

        admin = PortalUser(
            candidate_name=name,
            email_address=email,
            password_hash=generate_password_hash(password),
            role_type="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully.")