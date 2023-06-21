from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_mysqldb import MySQL
import ssl
app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Divendin14#'
app.config['MYSQL_DB']='users'
mysql = MySQL(app)

@app.route('/create', methods=['POST'])
def create():
    data = request.json
    name = data['name']
    email = data['email']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()

    return jsonify({'message': 'Record created successfully!', 'id': cur.lastrowid})


# Retrieve all records
@app.route('/read', methods=['GET'])
def read():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    records = cur.fetchall()

    return jsonify(records)

@app.route('/')
def home():
    return {"Home":"Hello"}
# Update an existing record
@app.route('/update/<int:user_id>', methods=['PUT'])
def update(user_id):
    data = request.json
    name = data['name']
    email = data['email']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, user_id))
    mysql.connection.commit()

    if cur.rowcount > 0:
        return jsonify({'message': 'Record updated successfully!'})
    else:
        return jsonify({'message': 'No record found for the given ID.'})


# Delete a record
@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    mysql.connection.commit()

    if cur.rowcount > 0:
        return jsonify({'message': 'Record deleted successfully!'})
    else:
        return jsonify({'message': 'No record found for the given ID.'})



if __name__ == '__main__':
    app.run(debug=True,port=8000)
