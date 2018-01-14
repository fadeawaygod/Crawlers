from requests import get
from bs4 import BeautifulSoup
from datetime import date

PTT_URL = 'https://www.ptt.cc'

def get_web_page(url):
    resp = get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_articles(dom, date_string):
    soup = BeautifulSoup(dom, 'html.parser')

    articles = []  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').string == date_string:  # 發文日期正確
            # 取得推文數
            push_count = 0
            if d.find('div', 'nrec').string:
                try:
                    push_count = int(d.find('div', 'nrec').string)  # 轉換字串為數字
                except ValueError:  # 若轉換失敗，不做任何事，push_count 保持為 0
                    pass

            # 取得文章連結及標題			
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                href = d.find('a')['href']
                title = d.find('a').string
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count
                })
    return articles

def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    links = soup.find(id='main-content').find_all('a')
    tmp_img_urls = []
    for link in links:
        if link['href'].startswith('http://i.imgur.com'):
            tmp_img_urls.append(link['href'])
    return tmp_img_urls


try:
    page = get_web_page('https://www.ptt.cc/bbs/Beauty/index.html')
    if page:
        date = date.today().strftime("%m/%d")
        if date[0] == '0':
            date = ' ' + date[1:]
        articles = get_articles(page, date)
        for post in articles:
            print(post)
    
    for article in articles:
        page = get_web_page(PTT_URL + article['href'])
        if page:
            img_urls = parse(page)
            save(img_urls, article['title'])
            article['num_image'] = len(img_urls)  

except Exception as e:
    print(e)
    pass
