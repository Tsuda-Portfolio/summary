import os
import html
from os.path import join, dirname
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import requests
import deepl
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.similarityfilter.tfidf_cosine import TfIdfCosine
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer


# ----------日本語の文章の要約(要約の度合いを決めれる)---------- #
def ja_summary(TEXT, LIMIT):
    LIMIT = float(LIMIT)

    # 空のリストを用意
    ja_summary = []

    # 元の文章の長さ
    original_text_len = len(TEXT)

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
    result_dict2 = auto_abstractor.summarize(TEXT, abstractable_doc, similarity_filter)

    # 空白の文字列を用意
    summary = ""

    # 出力
    for sentence in result_dict2["summarize_result"]:
        summary += sentence
        summary = "".join(summary.split())

    # 要約文から改行を取り除く
    summary_without_newlines = summary.replace("\n", "")

    # 要約後の文章の長さ
    summary_text_len = len(summary_without_newlines)

    ja_summary.append(
        {
            "original_text_len": original_text_len,
            "summary": summary,
            "summary_text_len": summary_text_len,
        }
    )
    return ja_summary


# ----------英語の文章の要約(要約の度合いを決めれる)---------- #
def en_summary(TEXT, LIMIT):

    # LIMITをfloat型に修正する
    LIMIT = float(LIMIT)

    # 空のリストを用意
    en_summary = []

    # 元の文章の長さ
    original_text_len = len(TEXT)

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
    auto_abstractor.delimiter_list = [".", "\n"]

    # 抽象化&フィルタリングオブジェクト
    abstractable_doc = TopNRankAbstractor()

    # 文書要約（similarity_filter機能追加）
    result_dict2 = auto_abstractor.summarize(TEXT, abstractable_doc, similarity_filter)

    # 空白の文字列を用意
    summary = ""

    # 出力
    for sentence in result_dict2["summarize_result"]:
        summary += sentence
        summary = "".join(summary.split())

    # 要約文から改行を取り除く
    summary_without_newlines = summary.replace("\n", "")

    # 要約後の文章の長さ
    summary_text_len = len(summary_without_newlines)

    en_summary.append(
        {
            "original_text_len": original_text_len,
            "summary": summary,
            "summary_text_len": summary_text_len,
        }
    )

    print(en_summary)

    return en_summary


# ----------英語→日本語の文章要約(要約の度合いを決めれる)---------- #
def en_to_ja_summary(TEXT, LIMIT):
    LIMIT = float(LIMIT)
    # 空のリストを用意
    summary = []

    # 元の文章の長さ
    original_text_len = len(TEXT)

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
    auto_abstractor.delimiter_list = [".", "\n"]

    # 抽象化&フィルタリングオブジェクト
    abstractable_doc = TopNRankAbstractor()

    # 文書要約（similarity_filter機能追加）
    result_dict2 = auto_abstractor.summarize(TEXT, abstractable_doc, similarity_filter)

    # 空白の文字列を用意
    en_summary = ""

    ##### ----------英語の文章---------- #####

    # 出力
    for sentence in result_dict2["summarize_result"]:
        en_summary += sentence
        en_summary = "".join(en_summary.split())

    # 要約文から改行を取り除く
    en_summary_without_newlines = en_summary.replace("\n", "")

    # 要約後の文章の長さ
    en_summary_text_len = len(en_summary_without_newlines)

    ##### ------------------------------ #####

    ##### ----------日本語に翻訳---------- #####

    dotenv_path = join(dirname(__file__), '.env')

    load_dotenv(dotenv_path)

    DEEPL_API_KEY = os.environ["DEEPL_API_KEY"]

    # APIから翻訳情報を取得
    translator = deepl.Translator(DEEPL_API_KEY)

    ja_summary = translator.translate_text(en_summary, target_lang="JA")

    ja_summary = ja_summary.text

    # 要約文から改行を取り除く
    ja_summary_without_newlines = ja_summary.replace("\n", "")

    # 要約後の文章の長さ
    ja_summary_text_len = len(ja_summary_without_newlines)

    ##### ------------------------------ #####

    summary.append(
        {
            "original_text_len": original_text_len,
            "en_summary": en_summary,
            "summary_text_len": en_summary_text_len,
            "ja_summary": ja_summary,
            "ja_summary_text_len": ja_summary_text_len,
        }
    )

    return summary


# ----------日本語→英語の文章要約(要約の度合いを決めれる)---------- #
def ja_to_en_summary(TEXT, LIMIT):

    # LIMITをfloat型に修正する
    LIMIT = float(LIMIT)

    # 空のリストを用意
    summary = []

    # 元の文章の長さ
    original_text_len = len(TEXT)

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
    result_dict2 = auto_abstractor.summarize(TEXT, abstractable_doc, similarity_filter)

    # 空白の文字列を用意
    ja_summary = ""

    ##### ----------英語の文章---------- #####

    # 出力
    for sentence in result_dict2["summarize_result"]:
        ja_summary += sentence
        ja_summary = "".join(ja_summary.split())

    # 要約文から改行を取り除く
    ja_summary_without_newlines = ja_summary.replace("\n", "")

    # 要約後の文章の長さ
    ja_summary_text_len = len(ja_summary_without_newlines)

    ##### ------------------------------ #####

    ##### ----------日本語に翻訳---------- #####

    load_dotenv()

    DEEPL_API_KEY = os.environ["DEEPL_API_KEY"]

    # APIから翻訳情報を取得
    translator = deepl.Translator(DEEPL_API_KEY)

    en_summary = translator.translate_text(ja_summary, target_lang="EN-US")

    en_summary = en_summary.text

    # 要約文から改行を取り除く
    en_summary_without_newlines = en_summary.replace("\n", "")

    # 要約後の文章の長さ
    en_summary_text_len = len(en_summary_without_newlines)

    ##### ------------------------------ #####

    summary.append(
        {
            "original_text_len": original_text_len,
            "ja_summary": ja_summary,
            "ja_summary_text_len": ja_summary_text_len,
            "en_summary": en_summary,
            "summary_text_len": en_summary_text_len,
        }
    )

    print(summary)
    return summary


