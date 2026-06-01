import pymysql

class MySqlHelper:
    def __init__(self, host, port, user, password, database):
        try:
            self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='12345678', 
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor 
            )
            self.cursor = self.conn.cursor()
            print(" 数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {e}")

    def execute_update(self, sql, params=None):
        try:
            affected_rows = self.cursor.execute(sql, params)
            self.conn.commit()
            return affected_rows
        except Exception as e:
            self.conn.rollback() 
            print(f" 执行更新失败，已回滚: {e}")
            return 0

    def execute_query(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"查询失败: {e}")
            return []

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print(" 数据库连接已关闭。")


if __name__ == "__main__":
    print("开始测试 MySqlHelper")
    
    db = MySqlHelper('127.0.0.1', 3306, 'root', '12345678', 'study_db')
    
    print("\n测试查询")
    results = db.execute_query("SELECT * FROM study_db.student") 
    print(f"当前所有学生信息: {results}")
    
    print("\n测试插入")
    insert_sql = "INSERT INTO study_db.student (student_id, name, height) VALUES (%s, %s, %s)"
    affected = db.execute_update(insert_sql, ('20260104', '赵六', 200))
    print(f"成功插入了 {affected} 条数据。")
    
    db.close()