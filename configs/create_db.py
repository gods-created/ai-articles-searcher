import sqlite3
from os import getenv
import os
from loguru import logger

DATABASE_FILE_NAME = getenv('DATABASE_FILE_NAME')
DATABASE_TABLE_NAME = getenv('DATABASE_TABLE_NAME')

def init() -> None:
    if not os.path.exists(DATABASE_FILE_NAME):
        logger.error('DB file not exists!')
        return
        
    connect = sqlite3.connect(DATABASE_FILE_NAME, check_same_thread=False)
    cursor = connect.cursor()
        
    try:
        stmt = f'CREATE TABLE IF NOT EXISTS `{DATABASE_TABLE_NAME}` (' \
                 'id INT PRIMARY KEY,' \
                 'title VARCHAR(256) NOT NULL UNIQUE,' \
                 'category VARCHAR(256) NOT NULL,' \
                 'content TEXT NULL UNIQUE);'
                 
        cursor.execute(stmt)
        connect.commit()
        
    except (Exception, ) as e:
        logger.error(str(e))
        
    finally:
        return
