from flask import Flask, render_template
from summary import Bloomberg_summary, yahoo_news

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/yahoo_summary")
def yahoo_summary():
    yahoo_summary_data = yahoo_news()
    return render_template("yahoo_news.html", yahoo_summary_data=yahoo_summary_data)


@app.route("/Bloomberg_summary")
def Bloomberg():
    Bloomberg_summary_data = Bloomberg_summary()
    return render_template(
        "Bloomberg.html", Bloomberg_summary_data=Bloomberg_summary_data
    )


if __name__ == "__main__":
    app.run(debug=True)
