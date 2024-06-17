import sqlite3
from sqlite3 import Error
import os.path
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s %(message)s")

class RandomCoffeeDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        # cursor.execute('''CREATE TABLE IF NOT EXISTS anketa
        #               (id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                name TEXT NOT NULL,
        #                telegram_username TEXT NOT NULL,
        #                page_link TEXT NOT NULL,
        #                sphere_of_work TEXT NOT NULL,
        #                profession TEXT NOT NULL,
        #                interests TEXT NOT NULL,
        #                birthdate TEXT NOT NULL,
        #                expectation TEXT NOT NULL,
        #                format TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS profile
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telegram_id INTEGER UNIQUE,
                        name TEXT NOT NULL,
                        telegram_name TEXT NOT NULL,
                        job_area TEXT NOT NULL,
                        hobby TEXT NOT NULL,
                        motivation TEXT NOT NULL,
                        format TEXT NOT NULL)''')
        self.conn.commit()

    def create_matching_db():
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS matiching
                        (profile1 INTEGER,
                        profile2 INTEGER,
                        is_offered: BOOLING,
                        format: INTEGER,
                        motivation: INTEGER,
                        job_score: INTEGER,
                        hobby_score: INTEGER
                        PRIMARY KEY (profile1, profile2)
                        )
                        ''')
        self.conn.commit()
    

    def insert_data(self, telegram_id, name, telegram_name, job_area, hobby, motivation, format):
        cursor = self.conn.cursor()
        # cursor.execute("INSERT INTO anketa (name, telegram_username, page_link, sphere_of_work, profession, interests, birthdate, expectation, format) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        #                (name, telegram_username, page_link, sphere_of_work, profession, interests, birthdate, expectation, format))
        cursor.execute(f"INSERT OR REPLACE INTO profile (id, telegram_id, name, telegram_name, job_area, hobby, motivation, format) VALUES \
                        ((select ID from profile where telegram_id ={telegram_id}), ?, ?, ?, ?, ?, ?, ?)",
                       (telegram_id, name, telegram_name, job_area, hobby, motivation, format))        
        self.conn.commit()
        logging.info(f"Safe profile {telegram_name} ({telegram_id})")

# 1287278626
    def get_all_data(self):
        keys = ["telegram_id", "name", "telegram_name", "job_area", "hobby", "motivation", "format"]
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM profile")
        rows = cursor.fetchall()
        data = {}
        for row in rows:
            data[row[0]]={k: v for k, v in zip(keys, row[1:])}
        return data
    
    def get_profile(self, telegram_id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM profile WHERE telegram_id={telegram_id};")
        profile = cursor.fetchall()

        logging.info(f"Profile: {profile}")
        return ({} if not profile else profile[0])

    def get_persons_by_format(self, format: str):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM profile WHERE format={format}")
        profile = cursor.fetchall()
        return ({} if not profile else profile[0])
    
    def full_db(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO profile (telegram_id, name, telegram_name, job_area, hobby, motivation, format)
VALUES
    (1234567896, 'Eve Peterson', 'evepeterson', 'UX designer', 'photography', 50, 'online'),
    (1234567897, 'Frank Davis', 'frankdavis', 'technical writer', 'fishing', 100, 'offline'),
    (1234567898, 'Grace Miller', 'gracemiller', 'marketing specialist', 'dancing', 0, 'both'),
    (1234567899, 'Harry Moore', 'harrymoore', 'sales manager', 'gardening', 50, 'online'),
    (1234567900, 'Irene Taylor', 'irenetaylor', 'HR manager', 'painting', 100, 'offline'),
    (1234567901, 'Jack White', 'jackwhite', 'finance analyst', 'swimming', 0, 'both'),
    (1234567902, 'Kate Green', 'kategreen', 'business analyst', 'yoga', 50, 'online'),
    (1234567903, 'Larry Hall', 'larryhall', 'DevOps engineer', 'running', 100, 'offline'),
    (1234567904, 'Mia Thompson', 'miathompson', 'product manager', 'cycling', 0, 'both'),
    (1234567905, 'Noah Clark', 'noahclark', 'QA engineer', 'baking', 50, 'online'),
    (1234567890, 'John Doe', 'johndoe', 'software engineer', 'reading', 50, 'online'),
    (1234567891, 'Jane Smith', 'janesmith', 'data analyst', 'hiking', 100, 'offline'),
    (1234567892, 'Bob Johnson', 'bobjohnson', 'project manager', 'gaming', 0, 'both'),
    (1234567893, 'Alice Williams', 'alicewilliams', 'graphic designer', 'music', 50, 'online'),
    (1234567894, 'Charlie Brown', 'charliebrown', 'web developer', 'cooking', 100, 'offline'),
    (1234567895, 'Dave Wilson', 'davewilson', 'system administrator', 'traveling', 0, 'both'),
    (1234567906, 'Olivia King', 'oliviaking', 'frontend developer', 'reading', 50, 'online'),
    (1234567907, 'Peter Lee', 'peterlee', 'backend developer', 'hiking', 100, 'offline'),
    (1234567908, 'Quinn Walker', 'quinnwalker', 'fullstack developer', 'gaming', 0, 'both'),
    (1234567909, 'Rachel Young', 'rachelyoung', 'data scientist', 'music', 50, 'online'),
    (1234567910, 'Samuel Adams', 'samueladams', 'machine learning engineer', 'cooking', 100, 'offline'),
    (1234567911, 'Taylor Brooks', 'taylorbrooks', 'mobile developer', 'traveling', 0, 'both'),
    (1234567912, 'Uma Patel', 'umapatel', 'network engineer', 'photography', 50, 'online'),
    (1234567913, 'Victor Kim', 'victorkim', 'database administrator', 'fishing', 100, 'offline'),
    (1234567914, 'Whitney Lane', 'whitneylane', 'security analyst', 'dancing', 0, 'both'),
    (1234567915, 'Xavier Ramirez', 'xavierramirez', 'project coordinator', 'gardening', 50, 'online'),
    (1234567916, 'Yasmine Carter', 'yasminecarter', 'technical support', 'painting', 50, 'online'),
    (1234567917, 'Zachary Turner', 'zacharyturner', 'system engineer', 'swimming', 100, 'offline'),
    (1234567918, 'Alexandra Phillips', 'alexandraphillips', 'content writer', 'yoga', 0, 'both'),
    (1234567919, 'Benjamin Harris', 'benjaminharris', 'scrum master', 'running', 50, 'online'),
    (1234567920, 'Catherine Anderson', 'catherineanderson', 'product owner', 'cycling', 100, 'offline'),
    (1234567921, 'Dennis Nelson', 'dennisnelson', 'business developer', 'baking', 0, 'both'),
    (1234567922, 'Emily Garcia', 'emilygarcia', 'marketing manager', 'reading', 50, 'online'),
    (1234567923, 'Frederick Scott', 'frederickscott', 'sales director', 'hiking', 100, 'offline'),
    (1234567924, 'Grace Sullivan', 'gracesullivan', 'HR director', 'gaming', 0, 'both'),
    (1234567925, 'Henry Thompson', 'henrythompson', 'finance manager', 'music', 50, 'online');
            """
        )
        self.conn.commit()
