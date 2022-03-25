import json
from bs4 import BeautifulSoup as BS
import requests
import datetime
import undetected_chromedriver as uc
import time

def get_data(url):

    driver = uc.Chrome()  
    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    driver.close()
    driver.quit()     
    soup = BS(html, "lxml")
    news_card = soup.findAll("a", class_="mg-card__link")
    
    # print(news_card)
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

 
    
    with open("newsliks_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    
    result_data = []   
          
    with open("newsliks_dict.json") as file:
        news_dict = json.load(file)
    
    discr_dict = []
    update_time = datetime.datetime.now()
    for n_url in news_dict[0:10]:
        discr_str= ""
        driver = uc.Chrome()  
        driver.get(n_url.get("url"))
        time.sleep(5)
        r = driver.page_source
        # r = s.get(url=n_url.get("url"), headers=headers)
        soup = BS(r, "lxml")
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
        driver.close()
        driver.quit()
        print(result_data)
    with open("news_dict.json", "w") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def gest_scrab_news():
    # get_data("https://yandex.ru/news?from=tabbar")
     get_data("https://yandex.ru/news/rubric/auto")


# if __name__ == '__main__':
#     main()