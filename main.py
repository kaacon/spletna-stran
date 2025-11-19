from flask import Flask, request, render_template, redirect, make_response
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/prijava/')
def prijava():
    return render_template("prijava.html")

@app.route('/prijava-submit/')
def prijava_submit():
    uporabnisko_ime = request.args.get("username")
    geslo = request.args.get("geslo")
    print(uporabnisko_ime, geslo)

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    query = 'SELECT * FROM contacts WHERE first_name="'+uporabnisko_ime+'" AND last_name="'+geslo+'"'
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        response = make_response(redirect("/main/"))
        response.set_cookie("username", uporabnisko_ime)
        return response
    else:
        return render_template("prijava.html", info_text = "Prijava ni uspela")

@app.route('/registracija/')
def registracija():
    return render_template("registracija.html")

@app.route('/registracija-submit/')
def registracija_submit():
    uporabnisko_ime = request.args.get("username")
    geslo = request.args.get("geslo")

    insert_command = 'INSERT INTO contacts(first_name, last_name) VALUES("'+uporabnisko_ime+'", "'+geslo+'");'
    print(insert_command)
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(insert_command)
    conn.commit()
    conn.close()
    return redirect("/prijava/")

@app.route('/main/')
def main():
    username = request.cookies.get("username")
    if not username:
        return redirect("/prijava/")

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    query = 'SELECT id, note_text FROM notes WHERE username="'+username+'";'
    cursor.execute(query)
    notes = cursor.fetchall()
    conn.close()

    notes_html = "<br>".join(note[1] for note in notes)
    if not notes_html:
        notes_html = "<p>Nimate še nobenih zapiskov</p>"

    return render_template("main.html", username=username, notes_html=notes_html)

@app.route('/add-note-submit/')
def add_note_submit():
    username = request.cookies.get("username")
    if not username:
        return redirect("/prijava/")

    note_text = request.args.get("note")
    note_text = note_text.replace("<","")

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    insert_command = 'INSERT INTO notes(username, note_text) VALUES("'+username+'", "'+note_text+'")'
    cursor.execute(insert_command)
    conn.commit()
    conn.close()

    return redirect("/main/")

@app.route('/odjava/')
def odjava():
    response = make_response(redirect("/"))
    response.set_cookie("username", "", expires=0)
    return response

app.run(debug=True)

