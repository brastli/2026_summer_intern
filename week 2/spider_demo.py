import requests
from bs4 import BeautifulSoup
from mysql_helper import MySqlHelper

def scrape_baidu_hot_top10():
    print("连接数据库连接")
    db = MySqlHelper('127.0.0.1', 3306, 'root', '12345678', 'study_db')
    
    print("\n请求百度热搜榜")
    url = "https://top.baidu.com/board?tab=realtime"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            hot_items = soup.select('.c-single-text-ellipsis')
            print("Top 10热搜写入数据库\n")
            insert_sql = """
                INSERT INTO study_db.baidu_hot_search (rank_num, title) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE title = VALUES(title), crawl_time = CURRENT_TIMESTAMP
            """
            for i, item in enumerate(hot_items[:10], start=1):
                title = item.text.strip()
                print(f"入库中 -> Top {i:02d} | {title}")
                db.execute_update(insert_sql, (i, title))                
            print("\nTop 10 热搜存入数据库")            
        else:
            print(f"请求失败，状态码: {response.status_code}")           
    except Exception as e:
        print(f"爬虫运行出错: {e}")
    db.close()

if __name__ == "__main__":
    scrape_baidu_hot_top10()