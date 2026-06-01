from playwright.sync_api import sync_playwright
import time
import re
import random
from mysql_helper import MySqlHelper

def scrape_douban_extreme_bulletproof():
    print("初始化数据库环境")
    db = MySqlHelper('127.0.0.1', 3306, 'root', '12345678', 'study_db')
    db.execute_update("USE study_db;")
    
    print("开启断点续传与深度仿生延迟\n")
    
    existing_records = db.execute_query("SELECT rank_num FROM douban_top100;")
    existing_ranks = [record['rank_num'] for record in existing_records] if existing_records else []
    
    print(f"本地数据库已有 {len(existing_ranks)} 条存活数据，自动跳过这些目标\n")

    insert_sql = """
        INSERT INTO douban_top100 
        (rank_num, title, director, writers, actors, genre, release_year, country, runtime, imdb_id, rating, review_count) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    seeds_queue = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        
        main_page = context.new_page()
        
        main_page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "stylesheet", "media"] else route.continue_())
        
        print(" 收割详情页URL种子")
        for start in range(0, 100, 25):
            main_page.goto(f"https://movie.douban.com/top250?start={start}", wait_until="domcontentloaded")
            time.sleep(2)
            
            items = main_page.query_selector_all('div.item')
            for item in items:
                rank_num = int(item.query_selector('em').inner_text())
                
                if rank_num in existing_ranks:
                    continue
                    
                raw_title = "".join([span.inner_text() for span in item.query_selector_all('.hd span.title, .hd span.other')])
                title = re.sub(r'\s+', ' ', raw_title.replace('\xa0', ' ')).strip()
                rating = float(item.query_selector('.rating_num').inner_text()) if item.query_selector('.rating_num') else 0.0
                review_match = re.search(r'(\d+)人评价', item.inner_text())
                review_count = int(review_match.group(1)) if review_match else 0
                detail_url = item.query_selector('.hd a').get_attribute('href')
                
                seeds_queue.append({
                    'rank_num': rank_num, 'title': title, 'rating': rating, 
                    'review_count': review_count, 'detail_url': detail_url
                })
        
        print(f"过滤掉已存数据后，需要攻坚 {len(seeds_queue)} 个新种子\n")
        success_count = 0
        total_targets = len(seeds_queue)
        
        if total_targets > 0:
            for i, movie in enumerate(seeds_queue, start=1):
                url = movie['detail_url']
                detail_page = None
                
                try:
                    detail_page = context.new_page()
                    detail_page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "stylesheet", "media"] else route.continue_())
                    
                    print(f" [{i:03d}/{total_targets}] 空降  {movie['title'][:15]}...")
                    
                    detail_page.goto(url, wait_until="domcontentloaded", timeout=20000)
                    detail_page.wait_for_selector('#info', timeout=10000) 
                    
                    info_text = detail_page.query_selector('#info').inner_text()
                    
                    dir_match = re.search(r'导演:\s*(.+)', info_text)
                    director = dir_match.group(1).split('\n')[0].strip() if dir_match else "未知"
                    writer_match = re.search(r'编剧:\s*(.+)', info_text)
                    writers = writer_match.group(1).split('\n')[0].strip() if writer_match else "未知"
                    actor_match = re.search(r'主演:\s*(.+)', info_text)
                    actors = actor_match.group(1).split('\n')[0].strip() if actor_match else "未知"
                    genre_match = re.search(r'类型:\s*(.+)', info_text)
                    genre = genre_match.group(1).split('\n')[0].strip() if genre_match else "未知"
                    country_match = re.search(r'制片国家/地区:\s*(.+)', info_text)
                    country = country_match.group(1).split('\n')[0].strip() if country_match else "未知"
                    imdb_match = re.search(r'IMDb:\s*(.+)', info_text)
                    imdb_id = imdb_match.group(1).split('\n')[0].strip() if imdb_match else "未知"
                    year_match = re.search(r'上映日期:\s*(\d{4})', info_text)
                    release_year = int(year_match.group(1)) if year_match else 0
                    runtime_match = re.search(r'片长:\s*(\d+)', info_text)
                    runtime = int(runtime_match.group(1)) if runtime_match else 120 

                    db.execute_update(insert_sql, (
                        movie['rank_num'], movie['title'], director, writers, actors, genre, 
                        release_year, country, runtime, imdb_id, movie['rating'], movie['review_count']
                    ))
                    
                    success_count += 1
                    print(f"     补齐入库")
                    
                except Exception as e:
                    print(f"     被墙或超时 ({type(e).__name__})，已记录失败")
                
                finally:
                    if detail_page:
                        detail_page.close()
                
                sleep_time = random.uniform(5.0, 10.0)
                print(f" 静默 {sleep_time:.1f} 秒...")
                time.sleep(sleep_time)

        browser.close()

    print(f"本次斩获：{success_count} / {total_targets}。")
    db.close()

if __name__ == "__main__":
    scrape_douban_extreme_bulletproof()