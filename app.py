from flask import Flask, render_template, request
from summary import ja_summary, en_summary, en_to_ja_summary, ja_to_en_summary, yahoonews_summary, home_news, search_news


app = Flask(__name__)


# HomeのHTML
@app.route("/")
def index():
    home_News = home_news()
    return render_template("index.html", home_News=home_News)


# 日本語要約のHTML
@app.route("/ja_summary", methods=["GET", "POST"])
def japanese():
    home_News = home_news()
    # POSTのとき
    if request.method == "POST":
        TEXT = request.form["keyword"]
        LIMIT = request.form["limit"]
        japanese_summary = ja_summary(TEXT, LIMIT)
        return render_template("ja_summary.html", japanese_summary=japanese_summary, home_News=home_News)
    # GETのとき
    return render_template("ja_summary.html", home_News=home_News)


# 英語要約のHTML
@app.route("/en_summary", methods=["GET", "POST"])
def english():
    home_News = home_news()
    # POSTのとき
    if request.method == "POST":
        TEXT = request.form["keyword"]
        LIMIT = request.form["limit"]
        english_summary = en_summary(TEXT, LIMIT)
        return render_template("en_summary.html", english_summary=english_summary, home_News=home_News)
    # GETのとき
    return render_template("en_summary.html", home_News=home_News)


# 英語から日本語要約のHTML
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


# 日本語から英語要約のHTML
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


# Yahoo!News要約のHTML
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


# 404エラーハンドリング
@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Error</h1>', 404


if __name__ == "__main__":
    app.run(debug=True)
