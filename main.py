from flask import Flask, render_template, request
from summary import ja_summary, en_to_ja_summary, ja_to_en_summary, yahoonews_summary


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ja_summary", methods=["GET", "POST"])
def japanese():
    # POSTのとき
    if request.method == "POST":
        TEXT = request.form["keyword"]
        LIMIT = request.form["limit"]
        japanese_summary = ja_summary(TEXT, LIMIT)
        return render_template("ja_summary.html", japanese_summary=japanese_summary)
    # GETのとき
    return render_template("ja_summary.html")


@app.route("/en_to_ja_summary", methods=["GET", "POST"])
def en_to_ja():
    # POSTのとき
    if request.method == "POST":
        TEXT = request.form["keyword"]
        LIMIT = request.form["limit"]
        english_to_ja_summary = en_to_ja_summary(TEXT, LIMIT)
        return render_template(
            "en_to_ja_summary.html", english_to_ja_summary=english_to_ja_summary
        )
    # GETのとき
    return render_template("en_to_ja_summary.html")


@app.route("/ja_to_en_summary", methods=["GET", "POST"])
def ja_to_en():
    # POSTのとき
    if request.method == "POST":
        TEXT = request.form["keyword"]
        LIMIT = request.form["limit"]
        japanese_to_english_summary = ja_to_en_summary(TEXT, LIMIT)
        return render_template(
            "ja_to_en_summary.html",
            japanese_to_english_summary=japanese_to_english_summary,
        )
    # GETのとき
    return render_template("ja_to_en_summary.html")


@app.route("/yahoonews", methods=["GET", "POST"])
def yahoo():
    # POSTのとき
    if request.method == "POST":
        COUNT = request.form["count"]
        LIMIT = request.form["limit"]
        yahoo_summary_data = yahoonews_summary(COUNT, LIMIT)
        return render_template("yahoonews.html", yahoo_summary_data=yahoo_summary_data)
    # GETのとき
    return render_template("yahoonews.html")


if __name__ == "__main__":
    app.run(debug=True)
