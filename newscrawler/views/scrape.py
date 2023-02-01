from bs4 import BeautifulSoup
import requests
# from requests_html import HTMLSession

def change_view(all_result, companies):
  new_all_result = []
  for company in companies:
    for result in all_result:
      if result["company"] == company:
        new_all_result.append(result)
  return new_all_result

def scrape(sources, companies, number, groupbysource):
  number = int(number)
  all_result = []
  result = {}


  if "Forbes" in sources:
    for query in companies:
        website = "https://www.forbes.com/search/?q="
        URL = website + query
        source = requests.get(URL).text
        soup = BeautifulSoup(source, 'html5lib')
        article = soup.find_all('div', class_= "stream-item__text")[:number]
        for stream_text in article:
            try:
              result = {}
              result["company"] = query
              result["source"] = 'Forbes'
              headline = stream_text.h3.a.text
              result["headline"] = headline
              # print(headline)
              url = stream_text.h3.a["href"]
              result["url"] = url
              # print(url)
              date = stream_text.find('div', class_="stream-item__date").text
              result['date'] = date
              # print(date)
              summary = stream_text.find('div', class_="stream-item__description").text
              result['summary'] = summary
              # print(summary)
              all_result.append(result)
            except:
              pass

  if "Chicago Tribune" in sources:
    for query in companies:
        website = "https://chicagotribune.search.yahoo.com/search?p="
        URL = website + query
        source = requests.get(URL).text
        soup = BeautifulSoup(source, 'html5lib')
        articles = soup.find_all('li', class_="ov-a mt-0 pt-26 pb-26 bt-dbdbdb")[:number]
        for article in articles:
            try:
              result = {}
              result["company"] = query
              result["source"] = 'Chicago Tribune'
              headline = article.h4.text
              result["headline"] = headline
              # print(headline)
              url = article.h4.a["href"]
              result["url"] = url
              # print(url)
              date = article.find('div', class_="mt-10 fz-13").p
              date = date.find_all('span')[2].text
              result["date"] = date
              # print(date)
              summary = article.p.text
              result["summary"] = summary
              # print(summary)
              all_result.append(result)
            except:
              pass

  if "BBC News" in sources:
    for query in companies:
        website = "https://www.bbc.co.uk/search?q="
        URL = website + query
        source = requests.get(URL).text
        soup = BeautifulSoup(source, 'html5lib')
        articles = soup.find_all('div', class_="ssrcss-11rb3jo-Promo ett16tt0")[:number]
        # print(articles)
        for article in articles:
            try:
              result = {}
              result["company"] = query
              result["source"] = 'BBC News'
              headline = article.find('div', class_="ssrcss-1cbga70-Stack e1y4nx260").p.text
              result["headline"] = headline
              # print(headline)
              url = article.find('div', class_="ssrcss-1cbga70-Stack e1y4nx260").a["href"]
              result['url'] = url
              # print(url)
              date = article.find('div', class_="ssrcss-1tha3dg-Stack e1y4nx260")
              date = date.find('span', class_="ssrcss-8g95ls-MetadataSnippet ecn1o5v2").text
              result['date'] = date
              # print(date)
              summary = article.find('p', class_="ssrcss-1q0x1qg-Paragraph eq5iqo00").text
              result['summary'] = summary
              # print(summary)
              all_result.append(result)
            except:
              pass

  if "USA TODAY" in sources:
    for query in companies:
        website = "https://www.usatoday.com/search/?q="
        website_url = "https://www.usatoday.com"
        URL = website + query
        source = requests.get(URL).text
        soup = BeautifulSoup(source, 'html5lib')
        articles = soup.find_all('a', class_="gnt_se_a gnt_se_a__hd gnt_se_a__hi")[:number]
        for article in articles:
            try:
              result = {}
              result["company"] = query
              result["source"] = "USA TODAY"
              headline = article.text
              result['headline'] = headline
              # print(headline)
              summary = article['data-c-desc']
              result['summary'] = summary
              # print(summary)
              date_source = article.find('div', "gnt_se_th_by gnt_sbt gnt_sbt__ms gnt_sbt__ts")
              date = ""
              if date_source is not None:
                  date = date_source['data-c-dt']
              result['date'] = date
              # print(date)
              url = website_url + article['href']
              result['url'] = url
              # print(url)
              all_result.append(result)
            except:
              pass

  if "The New York Times" in sources:
    for query in companies:
        website = "https://www.nytimes.com/search?query="
        website_url = "https://www.nytimes.com"
        URL = website + query
        source = requests.get(URL).text
        soup = BeautifulSoup(source, 'html5lib')
        articles = soup.find_all('div', class_ = 'css-1bdu3ax')[:number]
        for article in articles:
            try:
              result = {}
              result["company"] = query
              result['source'] = 'The New York Times'
              headline = article.h4.text
              result["headline"] = headline
              # print(headline)
              url = website_url + article.a["href"]
              result["url"] = url
              # print(url)
              # date = article.find('span').text
              # result["date"] = date
              # print(date)
              summary = article.find('p', class_="css-16nhkrn").text
              result["summary"] = summary
              # print(summary)
              all_result.append(result)
            except:
              pass


  if "The Economist" in sources:
      for query in companies:
          website = "https://www.economist.com/search?q="
          URL = website + query
          source = requests.get(URL).text          
          soup = BeautifulSoup(source, 'html5lib')
          article = soup.find_all('li', class_="_result-item")[:number]
          for stream_text in article:
              try:
                result = {}
                result["company"] = query
                result["source"] = "The Economist"
                headline = stream_text.find('span', class_="_headline").text
                result["headline"] = headline
                url_text = stream_text.find('div', class_="css-1ehrfcr e1k9lotg0")
                url = url_text.a['href']
                result["url"] = url
                context = url_text.a.p.text
                date = context.split('...')[0]
                description = context.split('... ')[1]
                result["date"] = date
                result["summary"] = description
                all_result.append(result)
              except:
                pass

  if "Investopedia" in sources:
    for query in companies:
        website = "https://www.investopedia.com/search?q="
        URL = website + query
        source = requests.get(URL).text
        soup = BeautifulSoup(source, 'html5lib')
        article = soup.find_all('div', class_="comp search-results__list mntl-block")[:number]
        for stream_text in article:
            try:
              result = {}
              result["company"] = query
              headline = stream_text.a.h3.text.strip()
              result["source"] = 'Investopedia'
              result["headline"] = headline
              url = stream_text.a["href"]
              result["url"] = url
              description = stream_text.find('div', class_="comp search-results__description mntl-text-block").text.strip()
              result["summary"] = description
              result["date"] = ""
              all_result.append(result)
            except:
              pass


  if "TheStreet" in sources:
    for query in companies:
        website = "https://www.thestreet.com/search?query="
        URL = website + query
        source = requests.get(URL).text
        soup = BeautifulSoup(source, 'html5lib')
        article = soup.find_all('div', class_="l-grid--item")[2:number+2]
        for stream_text in article:
            try:
              result = {}
              result["company"] = query
              headline = stream_text.find('div', class_="m-card--content").a.h2.text
              result["source"] = 'TheStreet'
              result["headline"] = headline
              url = stream_text.find('div', class_="m-card--content").a["href"]
              result["url"] = url
              date = stream_text.find('div',class_="m-card--metadata-b").span.text
              result["date"] = date
              result["summary"] = ""
              all_result.append(result)
            except:
              pass
           

  if "The New Yorker" in sources:
      for query in companies:
          website = "https://www.newyorker.com/search/q/"
          URL = website + query
          source = requests.get(URL).text  
          soup = BeautifulSoup(source, 'html5lib')
          article = soup.find_all('li', class_="River__riverItem___3huWr")[:number]
          for stream_text in article:
              try:
                result = {}
                result["company"] = query
                headline = stream_text.find('h4', class_="River__hed___re6RP").text
                result["source"] = 'The New Yorker'
                result["headline"] = headline
                url= stream_text.findAll('a')[2]["href"]
                url = "https://www.newyorker" + url
                result["url"] = url
                summary = stream_text.find('h5',class_="River__dek___CayIg").text
                result["summary"] = summary
                date = stream_text.find('h6', class_="River__publishDate___1fSSK").text
                result["date"] = date
                all_result.append(result)
              except:
                  pass

  if "The Wall Street Journal" in sources:
      session = HTMLSession()
      for query in companies:         
          website = "https://www.wsj.com/search?query="
          URL = website + query
          r = session.get(URL)
          r.html.render(sleep=1, scrolldown=5)
          articles = r.html.find('article')[:number]
          for item in articles:
              try:
                  result = {}
                  result["company"] = query
                  headline = item.find('span', first=True).text
                  description = item.find('p', first=True).text
                  url = list(item.find('h3', first=True).absolute_links)[0]
                  date_all = item.find('p')
                  date = date_all[len(date_all)-1].text
                  result["source"] = 'The Wall Street Journal'
                  result["headline"] = headline
                  result["summary"] = description
                  result["date"] = date
                  result["url"] = url
                  all_result.append(result)                
              except:
                  pass
  if groupbysource == 0:
    all_result = change_view(all_result, companies)
  return all_result

# if __name__ == '__main__':
#   sources = ['BBC News']
#   number = 1
#   companies = ['zoom', 'netflix']
#   print(scrape(sources, companies, number, 1))