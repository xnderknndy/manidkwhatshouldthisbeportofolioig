from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)
def db():
    return sqlite3.connect("data.db")
con = db()
con.execute("CREATE TABLE IF NOT EXISTS portofolio (project TEXT, skill TEXT, deskripsi TEXT)")
con.close()

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/form", methods=["GET","POST"])
def form():
    if request.method == "POST":
        con = db()
        con.execute("INSERT INTO portofolio VALUES (?,?,?)",
                    (request.form["project"], request.form["skill"], request.form["deskripsi"]))
        con.commit()
        con.close()
        return redirect("/data")
    return render_template("form.html")
@app.route("/data")
def data():
    con = db()
    rows = con.execute("SELECT rowid, * FROM portofolio").fetchall()
    con.close()
    return render_template("data.html", rows=rows)


@app.route("/delete/<int:id>")
def delete(id):
    con = db()
    con.execute("DELETE FROM portofolio WHERE rowid = ?", (id,))
    con.commit()
    con.close()
    return redirect("/data")



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    con = db()

    if request.method == "POST":
        con.execute("""
            UPDATE portofolio 
            SET project = ?, skill = ?, deskripsi = ?
            WHERE rowid = ?
        """, (
            request.form["project"],
            request.form["skill"],
            request.form["deskripsi"],
            id
        ))
        con.commit()
        con.close()
        return redirect("/data")

    row = con.execute(
        "SELECT rowid, * FROM portofolio WHERE rowid = ?", (id,)
    ).fetchone()
    con.close()

    return render_template("form.html", row=row)


if __name__ == "__main__":
    app.run()