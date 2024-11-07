from loguru import logger
import copy

from .singleton import Singleton
from .actions import Actions

class CompareClass(Singleton, Actions):
    pass

class FetchNews(CompareClass):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.st_response_json = {
            'status': 'error',
            'err_description': ''
        }
        
    async def __aenter__(self):
        return self
        
    async def _executing(self, data: dict) -> dict:
        response_json = copy.deepcopy(self.st_response_json)
        
        try:
            send_request_response = await self._send_request(0, data)
            response_json.update(
                send_request_response
            )
            
        except (Exception, ) as e:
            response_json['err_description'] = str(e)
            
        finally:
            return response_json
        
    async def __aexit__(self, *args, **kwargs):
        pass
