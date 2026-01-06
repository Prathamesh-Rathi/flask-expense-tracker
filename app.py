from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from flask_bcrypt import Bcrypt
from sqlalchemy import func
from models import db, User, Expense

app = Flask(__name__)

# Secret key for session (change to something random in real use)
app.config["SECRET_KEY"] = "change-this-secret-key"

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)

# Create tables once, at startup
with app.app_context():
    db.create_all()


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


def login_required(view_func):
    def wrapper(*args, **kwargs):
        if not get_current_user():
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            return render_template("signup.html", error="All fields are required.")

        existing = User.query.filter_by(email=email).first()
        if existing:
            return render_template("signup.html", error="Email already registered.")

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(name=name, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template("login.html", error="Invalid email or password.")

        if not bcrypt.check_password_hash(user.password_hash, password):
            return render_template("login.html", error="Invalid email or password.")

        session["user_id"] = user.id
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    current_user = get_current_user()

    if request.method == "POST":
        category = request.form.get("category")
        amount = request.form.get("amount")
        comments = request.form.get("comments")

        if not category or not amount:
            return redirect(url_for("home"))

        try:
            amount_value = float(amount)
            if amount_value <= 0:
                raise ValueError()
        except ValueError:
            return redirect(url_for("home"))

        expense = Expense(
            category=category,
            amount=amount_value,
            comments=comments,
            user_id=current_user.id,
        )
        db.session.add(expense)
        db.session.commit()

        return redirect(url_for("home"))

    expenses = (
        Expense.query
        .filter_by(user_id=current_user.id)
        .order_by(Expense.created_at.desc())
        .all()
    )
    return render_template("home.html", expenses=expenses, user=current_user)


@app.route("/expense/<int:expense_id>/edit", methods=["POST"])
@login_required
def edit_expense(expense_id):
    current_user = get_current_user()
    expense = Expense.query.filter_by(
        id=expense_id, user_id=current_user.id
    ).first_or_404()

    category = request.form.get("category")
    amount = request.form.get("amount")
    comments = request.form.get("comments")

    if not category or not amount:
        return redirect(url_for("home"))

    try:
        amount_value = float(amount)
        if amount_value <= 0:
            raise ValueError()
    except ValueError:
        return redirect(url_for("home"))

    expense.category = category
    expense.amount = amount_value
    expense.comments = comments
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/expense/<int:expense_id>/delete", methods=["POST"])
@login_required
def delete_expense(expense_id):
    current_user = get_current_user()
    expense = Expense.query.filter_by(
        id=expense_id, user_id=current_user.id
    ).first_or_404()

    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/chart")
@login_required
def chart():
    current_user = get_current_user()

    results = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .filter_by(user_id=current_user.id)
        .group_by(Expense.category)
        .all()
    )

    labels = [row[0] for row in results]
    values = [float(row[1]) for row in results]

    return render_template(
        "chart.html",
        labels=labels,
        values=values,
        user=current_user,
    )


if __name__ == "__main__":
    app.run(debug=True)
