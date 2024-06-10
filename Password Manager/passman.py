from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_password():
    username = request.form["username"]
    password = request.form["password"]
    if username and password:
        with open("passwords.txt", 'a') as f:
            f.write(f"{username} {password}\n")
        return "Password added successfully!"
    else:
        return "Please enter both the fields", 400

@app.route("/get", methods=["POST"])
def get_password():
    username = request.form["username"]
    passwords = {}
    try:
        with open("passwords.txt", 'r') as f:
            for k in f:
                i = k.split(' ')
                passwords[i[0]] = i[1]
    except:
        return "ERROR!!", 500

    if passwords:
        mess = "Your passwords:\n"
        for i in passwords:
            if i == username:
                mess += f"Password for {username} is {passwords[i]}\n"
                break
        else:
            mess += "No Such Username Exists!!"
        return mess
    else:
        return "EMPTY LIST!!", 404

@app.route("/list", methods=["GET"])
def list_passwords():
    passwords = {}
    try:
        with open("passwords.txt", 'r') as f:
            for k in f:
                i = k.split(' ')
                passwords[i[0]] = i[1]
    except:
        return "No passwords found!!", 404

    if passwords:
        mess = "List of passwords:\n"
        for name, password in passwords.items():
            mess += f"Password for {name} is {password}\n"
        return mess
    else:
        return "Empty List!!", 404

@app.route("/delete", methods=["POST"])
def delete_password():
    username = request.form["username"]
    temp_passwords = []
    try:
        with open("passwords.txt", 'r') as f:
            for k in f:
                i = k.split(' ')
                if i[0] != username:
                    temp_passwords.append(f"{i[0]} {i[1]}")
        with open("passwords.txt", 'w') as f:
            for line in temp_passwords:
                f.write(line)
        return f"User {username} deleted successfully!"
    except Exception as e:
        return f"Error deleting user {username}: {e}", 500

@app.route("/generate", methods=["GET"])
def generate_password():
    password_length = 12
    password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(password_length))
    return render_template("generate.html", password=password)

@app.route("/clear", methods=["GET"])
def clear_fields():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
