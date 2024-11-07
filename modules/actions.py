import aiohttp
import sqlite3
import uuid
from os import getenv
from loguru import logger
from sentence_transformers import SentenceTransformer, util
from thefuzz import fuzz
from torch import Tensor

class Actions:
    def __init__(self, *args, **kwargs):
        self.DATABASE_FILE_NAME = getenv('DATABASE_FILE_NAME', '')
        self.DATABASE_TABLE_NAME = getenv('DATABASE_TABLE_NAME', '')
        
        NEWSAPI_API_KEY = getenv('NEWSAPI_API_KEY', '')
        self.urls = [
            f'https://newsapi.org/v2/everything?apiKey={NEWSAPI_API_KEY}',
            f'https://newsapi.org/v2/top-headlines?apiKey={NEWSAPI_API_KEY}'
        ]
        
        self.connect = None
        self.cursor = None
        
        if all((self.DATABASE_FILE_NAME, self.DATABASE_TABLE_NAME)):
            self.connect = sqlite3.connect(self.DATABASE_FILE_NAME, check_same_thread=False)
            self.cursor = self.connect.cursor()
            
    def _if_similar(self, text1: str, text2: str) -> bool:
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embedding_1: Tensor = model.encode(text1, convert_to_tensor=True)
        embedding_2: Tensor = model.encode(text2, convert_to_tensor=True)

        similarity = util.pytorch_cos_sim(embedding_1, embedding_2)[0][0].item()
        
        if similarity > 0.4:
            return True
            
        return False
        
    async def _get_articles(self, text: str) -> dict:
        response_json = {
            'status': 'error',
            'err_description': ''
        }
        
        connect = self.connect
        cursor = self.cursor
        
        if not all((connect, cursor)):
            response_json['err_description'] = 'One of the DB params is absent!'
            return
        
        try:
            stmt = f'SELECT * from {self.DATABASE_TABLE_NAME};'
            rows = cursor.execute(stmt)
            if not rows:
                response_json['err_description'] = 'Not articles in DB.'
                return response_json
                
            articles = []
            for row in rows:
                title = row[1]
                url = row[2]
                description = row[3]
                result = self._if_similar(title, text) or self._if_similar(description, text)
                if result:
                    articles.append({
                        'title': title,
                        'url': url,
                        'description': description
                    })
            
            response_json['status'] = 'success'
            response_json['articles'] = articles
            
        except (Exception, ) as e:
            response_json['err_description'] = str(e)
            
        finally:
            connect.close()
            return response_json
        
    def _save_in_db(self, articles: list) -> None:
        connect = self.connect
        cursor = self.cursor
        
        if not all((connect, cursor)):
            logger.error('One of the DB params is absent!')
            return
            
        try:
            for article in articles:
                title, url, description = article.get('title'), article.get('url'), article.get('description')
                
                stmt = f'INSERT INTO `{self.DATABASE_TABLE_NAME}` VALUES(?, ?, ?, ?);'
                id = str(uuid.uuid4())
                
                try:
                    cursor.execute(stmt, (id, title, url, description, ))
                    connect.commit()
                    
                except:
                    connect.rollback()
            
        except (Exception, ) as e:
            connect.rollback()
            logger.error(str(e))
        
        finally:
            connect.close()
            return

    async def _send_request(self, *args) -> dict:
        response_json = {
            'status': 'error',
            'err_description': ''
        }
        
        try:
            index, data = args
            if not 0 <= index <= len(self.urls):
                response_json['err_description'] = 'Not found URL index in URLS list.'
                return response_json
                
            url = ''
            if index == 0:
                q, language = data.get('q', 'bitcoin'), data.get('lg', 'en')
                url = f'{self.urls[index]}&q={q}&language={language}'
            elif index == 1:
                category = data.get('category', 'business')
                url = f'{self.urls[index]}&category={category}'
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={}) as request:
                    if request.status not in [200, 201]:
                        response_json['err_description'] = f'NewsAPI get ERROR {request.status}.'
                        return response_json
                        
                    response = await request.json()
                    # logger.debug(response)
            
            status, articles = response.get('status', 'error'), response.get('articles', [])
            if status != 'ok' or not articles:
                response_json['err_description'] = f'NewsAPI return 0 articles.'
                return response_json
        
            articles = [
                {
                    'title': article.get('title', 'NO TITLE'),
                    'url': article.get('url', 'NO URL'),
                    'description': article.get('description', 'NO DESCRIPTION')
                }
                for article in articles[0:10]
            ]
            
            self._save_in_db(articles)
            response_json['status'] = 'success'
            response_json['articles'] = articles
            
        except (Exception, ) as e:
            response_json['err_description'] = str(e)
            
        finally:
            return response_json
