import trend_app_protect.start
import os
import hashlib
from flask import Flask, request, redirect

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'

@app.route('/')
def menu():
    return """
        <h1>AppSec Demo</h1>
        <p>
        <a href='menu'>Menu</a>
        </p>
        <p>
        <a href='log'>Log</a>
        </p>
        <p>
        <a href="upload">Upload</a>
        </p>
        <p>
        <a href="redirect">Redirect to Yandex</a>
        </p>
        <p>
        <a href="sql">Auth User</a>
        </p>
    """


@app.route('/menu')
def get():
    req = request.args.get('option')
    if req is not None:
        return open(req, 'rb').read()

    return """
        <form action="" method="get">
        <p>
        <label for="menu">Choose option:</label>
            <select name="option" id="option">
                <option value="first.html">First</option>
                <option value="second.html">Second</option>
                <option value="third.html">Third</option>
            </select>
	</p>
        <p>
	    <input type="submit">
	</p>
    </form>
    """

@app.route('/log')
def log():
    from datetime import datetime
    with open('/tmp/appsec.txt', 'a') as fp:
        fp.write(str(datetime.now()) + ' event description\n')
    result = '<h3>Logging</h3>'
    result += '/tmp/appsec.txt: <br/>\n'
    result += "<pre>\n"
    result += open('/tmp/appsec.txt', 'r').read()
    result += "</pre>"
    result += '<a href="clear">Clear</a>'
    return result

@app.route('/clear')
def clear():
    os.remove('/tmp/appsec.txt')
    return 'Removed<br/> <a href="/">Main menu</a>'


@app.route('/upload', methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            return "File is missing"
        file = request.files["file"]
        return "File name:" + file.filename + '<br/> <a href="/">Main menu</a>'

    return """
<form method="post" enctype="multipart/form-data">
<input type="file" name="file" id="file">
<input type="submit" value="Upload" name="submit">
</form>
    """

@app.route('/redirect')
def redir():
    return redirect('http://www.ya.ru')

@app.route('/sql', methods=['POST', 'GET'])
def sql():
    import sqlite3
    exist = os.path.isfile('auth.db')
    conn = sqlite3.connect('auth.db')
    c = conn.cursor()
    if not exist:
        c.execute("CREATE TABLE users (name text, password text)")
        conn.commit()
        users = ('mike', 'bill')
        passwords = ('topsecret', '1234')
        for user, password in zip(users, passwords):
            pwd = hashlib.md5(password.encode()).hexdigest()
            c.execute(f"INSERT INTO users VALUES('{user}', '{pwd}')")
            conn.commit()
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        pwd = hashlib.md5(password.encode()).hexdigest()
        query = "SELECT * FROM users WHERE " \
                f"name = '{user}' AND password = '{pwd}'"
        result = c.execute(query)
        if len(result.fetchall()) > 0:
            return "<h1>Access granted</h1>" 
        else:
            return "<h1>Access denied</h1>" + query 
    return """
    <form method="POST">
        <input type="text" name="user"/><br/>
        <input type="password" name="password"/><br/>
        <input type="submit" value="Submit" name="submit"/>
    </form>
    """
