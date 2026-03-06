from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

#db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_placement_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Db model for users
class PortalUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(70), nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(90), nullable=False)
    role_type = db.Column(db.String(20), nullable=False)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = PortalUser.query.filter_by(email_address=email).first()

        if user and check_password_hash(user.password_hash, password):

            # Store user info in session
            session["user_id"] = user.id
            session["user_role"] = user.role_type
            session["user_name"] = user.candidate_name

            # Redirect based on role
            if user.role_type == "student":
                return redirect("/student-dashboard")

            elif user.role_type == "company":
                return redirect("/company-dashboard")

        else:
            return "Invalid email or password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        # Check if email already exists
        existing_user = PortalUser.query.filter_by(email_address=email).first()

        if existing_user:
            return "Email already registered!"

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create new user object
        new_user = PortalUser(
            candidate_name=name,
            email_address=email,
            password_hash=hashed_password,
            role_type=role
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")
@app.route("/student-dashboard")
def student_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return f"Welcome {session['user_name']} (Student)"
@app.route("/company-dashboard")
def company_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return f"Welcome {session['user_name']} (Company)"
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # it will create database and table automatically
    app.run(debug=True)