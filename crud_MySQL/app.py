from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = '3rrou.h.filess.io'
app.config['MYSQL_USER'] = 'basedatos_chancemake'
app.config['MYSQL_PASSWORD'] = '11f552fa0d338c64e1d39e312250283e8202895a'
app.config['MYSQL_DB'] = 'basedatos_chancemake'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)  

@app.route('/')
def index():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.close()
        return render_template('index.html', users=data)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nombre = %s, email = %s, password = %s WHERE id = %s", (nombre, email, password, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        data = cur.fetchone()
        cur.close()
        return render_template('edit.html', user=data)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
