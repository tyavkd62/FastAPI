from celery.result import AsyncResult
from common.messaging import celery

if __name__ == '__main__':
    async_result = AsyncResult('87136561-f521-45ee-a0ab-ff05b6fb6aad',
                            app=celery)
    result = async_result.result
    
    print(result)