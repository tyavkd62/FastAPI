from fastapi import FastAPI
import uvicorn
'''
FastAPI에서 라우터를 사용하도록 설정합니다'''
from user.interface.controllers.user_controller import router as user_routers

app = FastAPI()
app.include_router(user_routers)

@app.get('/')
def hello():
    return {'Hello': 'FastAPI'}

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', reload=True)
