from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer


# ----------英語の文章の要約(要約の度合いを決めれる)---------- #
def En_summary(TEXT, LIMIT=0.5):

    # LIMITをfloat型に修正する
    LIMIT = float(LIMIT)

    # 空のリストを用意
    En_summary = []

    # NLPオブジェクトの初期化
    nlp_base = NlpBase()

    # トークナイザー設定（SimpleTokenizer使用）
    nlp_base.tokenizable_doc = SimpleTokenizer()

    # 区切り文字設定
    nlp_base.delimiter_list = [".", "\n"]

    # 元の文章の文のリスト
    sentence_list = nlp_base.listup_sentence(TEXT)

    # 元の文章の文の数
    num_sentences = len(sentence_list)

    # 自動要約のオブジェクト
    auto_abstractor = AutoAbstractor()

    # トークナイザー設定（SimpleTokenizer使用）
    auto_abstractor.tokenizable_doc = SimpleTokenizer()

    # 区切り文字設定
    auto_abstractor.delimiter_list = [".", "\n"]

    # 抽象化&フィルタリングオブジェクト
    abstractable_doc = TopNRankAbstractor()

    # 要約の文の数を設定
    abstractable_doc.top_n = max(1, int(num_sentences * LIMIT))

    # 文書要約（similarity_filter機能は一旦無効化）
    result_dict2 = auto_abstractor.summarize(TEXT, abstractable_doc)

    # 空白の文字列を用意
    summary = ""

    # 出力する
    for sentence in result_dict2["summarize_result"]:
        summary += sentence.strip() + " "

    # 要約文から余分な空白を取り除く
    summary = " ".join(summary.split())

    # 元の文章と要約後の文章の単語数
    original_text_len = len(TEXT.split())
    summary_text_len = len(summary.split())

    # リスト型を使う
    En_summary.append(
        {
            "original_text_len": original_text_len,
            "summary_text_len": summary_text_len,
            "summary": summary,
        }
    )

    return En_summary
