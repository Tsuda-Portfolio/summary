import os
from dotenv import load_dotenv

import deepl
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer


# ----------英語→日本語の文章要約(要約の度合いを決めれる)---------- #
def En_to_Ja_summary(TEXT, LIMIT=0.5):

    # LIMITをfloat型に修正
    LIMIT = float(LIMIT)
    
    # 空のリストを用意
    summary = []

    # 元の文章の単語数
    original_word_count = len(TEXT.split())

    # ----------英語の要約---------- #

    # NLPオブジェクトの初期化
    nlp_base = NlpBase()
    
    # トークナイザー設定（SimpleTokenizer使用：英語用）
    nlp_base.tokenizable_doc = SimpleTokenizer()
    
    # 区切り文字設定
    nlp_base.delimiter_list = [".", "\n"]
    
    # 自動要約のオブジェクトの初期化
    auto_abstractor = AutoAbstractor()
    
    # トークナイザー設定（SimpleTokenizer使用：英語用）
    auto_abstractor.tokenizable_doc = SimpleTokenizer()
    
    # 区切り文字設定
    auto_abstractor.delimiter_list = [".", "\n"]
    
    # 抽象化&フィルタリングオブジェクトの設定
    abstractable_doc = TopNRankAbstractor()
    
    # 元の文章の文のリスト
    sentence_list = nlp_base.listup_sentence(TEXT)
    
    # 元の文章の文の数
    num_sentences = len(sentence_list)
    
    # 要約の文の数を設定（最低1文）
    abstractable_doc.top_n = max(1, int(num_sentences * LIMIT))
    
    # 文書要約（similarity_filter機能は無効）
    result_dict = auto_abstractor.summarize(TEXT, abstractable_doc)
    
    # 要約文を結合
    en_summary = " ".join([sentence.strip() for sentence in result_dict["summarize_result"]])
    
    # 要約文から余分な空白を取り除く
    en_summary = " ".join(en_summary.split())
    
    # 要約文から改行を取り除く
    en_summary = en_summary.replace("\n", "")
    
    # 要約後の英語文章の単語数
    en_summary_word_count = len(en_summary.split())

    ##### ------------------------------ #####

    # ----------日本語に翻訳---------- #

    # 環境変数の読み込み
    load_dotenv()
    DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
    
    # DeepLの翻訳オブジェクトの初期化
    translator = deepl.Translator(DEEPL_API_KEY)
    
    # 英語の要約を日本語に翻訳
    ja_summary = translator.translate_text(en_summary, target_lang="JA").text
    
    # 要約文から改行を取り除く
    ja_summary = ja_summary.replace("\n", "")
    
    # 要約後の日本語文章の文字数
    ja_summary_char_count = len(ja_summary)

    ##### ------------------------------ #####

    # 結果を辞書にまとめてリストに追加
    summary.append(
        {
            "original_text_len": original_word_count,
            "En_summary_text_len": en_summary_word_count,
            "Ja_summary_text_len": ja_summary_char_count,
            "En_summary": en_summary,
            "Ja_summary": ja_summary,
        }
    )
    
    return summary
