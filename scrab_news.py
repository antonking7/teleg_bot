import json
from msvcrt import open_osfhandle
from turtle import update
from bs4 import BeautifulSoup as BS
import requests
import datetime

def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }
    s = requests.session()
    r = requests.get(url=url, headers=headers)

            
    soup = BS(r.text, "lxml")
    news_card = soup.findAll("a", class_="mg-card__link")

    news_dict = []
    
    for news_url in news_card:
        news_url_ = news_url.get("href") #news_url.find("a").get("href")
        news_discription = news_url.text #news_url.find("a").get(">")
        news_dict.append(
            {
                "url": news_url_,
                "title": news_discription
            }
        )

 
    
    with open("news_liks_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    
    result_data = []   
          
    with open("news_liks_dict.json") as file:
        news_dict = json.load(file)
    
    discr_dict = []
    update_time = datetime.datetime.now()
    discr_str = ""
    for n_url in news_dict[0:10]:
        discr_str = ""
        r = s.get(url=n_url.get("url"), headers=headers)
        soup = BS(r.text, "lxml")
        news = soup.findAll(class_="mg-story news-story mg-grid__item") 
        info_url = soup.find("a", class_="mg-story__title-link").get("href")
        info_title = soup.find("a", class_="mg-story__title-link").text.strip()
        info_discr = soup.findAll("div", class_="mg-snippet mg-snippets-group__item")
        for discr in info_discr:
            discr_text = discr.findAll("span",  class_="mg-snippet__text")
            for info in discr_text:
                info_span = info.find("span")
                discr_str += info_span.text
            
        result_data.append(
            {   
            "update_time": str(update_time),
                "url": info_url,
                "title": info_title,
                "discr": discr_str
            }
            )
    print(result_data)
    if result_data:
        with open("news_dict.json", "w") as file:
            json.dump(result_data, file, indent=4, ensure_ascii=False)


def gest_scrab_news():
    # get_data("https://yandex.ru/news?from=tabbar")
    get_data("https://yandex.ru/news/rubric/auto")


# if __name__ == '__main__':
#     main()