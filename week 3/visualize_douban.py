import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mysql_helper import MySqlHelper

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei'] 
plt.rcParams['axes.unicode_minus'] = False                      
plt.style.use('ggplot') 

def generate_extreme_dashboard():
    db = MySqlHelper('127.0.0.1', 3306, 'root', '12345678', 'study_db')
    db.execute_update("USE study_db;")
    
    query_sql = """
        SELECT title, director, release_year, country, genre, rating, review_count, runtime 
        FROM douban_top100;
    """
    results = db.execute_query(query_sql)
    db.close()
    
    if not results:
        print("数据库为空")
        return

    raw_df = pd.DataFrame(results)
    
    raw_df.columns = ['Title', 'Director', 'Year', 'Country', 'Genre', 'Rating', 'ReviewCount', 'Runtime']
    
    raw_df['Year'] = pd.to_numeric(raw_df['Year'], errors='coerce')
    raw_df['Rating'] = pd.to_numeric(raw_df['Rating'], errors='coerce')
    raw_df['ReviewCount'] = pd.to_numeric(raw_df['ReviewCount'], errors='coerce')
    raw_df['Runtime'] = pd.to_numeric(raw_df['Runtime'], errors='coerce').fillna(120) 
    
    df = raw_df[(raw_df['Year'] > 1900) & (raw_df['Rating'] > 0)].dropna().copy()
    fig, axs = plt.subplots(3, 2, figsize=(16, 18))
    fig.suptitle('豆瓣电影 Top 100 数据看板', fontsize=24, fontweight='bold', color='#222222')

    # 1. 评分分布柱状图
    bins = [0, 8.5, 9.0, 9.5, 10.0]
    labels = ['8.5分以下', '8.5–9.0分', '9.0–9.5分', '9.5分以上']
    df['RatingGroup'] = pd.cut(df['Rating'], bins=bins, labels=labels, right=False)
    rating_counts = df['RatingGroup'].value_counts().reindex(labels).fillna(0)
    
    colors_rating = ['#99cc99', '#66bb6a', '#43a047', '#1b5e20']
    bars1 = axs[0, 0].bar(rating_counts.index, rating_counts.values, color=colors_rating, edgecolor='black', width=0.5)
    axs[0, 0].set_title('评分区间分布数量', fontsize=14, fontweight='bold')
    axs[0, 0].set_ylabel('电影数量 (部)')
    for bar in bars1:
        yval = bar.get_height()
        axs[0, 0].text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{int(yval)}部', ha='center', va='bottom', fontsize=10)

    # 2. 年份/年代分布柱状图
    df['Decade'] = (df['Year'] // 10 * 10).astype(int).astype(str) + 's'
    decade_counts = df['Decade'].value_counts().sort_index()
    
    axs[0, 1].bar(decade_counts.index, decade_counts.values, color='#2196F3', edgecolor='black', width=0.6)
    axs[0, 1].set_title('各年代神作上榜数量分布', fontsize=14, fontweight='bold')
    axs[0, 1].set_ylabel('电影数量 (部)')
    axs[0, 1].tick_params(axis='x', rotation=30)
    for x, y in zip(decade_counts.index, decade_counts.values):
        axs[0, 1].text(x, y + 0.3, str(y), ha='center', va='bottom', fontsize=10)

    # 3. 国家/地区分布饼图 
    countries_series = df['Country'].str.split('/').explode().str.strip()
    country_counts = countries_series.value_counts()
    
    top_countries = country_counts.head(5)
    other_countries_sum = country_counts.iloc[5:].sum()
    if other_countries_sum > 0:
        top_countries['其他'] = other_countries_sum
        
    axs[1, 0].pie(top_countries.values, labels=top_countries.index, autopct='%1.1f%%', 
                  startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6'],
                  wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True})
    axs[1, 0].set_title('制片国家/地区上榜频次占比', fontsize=14, fontweight='bold')

    # 4. 类型分布柱状图 
    genres_series = df['Genre'].str.split('/').explode().str.strip()
    genre_counts = genres_series.value_counts().head(10) 
    
    axs[1, 1].barh(genre_counts.index[::-1], genre_counts.values[::-1], color='#FF9800', edgecolor='black', height=0.6)
    axs[1, 1].set_title('上榜率最高电影类型 Top 10', fontsize=14, fontweight='bold')
    axs[1, 1].set_xlabel('出现频次 (部)')

    # 5. 评分 vs 评价人数散点图 
    sc = axs[2, 0].scatter(df['Rating'], df['ReviewCount'] / 10000, 
                           c=df['Year'], cmap='viridis', s=df['Runtime']*0.8, alpha=0.7, edgecolors='black')
    axs[2, 0].set_title('评分 vs 评价人数 (气泡大小代表片长)', fontsize=14, fontweight='bold')
    axs[2, 0].set_xlabel('豆瓣评分')
    axs[2, 0].set_ylabel('评价人数 (万人)')
    cbar = fig.colorbar(sc, ax=axs[2, 0], pad=0.02)
    cbar.set_label('上映年份', rotation=270, labelpad=15)

    # 6.导演出现次数排名
    df['Pure_Director'] = df['Director'].apply(lambda x: x.split(' ')[0].strip() if x else "未知")
    director_counts = df['Pure_Director'].value_counts().head(8)
    
    axs[2, 1].bar(director_counts.index, director_counts.values, color='#9C27B0', edgecolor='black', width=0.4)
    axs[2, 1].set_title('上榜作品最多导演 Top 8', fontsize=14, fontweight='bold')
    axs[2, 1].set_ylabel('作品数量 (部)')
    axs[2, 1].tick_params(axis='x', rotation=15)
    for x, y in zip(director_counts.index, director_counts.values):
        axs[2, 1].text(x, y + 0.1, f'{y}部', ha='center', va='bottom', fontsize=10)

    

    plt.tight_layout()
    plt.subplots_adjust(top=0.92, hspace=0.35) 
    plt.show()

if __name__ == "__main__":
    generate_extreme_dashboard()