# ----------ヤフーニュースの要約(API使用なし)---------- #
def yahoonews_summary(COUNT, LIMIT):

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
    articles = soup_1.select("li.sc-fHCHyC > a")

    for i, article in enumerate(articles, start=1):
        # URLを作成
        article_url = article.get("href")

        # 記事のリクエスト要求
        article_response = requests.get(article_url)

        # 解析
        article_soup = BeautifulSoup(article_response.content, "lxml")

        # 記事全文を読む
        more_articles = article_soup.select_one("p.sc-dyBVLV > a")

        # URLを作成
        more_article_url = more_articles.get("href")

        # 記事のリクエスト要求
        more_article_response = requests.get(more_article_url)

        # 解析
        more_article_soup = BeautifulSoup(more_article_response.content, "lxml")

        # 時間の解析
        article_date = more_article_soup.select("p.sc-gSiFqf > time")

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

        # 記事の内容の解析
        article_contain = more_article_soup.select(".sc-gDyJDg > p")

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
                "article_num": i,
                "article_URL": more_article_url,
                "article_date": article_date,
                "article_title": article_title,
                "article_summary": all_sentence
            }
        )

        print(yahoo_news_list)

        if i == COUNT or i == 8:
            return yahoo_news_list


# ----------ニュースサイト要約(ホームページ用)----------#
def home_news():

    # ニュースを格納する空のリスト
    news_list = []

    # ニュースapiのurl
    url = 'https://newsapi.org/v2/top-headlines'

    # 環境変数からAPIKEYを取得
    load_dotenv()

    NEWS_API_KEY = os.environ["NEWS_API_KEY"]

    # ヘッダーの設置
    headers = {'X-Api-Key': NEWS_API_KEY}

    params = {   
        # 国名
        'country': 'jp',
        # 最大何件取得するか
        'pageSize': 5,
        # 人気のニュースをピックアップ
        'sortBy': 'popularity'
    }

    # リクエストを送信してレスポンスを取得
    response = requests.get(url, headers=headers, params=params)

    # 記事が取得できたか否か
    if response.status_code == 200:
        # JSON形式のデータを取得
        news_data = response.json()
        # 記事を取得
        articles = news_data['articles']

        # 記事を表示
        for article in articles:
            # タイトル
            title = html.escape(article['title'])
            # URL
            url = html.escape(article['url'])
            # 画像のURL
            image_url = html.escape(article['urlToImage'])

            if article['description'] is not None:
                # 記事の内容
                content = html.escape(article['description'])
            else:
                content = '記事が取得できませんでした。'

            # リストに追加
            news_list.append({
                'title': title,
                'url': url,
                'image_url': image_url,
                'content': content
            })

    else:
        news_list.append({
            'title': 'タイトルの取得に失敗しました。',
            'url': 'URLの取得に失敗しました。',
            'image_url': '画像の取得に失敗しました。',
            'content': '記事内容の取得に失敗しました。'
        })
    return news_list


# ----------ニュースサイト要約(検索用)----------#
def search_news(target, sort, count, limit):

    # ニュースを格納する空のリスト
    news_list = []

    # ニュースapiのurl
    url = 'https://newsapi.org/v2/everything'

    # 環境変数からAPIKEYを取得
    load_dotenv()

    NEWS_API_KEY = os.environ["NEWS_API_KEY"]

    # ヘッダーの設置
    headers = {'X-Api-Key': NEWS_API_KEY}

    params = {   
        'q': target,
        'sortBy': sort,
        'pageSize': count
    }

    # リクエストを送信してレスポンスを取得
    response = requests.get(url, headers=headers, params=params)

    # 記事が取得できたか否か
    if response.status_code == 200:
        # JSON形式のデータを取得
        news_data = response.json()
        # 記事を取得
        articles = news_data['articles']

        # 記事を表示
        for article in articles:
            # タイトル
            title = article['title']
            print(title)
            # URL
            url = article['url'] 
            print(url)
            # 画像のURL
            image_url = article['urlToImage'] 
            print(image_url)
            # 記事の内容
            content = article['description'] 

            if content is not None:
                # 文字列に変換（もし必要なら）
                if not isinstance(content, str):
                    content = str(content)

            else:
                content = '記事の取得に失敗しました。'

            # リストに追加
        news_list.append({
            'title': title,
            'url': url,
            'image_url': image_url,
            'content': content
        })
    else:
        news_list.append({
            'title': 'タイトルの取得に失敗しました。',
            'url': 'URLの取得に失敗しました。',
            'image_url': '画像の取得に失敗しました。',
            'content': '記事内容の取得に失敗しました。'
        })
    return news_list
