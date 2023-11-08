import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import requests
import deepl
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.similarityfilter.tfidf_cosine import TfIdfCosine
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer


# ----------日本語の文章の要約---------- #
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


# ----------英語の文章の要約---------- #
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


# ----------英語→日本語の文章要約---------- #
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

    load_dotenv()

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


# ----------日本語→英語の文章要約---------- #
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


# ----------ヤフーニュースの要約---------- #
def yahoonews_summary(COUNT, LIMIT):

    LIMIT = float(LIMIT)
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

        # もっと見る
        more_articles = article_soup.select_one("p.sc-biJonm > a")

        # URLを作成
        more_article_url = article.get("href")

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
            article_date = "記事タイトルが取得できませんでした．"

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

        if i == COUNT or i == 8:
            return yahoo_news_list
