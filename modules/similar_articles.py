from loguru import logger
import copy

from .singleton import Singleton
from .actions import Actions

class CompareClass(Singleton, Actions):
    pass

class SimilarArticles(CompareClass):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.st_response_json = {
            'status': 'error',
            'err_description': ''
        }
        
    async def __aenter__(self):
        return self
        
    async def _executing(self, text: str) -> dict:
        response_json = copy.deepcopy(self.st_response_json)
        
        try:
            get_articles_response = await self._get_articles(text)
            response_json.update(
                get_articles_response
            )
            
        except (Exception, ) as e:
            response_json['err_description'] = str(e)
            
        finally:
            return response_json
        
    async def __aexit__(self, *args, **kwargs):
        pass
