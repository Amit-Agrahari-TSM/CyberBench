#!/bin/bash
cat << 'EOF' > app_fixed.py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'SuperSecretPass123!')")
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Parameterized SQL query preventing SQL Injection
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "user": user[1]})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    init_db()
    app.run(port=5000)
EOF

cat << 'EOF' > report.json
{
  "vulnerable_file": "app.py",
  "vulnerability_type": "SQL Injection",
  "remediation": "Parameterized Queries",
  "vulnerability_fixed": true
}
EOF
