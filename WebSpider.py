import requests
from bs4 import BeautifulSoup
import random
import time

# 自由時報搜索 URL，搜索關鍵詞為 "外省" 且限定為評論版
base_search_url = "https://search.ltn.com.tw/list?keyword=%E5%A4%96%E7%9C%81&start_time=20041201&end_time=20240719&sort=date&type=all&page=1"

# 保存結果的列表
news_list = []

# 函數：發送請求並隨機延遲
def fetch_url(url):
    delay = random.uniform(20, 35)  # 生成隨機延遲時間，以防止被檢測為爬蟲
    print(f"Delaying for {delay:.2f} seconds...")
    time.sleep(delay)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# 函數：提取每篇文章的標題、連結和發表時間
def extract_article_info(article):
    title_element = article.find('a', class_='tit')
    if not title_element:
        return None, None, None
    
    title = title_element.get_text(strip=True)
    link = title_element['href']
    if not link.startswith("http"):
        link = "https:" + link
    
    cont_div = article.find('div', class_='cont')
    if not cont_div:
        return title, link, "Time not found"
    
    time_element = cont_div.find('span', class_='time')
    time_text = time_element.get_text(strip=True) if time_element else "Time not found"
    
    return title, link, time_text

# 主爬蟲邏輯
for page in range(1, 50):  # 爬取前20~40頁
    search_url = base_search_url.format(page)
    print(f"\nFetching search page {page}: {search_url}")
    
    web = fetch_url(search_url)
    if web is None:
        continue
    
    soup = BeautifulSoup(web.content, "html.parser")
    
    # 找到正確的 ul 元素
    article_list = soup.find('ul', class_='list boxTitle', attrs={'data-desc': '列表'})
    if not article_list:
        print(f"No article list found on page {page}")
        continue
    
    articles = article_list.find_all('li')
    print(f"Found {len(articles)} articles on page {page}")
    
    for index, article in enumerate(articles, start=1 + (page-1)*20):
        title, link, time_text = extract_article_info(article)
        if not title:
            print(f"No title found for article {index}")
            continue
        
        print(f"Processing article {index}: {title}")
        print(f"Article URL: {link}")
        print(f"Published time: {time_text}")
        
        news_list.append({
            'index': index,
            'title': title,
            'link': link,
            'time': time_text,
        })
    
    print(f"Page {page} done")

# 構建輸出字符串
output = ''
for news in news_list:
    output += f"項目：{news['index']}\n"
    output += f"標題：{news['title']}\n"
    output += f"網址：{news['link']}\n"
    output += f"發表時間：{news['time']}\n\n"

print(f"\nTotal articles scraped: {len(news_list)}")
print(output)

# 保存到本地文件
output_file = '/Users/weichiiiiih/Desktop/keyword_mainland.txt'
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Output successfully written to {output_file}")
except IOError as e:
    print(f"Error writing to file: {str(e)}")

print("Scraping process completed")
