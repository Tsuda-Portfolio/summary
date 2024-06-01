from flask import Flask, render_template, request
from Ja import Ja_summary
from En import En_summary
from Ja_En import Ja_to_En_summary
from En_Ja import En_to_Ja_summary
from Yahoo import Yahoo


app = Flask(__name__)


# HomeのHTML
@app.route("/")
def home():
    Yahoo_News = Yahoo()
    return render_template("index.html", Yahoo_News=Yahoo_News)


# 日本語要約のHTML
@app.route("/Ja", methods=["GET", "POST"])
def Japanese():
    # POSTのとき
    if request.method == "POST":
        TEXT = request.form["keyword"]
        LIMIT = request.form["limit"]
        Japanese_summary = Ja_summary(TEXT, LIMIT)
        return render_template(
            "Ja.html", Japanese_summary=Japanese_summary
        )
    # GETのとき
    return render_template("Ja.html")


# 英語要約のHTML
@app.route("/En", methods=["GET", "POST"])
def English():
    # POSTのとき
    if request.method == "POST":
        TEXT = request.form["keyword"]
        LIMIT = request.form["limit"]
        English_summary = En_summary(TEXT, LIMIT)
        return render_template(
            "En.html", English_summary=English_summary
        )
    # GETのとき
    return render_template("En.html")


# 英語から日本語要約のHTML
@app.route("/En_to_Ja", methods=["GET", "POST"])
def En_to_Ja():
    # POSTのとき
    if request.method == "POST":
        TEXT = request.form["keyword"]
        LIMIT = request.form["limit"]
        English_to_Japanese_summary = En_to_Ja_summary(TEXT, LIMIT)
        return render_template(
            "En_to_Ja.html", English_to_Japanese_summary=English_to_Japanese_summary
        )
    # GETのとき
    return render_template("En_to_Ja.html")


# 日本語から英語要約のHTML
@app.route("/Ja_to_En", methods=["GET", "POST"])
def Ja_to_En():
    # POSTのとき
    if request.method == "POST":
        TEXT = request.form["keyword"]
        LIMIT = request.form["limit"]
        Japanese_to_English_summary = Ja_to_En_summary(TEXT, LIMIT)
        return render_template(
            "Ja_to_En.html",
            Japanese_to_English_summary=Japanese_to_English_summary,
        )
    # GETのとき
    return render_template("Ja_to_En.html")


if __name__ == "__main__":
    app.run(debug=True)
