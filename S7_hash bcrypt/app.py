from flask import Flask, render_template, request
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt()


@app.route("/", methods=["GET", "POST"])
def generate_hash():
    if request.method == "POST":
        plaintext_password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(plaintext_password).decode(
            "utf-8"
        )
        return f"Hashed Password: {hashed_password}"
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
