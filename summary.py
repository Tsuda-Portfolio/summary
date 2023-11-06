from bs4 import BeautifulSoup
import requests
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.similarityfilter.tfidf_cosine import TfIdfCosine
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer


def Bloomberg_summary():
    similarity_limit = 0.4

    url = "https://www.bloomberg.co.jp/"

    # blooombergのトップページのリクエスト要求
    response = requests.get(url)

    # 解析
    soup_1 = BeautifulSoup(response.content, "lxml")

    # 記事を取得
    articles = soup_1.select("article.story-list-story > a")

    # リストを用意
    Bloomberg_list = []

    for i, article in enumerate(articles, start=1):
        # URLを作成
        article_url = url + article.get("href")

        # 記事のリクエスト要求
        article_response = requests.get(article_url)

        article_soup = BeautifulSoup(article_response.content, "lxml")

        article_date = article_soup.select_one("time.article-timestamp").text

        article_title = article_soup.select_one(".lede-text-only__highlight").text

        article_contains = article_soup.select(".body-copy > p")

        all_articles_text = ""

        for article_contain in article_contains:
            article = article_contain.text

            all_articles_text += article
            all_articles_text = "".join(all_articles_text.split())

        # NLPオブジェクト
        nlp_base = NlpBase()
        # トークナイザー設定（MeCab使用）
        nlp_base.tokenizable_doc = MeCabTokenizer()
        # 類似性フィルター
        similarity_filter = TfIdfCosine()
        # NLPオブジェクト設定
        similarity_filter.nlp_base = nlp_base
        # 類似性limit：limit超える文は切り捨て
        similarity_filter.similarity_limit = similarity_limit

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
            all_articles_text, abstractable_doc, similarity_filter
        )

        all_sentence = ""

        # 出力
        for sentence in result_dict2["summarize_result"]:
            all_sentence += sentence

        Bloomberg_list.append(
            {
                "article_num": i,
                "article_URL": article_url,
                "article_date": article_date,
                "article_title": article_title,
                "article_summary": all_sentence,
            }
        )

        if i == 5:
            return Bloomberg_list


def yahoo_news():
    similarity_limit = 0.5

    url = "https://news.yahoo.co.jp/"

    # yahoo_newsのトップページのリクエスト要求
    response = requests.get(url)

    # 解析
    soup_1 = BeautifulSoup(response.content, "lxml")

    # 記事を取得
    articles = soup_1.select("li.sc-fHCHyC > a")

    # リストを用意
    yahoo_news_list = []

    for i, article in enumerate(articles, start=1):
        # URLを作成
        article_url = article.get("href")

        # 記事のリクエスト要求
        article_response = requests.get(article_url)

        article_soup = BeautifulSoup(article_response.content, "lxml")

        # もっと見る
        more_articles = article_soup.select_one("p.sc-cXlOVI > a")

        for more_article in more_articles:
            # URLを作成
            more_article_url = more_articles.get("href")

            # 記事のリクエスト要求
            more_article_response = requests.get(more_article_url)

            more_article_soup = BeautifulSoup(more_article_response.content, "lxml")

            article_date = more_article_soup.select_one("p.sc-gSiFqf > time").text

            article_title = more_article_soup.select_one("#uamods > header > h1").text

            article_contain = more_article_soup.select_one(".sc-gDyJDg > p").text

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
            similarity_filter.similarity_limit = similarity_limit

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
                    "article_num": i,
                    "article_URL": more_article_url,
                    "article_date": article_date,
                    "article_title": article_title,
                    "article_summary": all_sentence,
                }
            )

        if i == 5:
            return yahoo_news_list
