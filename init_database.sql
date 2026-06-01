CREATE DATABASE IF NOT EXISTS study_db;

USE study_db;

CREATE TABLE student (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    height FLOAT COMMENT '身高'
);

INSERT INTO student (student_id, name, height) VALUES ('202600101', '张三', 160);
INSERT INTO student (student_id, name, height) VALUES ('202600102', '李四', 170);
INSERT INTO student (student_id, name, height) VALUES ('202600103', '王五', 180);

SELECT * FROM student;

UPDATE student SET height = 190.0 WHERE name = '张三';

DELETE FROM student WHERE name = '李四';

USE study_db;
CREATE TABLE IF NOT EXISTS baidu_hot_search (
    rank_num INT PRIMARY KEY COMMENT '热搜排名',
    title VARCHAR(200) NOT NULL COMMENT '热搜标题',
    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '抓取时间'
); 


SELECT * FROM baidu_hot_search;

USE study_db;

DROP TABLE IF EXISTS douban_top100;

CREATE TABLE douban_top100 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rank_num INT NOT NULL COMMENT '排名 (1-100)',
    title VARCHAR(255) NOT NULL COMMENT '电影完整多语种名称',
    director VARCHAR(100) COMMENT '导演',
    writers VARCHAR(255) COMMENT '编剧',       
    actors VARCHAR(500) COMMENT '主演深度名单',
    genre VARCHAR(100) COMMENT '影片类型',
    release_year INT COMMENT '上映年份',
    country VARCHAR(100) COMMENT '国家/地区',
    runtime INT COMMENT '片长(分钟)',            
    imdb_id VARCHAR(50) COMMENT 'IMDb唯一编号', 
    rating FLOAT COMMENT '豆瓣评分',
    review_count INT COMMENT '真实评价人数'
) COMMENT='豆瓣电影 Top 100 深度多维矩阵表';

SELECT * FROM douban_top100;

-- 每次抓取前清空旧数据
TRUNCATE TABLE douban_top100;

   DEFAULT CHARACTER SET = 'utf8mb4';