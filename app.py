from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=5)

@app.route("/")
def home():
	if "user" in session:
		user = session["user"]
		text = f"Welcome, {user}!"
		return render_template("index.html", text=text)
	else:
		return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		user = request.form["name"]
		email = request.form["email"]
		password = request.form["password"]
		session["user"] = user
		session["email"] = email
		session["password"] = password
		flash("Login Succesful!")
		return redirect(url_for("user"))
	else:
		if "user" in session:
			flash("Already logged In!")
			return redirect(url_for("user"))
		return render_template("login.html")

@app.route("/user")
def user():
	if "user" in session:
		user = session["user"]
		email = session["email"]
		password = session["password"]
		return render_template("user.html", name=user, email=email, password=password)
	else:
		flash("You are not logged in!")
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	try:
		user = session["user"]
		flash(f"You have been logged out, {user}.", "info")
		session.pop("user", None)
		session.pop("email", None)
		session.pop("password", None)
		return redirect(url_for("login"))
	except:
		flash("Already logged out!")
		return redirect(url_for("home"))

if __name__ == "__main__":
	app.run(debug=True)