from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.similarityfilter.tfidf_cosine import TfIdfCosine
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer


# ----------英語の文章の要約(要約の度合いを決めれる)---------- #
def En_summary(TEXT, LIMIT=0.5):
    # LIMITをfloat型に修正する
    LIMIT = float(LIMIT)

    # 空のリストを用意
    En_summary = []

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

    En_summary.append(
        {
            "original_text_len": original_text_len,
            "summary_text_len": summary_text_len,
            "summary": summary,
        }
    )

    return En_summary
