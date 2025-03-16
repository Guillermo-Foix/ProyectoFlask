import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = 'basedatos.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        conn.execute('INSERT INTO users (nombre, email, password) VALUES (?, ?, ?)',
                     (nombre, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        conn.execute('UPDATE users SET nombre = ?, email = ?, password = ? WHERE id = ?',
                     (nombre, email, password, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>', methods=('POST','GET'))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
