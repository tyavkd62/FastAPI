from example.ch11_01.middleware import create_sample_middleware
from example.ch11_01.context_sample import router as context_ex_router
from example.ch06_02.sync_ex import router as sync_ex_routers
from example.ch06_02.async_ex import router as async_ex_routers

from containers import Container
from middlewares import create_middlewares
from fastapi import FastAPI
import uvicorn
import user.interface.controllers.user_controller
'''
FastAPI에서 라우터를 사용하도록 설정합니다'''
from user.interface.controllers.user_controller import router as user_routers
from note.interface.controllers.note_controller import router as note_routers
'''
유효성 검사 오류의 상태 코드를 400 Bad Request로 변경하기'''
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

container = Container()
container.wire(
    modules=[user.interface.controllers.user_controller]
)

app = FastAPI()
app.container = Container() # 앱을 구동할 때 앞에서 작성한 컨테이너 클래스 등록
app.include_router(user_routers)
app.include_router(sync_ex_routers)
app.include_router(async_ex_routers)
app.include_router(note_routers)
create_sample_middleware(app)
create_middlewares(app)
app.include_router(context_ex_router)

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