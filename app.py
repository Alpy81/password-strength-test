from flask import Flask, render_template, request
import string

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check_password", methods=["POST"])
def check_password():
    password = request.form["password"]
    min_length = 8

    strength = 0
    remarks = ""
    categories = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        " ",
        string.punctuation,
    ]

    if len(password) < min_length:
        remarks = f"Das Passwort ist zu kurz. Es sollte mindestens {min_length} Zeichen enthalten."
    else:
        for category in categories:
            if any(char in category for char in password):
                strength += 1

        if strength == 1:
            remarks = "Das ist ein sehr schwaches Passwort. Ändern Sie es so schnell wie möglich."
        elif strength == 2:
            remarks = "Das ist ein schwaches Passwort. Sie sollten darüber nachdenken, ein stärkeres Passwort zu verwenden."
        elif strength == 3:
            remarks = "Ihr Passwort ist okay, aber es kann verbessert werden."
        elif strength == 4:
            remarks = "Ihr Passwort ist schwer zu erraten, aber Sie könnten es noch sicherer machen."
        elif strength == 5:
            remarks = "Das ist ein sehr starkes Passwort! Hacker haben keine Chance, dieses Passwort zu erraten."

    categories_count = [
        (category, any(char in category for char in password))
        for category in [
            "Kleinbuchstaben",
            "Großbuchstaben",
            "Ziffern",
            "Leerzeichen",
            "Sonderzeichen",
        ]
    ]

    print("Ihr Passwort hat:")
    for category, count in categories_count:
        print(f"{count} {category}")

    print(f"Passwortstärke: {strength} / 5")
    print(f"Bemerkungen: {remarks}")

    return render_template(
        "result.html",
        categories_count=categories_count,
        strength=strength,
        remarks=remarks,
    )


def check_pwd(another_pw=False):
    valid = False
    if another_pw:
        choice = input(
            "Möchten Sie die Stärke eines weiteren Passworts überprüfen? (j/n): "
        )
    else:
        choice = input("Möchten Sie die Stärke Ihres Passworts überprüfen? (j/n): ")

    while not valid:
        if choice.lower() == "j":
            return True
        elif choice.lower() == "n":
            print("Beende...")
            return False
        else:
            print("Ungültige Eingabe... bitte versuchen Sie es erneut.\n")


if __name__ == "__main__":
    print("===== Willkommen beim Passwortstärke-Checker =====")
    app.run(debug=True)
