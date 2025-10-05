from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime
from detector import analyze_certificate
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# In-memory storage
users = {"admin": {"password": "admin123", "role": "admin"}}
uploads = []

# ----------------- Routes -----------------
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("upload"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            flash("Username already exists!", "error")
        else:
            users[username] = {"password": password, "role": "user"}
            flash("Account created successfully!", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session["username"] = username
            session["role"] = users[username]["role"]
            if session["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("upload"))
        else:
            flash("Invalid credentials!", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            result = analyze_certificate(path)
            uploads.append({
                "username": session["username"],
                "filename": filename,
                "score": result["score"],
                "status": result["status"],
                "text": result["text"],
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return render_template("result.html", score=result["score"], extracted_text=result["text"])
    return render_template("index.html")

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin.html", uploads=uploads, users=users)

if __name__ == "__main__":
    app.run(debug=True)
