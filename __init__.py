from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')
def est_authentifie_admin():
    return session.get('admin_auth')

def est_authentifie_user():
    return session.get('user_auth')

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['admin_auth'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        elif request.form['username'] == 'user' and request.form['password'] == '12345':
            session['user_auth'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('fiche_par_nom'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

# @app.route('/fiche_nom/<string:post_name>')
# def Readname(post_name):
#     if not est_authentifie():
#         # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
#         return redirect(url_for('authentification'))
#     elif request.method == 'POST':
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM clients WHERE nom = ?', (post_name,))
#         data = cursor.fetchall()
#         conn.close()
#         # Rendre le template HTML et transmettre les données
#         return render_template('by_name.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement


@app.route('/fiche_nom/', methods=['GET', 'POST'])
def fiche_par_nom():
    if not est_authentifie_user():
        return redirect(url_for('authentification'))

    data = []
    if request.method == 'POST':
        try:
            nom = request.form['nom']
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
            data = cursor.fetchall()
            conn.close()
        except Exception as e:
            return f"<h3>Erreur lors de la recherche : {e}</h3>"

    return render_template('by_name.html', data=data)

@app.route('/logout_admin')
def logout_admin():
    session.pop('admin_auth', None)
    return redirect(url_for('authentification'))

@app.route('/logout_user')
def logout_user():
    session.pop('user_auth', None)
    return redirect(url_for('authentification'))

                                                       
                                                                                
if __name__ == "__main__":
  app.run(debug=True)
