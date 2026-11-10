import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
DB_PATH = os.getenv("DATABASE_PATH", "contracts.db")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            owner TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL,
            decision_note TEXT
        )
    """)
    db.commit()
    db.close()

@app.route("/")
def index():
    contracts = get_db().execute(
        "SELECT * FROM contracts ORDER BY id DESC"
    ).fetchall()
    return render_template("index.html", contracts=contracts)

@app.route("/contracts/new", methods=["GET", "POST"])
def new_contract():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        department = request.form.get("department", "").strip()
        owner = request.form.get("owner", "").strip()
        description = request.form.get("description", "").strip()
        if not all([title, department, owner]):
            flash("Title, department and owner are required.", "error")
            return render_template("new_contract.html")
        get_db().execute(
            """INSERT INTO contracts
               (title, department, owner, description, status, created_at)
               VALUES (?, ?, ?, ?, 'Pending', ?)""",
            (title, department, owner, description, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        get_db().commit()
        flash("Contract submitted for approval.", "success")
        return redirect(url_for("index"))
    return render_template("new_contract.html")

@app.post("/contracts/<int:contract_id>/decision")
def decision(contract_id):
    action = request.form.get("action")
    note = request.form.get("note", "").strip()
    if action not in ("Approved", "Rejected"):
        flash("Invalid approval action.", "error")
        return redirect(url_for("index"))
    db = get_db()
    row = db.execute("SELECT id FROM contracts WHERE id = ?", (contract_id,)).fetchone()
    if row is None:
        flash("Contract not found.", "error")
        return redirect(url_for("index"))
    db.execute(
        "UPDATE contracts SET status = ?, decision_note = ? WHERE id = ?",
        (action, note, contract_id)
    )
    db.commit()
    flash(f"Contract {action.lower()}.", "success")
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
