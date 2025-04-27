from containers import Container
from fastapi import FastAPI
import uvicorn
'''
FastAPI에서 라우터를 사용하도록 설정합니다'''
from user.interface.controllers.user_controller import router as user_routers
'''
유효성 검사 오류의 상태 코드를 400 Bad Request로 변경하기'''
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

app = FastAPI()
app.container = Container() # 앱을 구동할 때 앞에서 작성한 컨테이너 클래스 등록
app.include_router(user_routers)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )
    
@app.get('/')
def hello():
    return {'Hello': 'FastAPI'}

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', reload=True)