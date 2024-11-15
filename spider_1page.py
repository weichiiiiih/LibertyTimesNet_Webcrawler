import time
import random
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# China Times search URL for "外省"
base_search_url = "  https://www.chinatimes.com/search/%E7%9C%B7%E6%9D%91?page=46&chdtv   "
keyword = "外省"
encoded_keyword = urllib.parse.quote(keyword)

# List to store results
news_list = []

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Generate a random user agent
ua = UserAgent()
user_agent = ua.random
chrome_options.add_argument(f'user-agent={user_agent}')

# Setup WebDriver using webdriver_manager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

def fetch_url(url):
    delay = random.uniform(10, 15)  # Increased delay
    print(f"Delaying for {delay:.2f} seconds...")
    time.sleep(delay)
    
    driver.get(url)
    
    # Simulate scrolling
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(random.uniform(1, 3))
    
    # Wait for the content to load
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "articlebox-compact"))
        )
    except Exception as e:
        print(f"Timeout waiting for page to load: {e}")
        return None
    
    return driver.page_source

def extract_article_info(article):
    title_element = article.find('h3', class_='title')
    if not title_element:
        return None, None, None, None
    
    title = title_element.get_text(strip=True)
    link = title_element.find('a')['href']
    if not link.startswith("https"):
        link = "https://www.chinatimes.com" + link
    
    time_element = article.find('time')
    if time_element:
        date = time_element.find('span', class_='date').text
        hour = time_element.find('span', class_='hour').text
        time_text = f"{date} {hour}"
    else:
        time_text = "Time not found"
    
    intro_element = article.find('p', class_='intro')
    intro = intro_element.text.strip() if intro_element else "No intro available"
    
    # Extract label (category)
    category_element = article.find('div', class_='category')
    label = category_element.get_text(strip=True) if category_element else "No label available"
    
    return title, link, time_text, label

# Main scraping logic

#頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 
#頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 #頁數 
try:
    for page in range(46,47):  
        search_url = base_search_url.format(encoded_keyword, page)
        print(f"\nFetching search page {page}: {search_url}")
        
        html_content = fetch_url(search_url)
        if not html_content:
            print(f"Failed to fetch page {page}. Skipping...")
            continue
        
        soup = BeautifulSoup(html_content, "html.parser")
        
        articles = soup.find_all('div', class_='articlebox-compact')
        print(f"Found {len(articles)} articles on page {page}")
        
        if not articles:
            print("No articles found. The page might not have loaded correctly.")
            print("Page source:", html_content[:500]) 
            continue
        
        for index, article in enumerate(articles, start=1 + (page-1)*20):
            title, link, time_text, label = extract_article_info(article)
            if not title:
                print(f"No title found for article {index}")
                continue
            
            print(f"Processing article {index}: {title}")
            print(f"Article URL: {link}")
            print(f"Published time: {time_text}")
            print(f"Label: {label}")
            print(f"\n")
            
            news_list.append({
                'index': index,
                'title': title,
                'link': link,
                'time': time_text,
                'label': label
            })
        
        print(f"Page {page} done")
        time.sleep(random.uniform(10, 20))  

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()

#檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名 #檔名
output_file_path = '/Users/weichiiiiih/Desktop/Cword_Cword_village46.txt'

with open(output_file_path, 'w', encoding='utf-8') as f:
    for item in news_list:
        f.write(f"項目：{item['index']}\n")
        f.write(f"標題：{item['title']}\n")
        f.write(f"網址：\n{item['link']}\n")
        f.write(f"發表時間：{item['time']}\n")
        f.write(f"標籤：{item['label']}\n \n")

print("Scraping process completed")