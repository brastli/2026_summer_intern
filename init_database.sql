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

   DEFAULT CHARACTER SET = 'utf8mb4';