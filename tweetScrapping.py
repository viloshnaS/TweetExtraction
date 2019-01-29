import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
from textblob import TextBlob


def scrapTweets(url, extract_date):
    print(url)
    csvFile = open('tweets_about_macron.csv', 'a', encoding='utf-8', newline='')
    csvWriter = csv.writer(csvFile)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Create your driver
    driver = webdriver.Chrome("C:\\Users\\User\\AppData\\Roaming\\Python\\Python37\\Scripts\\chromedriver.exe",options=chrome_options)
    # Get a page
    driver.get(url)
    time.sleep(1)
    elem = driver.find_element_by_tag_name("body")
    no_of_pagedowns = 100
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1
    # Feed the source to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    contents = soup.findAll("div", {"class": "content"})


    for content in contents:



        tweet_text = content.find("p", {"class":"tweet-text"})

        if(tweet_text!= None):

            datespan = content.find("span", {"class": "_timestamp"})

            if (datespan != None):
                date = datespan.get_text()

            else:
                date = extract_date

            tt = tweet_text.get_text().replace('\n', ' ').replace('\r', '')
            print(tt)

            sentiment_value = get_tweet_sentiment(tt)
            if sentiment_value > 0:
                sentiment =  'positive'
            elif sentiment_value == 0:
                sentiment = 'neutral'
            else:
                sentiment = 'negative'
            csvWriter.writerow([extract_date,tt,sentiment_value,sentiment])

        print("-------------------------")

def get_tweet_sentiment(tweet):

    analysis = TextBlob(tweet)
    # set sentiment
    return analysis.sentiment.polarity





if __name__ == '__main__':
    f = open("date_list.txt", "r")
    date = (f.readline()).strip()



    while (date != ""):
        dates = date.split(',')
        print(dates[0],dates[1])
        scrapTweets('https://twitter.com/search?q=EmmanuelMacron%20since%3A'+dates[0]+'%20until%3A'+dates[1]+'&amp;amp;amp;amp;amp;amp;lang=fr',dates[0])
        date = (f.readline()).strip()

