from bs4 import BeautifulSoup
import requests
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.similarityfilter.tfidf_cosine import TfIdfCosine
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer

# ----------ITmediaニュースの要約(API使用なし)---------- #
def ITmedia(COUNT=2, LIMIT=0.3):
    # LIMITをfloat型に修正する
    LIMIT = float(LIMIT)

    # COUNTをint型に修正する
    COUNT = int(COUNT)

    # ITmediaのURL
    url = "https://www.itmedia.co.jp/news/"

    # リストを用意
    itmedia_news_list = []

    # ITmediaニュースのトップページのリクエスト要求
    response = requests.get(url)

    # 解析
    soup_1 = BeautifulSoup(response.content, "lxml")

    # 記事を取得
    articles = soup_1.select("div.colBoxTitle > h3 > a")

    for i, article in enumerate(articles, start=1):
        # URLを作成
        article_url = article.get("href")
        if not article_url.startswith("http"):
            article_url = "https://www.itmedia.co.jp" + article_url

        # 記事のリクエスト要求
        article_response = requests.get(article_url)

        # 解析
        article_soup = BeautifulSoup(article_response.content, "lxml")

        # 時間の解析
        article_date = article_soup.select("#update")

        # 時間が取得できるか
        if article_date:
            article_date = article_date[0].text
        else:
            article_date = "記事の投稿時間が取得できませんでした．"

        # 記事タイトルの解析
        article_title = article_soup.select("h1 > span.title__maintext")

        # 記事タイトルが取得できるか
        if article_title:
            article_title = article_title[0].text
        else:
            article_title = "記事タイトルが取得できませんでした．"

        # 画像の解析
        article_image = article_soup.select("div.inner > div > a > img")

        # 画像が取得できるか
        if article_image:
            article_image = article_image[0].get('src')
        else:
            article_image = "画像が取得できませんでした．"

        # 記事の内容の解析
        article_contain = article_soup.select("div.inner > p")

        # 記事の内容が取得できるか
        if not article_contain:
            all_sentence = "記事の内容が取得できませんでした．"
        else:
            article_contain = "".join([p.text for p in article_contain])

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

        itmedia_news_list.append(
            {
                "article_date": article_date,
                "article_URL": article_url,
                "article_image": article_image,
                "article_title": article_title,
                "article_summary": all_sentence,
            }
        )

        if i == COUNT or i == 7:
            return itmedia_news_list