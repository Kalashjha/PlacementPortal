from app import app, db, PortalUser

with app.app_context():

    admins = PortalUser.query.filter_by(role_type="admin").all()

    if admins:
        for admin in admins:
            db.session.delete(admin)

        db.session.commit()
        print("All admin users deleted successfully")

    else:
        print("No admin users found")