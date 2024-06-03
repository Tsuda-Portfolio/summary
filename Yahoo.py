from bs4 import BeautifulSoup
import requests
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.similarityfilter.tfidf_cosine import TfIdfCosine
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer


# ----------ヤフーニュースの要約(API使用なし)---------- #
def Yahoo(COUNT=2, LIMIT=0.3):
    # LIMITをfloat型に修正する
    LIMIT = float(LIMIT)

    # COUNTをint型に修正する
    COUNT = int(COUNT)

    # yahoonewsのURL
    url = "https://news.yahoo.co.jp/"

    # リストを用意
    yahoo_news_list = []

    # yahoo_newsのトップページのリクエスト要求
    response = requests.get(url)

    # 解析
    soup_1 = BeautifulSoup(response.content, "lxml")

    # 記事を取得
    articles = soup_1.select("li.sc-1nhdoj2-0 > a")

    for i, article in enumerate(articles, start=1):
        # URLを作成
        article_url = article.get("href")

        # 記事のリクエスト要求
        article_response = requests.get(article_url)

        # 解析
        article_soup = BeautifulSoup(article_response.content, "lxml")

        # 記事全文を読む
        more_articles = article_soup.select_one("div.sc-gdv5m1-8 > a")

        # URLを作成
        more_article_url = more_articles.get("href")

        # 記事のリクエスト要求
        more_article_response = requests.get(more_article_url)

        # 解析
        more_article_soup = BeautifulSoup(more_article_response.content, "lxml")

        # 時間の解析
        article_date = more_article_soup.select("p.sc-uzx6gd-4 > time")

        # 時間が取得できるか
        if article_date:
            article_date = article_date[0].text
        else:
            article_date = "記事の投稿時間が取得できませんでした．"

        # 記事タイトルの解析
        article_title = more_article_soup.select("#uamods > header > h1")


        # 記事タイトルが取得できるか
        if article_title:
            article_title = article_title[0].text
        else:
            article_title = "記事タイトルが取得できませんでした．"

        # 画像の解析
        article_image = more_article_soup.select(".sc-1z2z0a-0 > picture > img")

        # 画像が取得できるか
        if article_image:
            article_image = article_image[0].get('src')
        else:
            article_image = "画像が取得できませんでした．"

        # 記事の内容の解析
        article_contain = more_article_soup.select(".sc-zniwbk-0 > p")

        # 記事の解析が取得できるか
        if not article_contain:
            all_sentence = "記事の内容が取得できませんでした．"
        else:
            article_contain = article_contain[0].text

            article_contain = "".join(article_contain.split())

            # NLPオブジェクト
            nlp_base = NlpBase()
            # トークナイザー設定（MeCab使用）
            nlp_base.tokenizable_doc = MeCabTokenizer()
            # 類似性フィルター
            similarity_filter = TfIdfCosine()
            # NLPオブジェクト設定
            similarity_filter.nlp_base = nlp_base
            # 類似性limit：limit超える文は切り捨て
            similarity_filter.similarity_limit = LIMIT

            # 自動要約のオブジェクト
            auto_abstractor = AutoAbstractor()
            # トークナイザー設定（MeCab使用）
            auto_abstractor.tokenizable_doc = MeCabTokenizer()
            # 区切り文字設定
            auto_abstractor.delimiter_list = ["。", "\n"]
            # 抽象化&フィルタリングオブジェクト
            abstractable_doc = TopNRankAbstractor()
            # 文書要約（similarity_filter機能追加）
            result_dict2 = auto_abstractor.summarize(
                article_contain, abstractable_doc, similarity_filter
            )

            all_sentence = ""

            # 出力
            for sentence in result_dict2["summarize_result"]:
                all_sentence += sentence

        yahoo_news_list.append(
            {
                "article_date": article_date,
                "article_URL": more_article_url,
                "article_image": article_image,
                "article_title": article_title,
                "article_summary": all_sentence,
            }
        )

        if i == COUNT or i == 7:
            return yahoo_news_list