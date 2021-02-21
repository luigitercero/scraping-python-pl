import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.prensalibre.com/'

XPATH_LINK_TO_ARTICLE = '//article[@class="story-xs story"]/div/a/@href'
XPATH_TITLE = '//h1[@class="sart-title"]/text()'
XPATH_SUMMARY = '//header[@class="sart-header sart-header-wide gi one-whole"]/div[@class="sart-intro"]/p/text()'
XPATH_AUTHOR = '//div[@class="auth-info gi ten-sixteenths"]/p/span/span/text()'
XPATH_DATE = '//div[@class="auth-info gi ten-sixteenths"]/span/a/time/text()'
XPATH_BODY = '//div[@class="sart-content"]/p[not(@class)]/text()'

def parse_notice(link,today):
    try:
      response = requests.get(link)
      if response.status_code == 200:
         notice = response.content.decode('utf-8')
         parsed = html.fromstring(notice)
         try:
            title=parsed.xpath(XPATH_TITLE)[0]
            title = title.replace('\"', "")
            summary=parsed.xpath(XPATH_SUMMARY)[0]
            author=parsed.xpath(XPATH_AUTHOR)[0]
            body=parsed.xpath(XPATH_BODY)
            date=parsed.xpath(XPATH_DATE)[0]
         except IndexError:
            return
         with open(f'{today}/{title}.text','w',encoding='utf-8') as f:
            f.write(title)
            f.write('\n')
            f.write(author)
            f.write('\n')
            f.write(date)
            f.write('\n')
            f.write(summary)
            f.write('\n')
            f.write('\n')
            
            for p in body:
               f.write(p)
               f.write('\n')
      else:
         raise ValueError(f'Error:{response.status_code}') 
    except ValueError as ve:
      print(ve)

def parse_home():
   try:
      response = requests.get(HOME_URL)
      if response.status_code == 200:
         home = response.content.decode('utf-8')
         parsed = html.fromstring(home)
         links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
         #print(links_to_notices)

         today = datetime.date.today().strftime('%d-%m-%Y')
         if not os.path.isdir(today):
            os.mkdir(today)
         for link in links_to_notices:
            parse_notice(link, today)
      else:
         raise ValueError(f'Error:{response.status_code}') 
   except ValueError as ve:
      print(ve)

def run():
   parse_home()

if __name__ == '__main__':
   run()