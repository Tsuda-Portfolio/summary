import requests
from bs4 import BeautifulSoup
from transformers import pipeline

def get_bbc_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('h3')
    articles = []

    for headline in headlines:
        if headline.a:
            title = headline.text.strip()
            link = "https://www.bbc.com" + headline.a['href']
            articles.append({'title': title, 'link': link})
    
    return articles

def get_cnn_news():
    url = "https://edition.cnn.com/world"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('h3')
    articles = []

    for headline in headlines:
        if headline.a:
            title = headline.text.strip()
            link = "https://edition.cnn.com" + headline.a['href']
            articles.append({'title': title, 'link': link})
    
    return articles

def search_articles(articles, keyword):
    matching_articles = [article for article in articles if keyword.lower() in article['title'].lower()]
    return matching_articles

def summarize_article(article):
    summarizer = pipeline("summarization")
    response = requests.get(article['link'])
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([para.text for para in paragraphs])
    summary = summarizer(content, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def main():
    news_sources = {
        "1": get_bbc_news,
        "2": get_cnn_news
    }

    print("ニュースサイトを選択してください:")
    print("1: BBCニュース")
    print("2: CNNニュース")
    choice = input("選択 (1/2): ")
    
    if choice in news_sources:
        articles = news_sources[choice]()
        keyword = input("検索したい単語を入力してください: ")

        matching_articles = search_articles(articles, keyword)
        if not matching_articles:
            print("該当するニュースは見つかりませんでした。")
        else:
            for i, article in enumerate(matching_articles):
                print(f"{i+1}: {article['title']} ({article['link']})")
                summary = summarize_article(article)
                print("要約:", summary)
                print()

if __name__ == "__main__":
    main()
