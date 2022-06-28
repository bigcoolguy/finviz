import pandas as pd
import requests
from bs4 import BeautifulSoup
from newspaper import Article

def request_url(url):
    headers = {'User-Agent':'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    try:
        res.raise_for_status()
    except:
        print(f'Could not get {url}')
        return None
    return res

def companies():
    url = 'https://www.sec.gov/files/company_tickers.json'
    res = request_url(url)
    df = pd.DataFrame()
    if res is not None:
        data = res.json()
        df = pd.json_normalize(pd.json_normalize(data,max_level=0).values[0])
    return df

class company:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.url = f'https://finviz.com/quote.ashx?t={self.ticker}'
        self.res = res = request_url(self.url)
        self.info = self.quick_info()
        self.soup = BeautifulSoup(self.res.text, features='html.parser')

    def quick_info(self):
        df = pd.DataFrame(columns=['Item','Value'])
        tmp = pd.read_html(self.res.text)[6]
        # TODO: I bet there's a better way to do this but idk what that way is
        items = list(tmp[0])
        values = list(tmp[1])
        for i in range(2,len(tmp)):
            if i % 2 == 0:
                items.extend(list(tmp[i]))
            else:
                values.extend(list(tmp[i]))
        df.Item = items
        df.Value = values
        return df

    def latest_news(self):
        df = pd.DataFrame(columns=['Title','Url'])
        links = self.soup.find_all(class_='tab-link-news')
        for i in range(len(links)):
            info = links[i]
            df.loc[len(df)] = info.text, info['href']
        return df

def get_article(url):
    article = Article(url)
    try:
        article.download()
        article.parse()
        article.nlp()
    except:
        print(f"Unable to get full article info at {url}")
    return article

if __name__ == '__main__':
    ticker = 'icui'
    # TODO: stuff
