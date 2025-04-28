from dependency_injector.wiring import inject, Provide
from containers import Container

'''
의존성 주입'''
from typing import Annotated
from fastapi import APIRouter, Depends
'''
회원 가입 라우터로 전달된 외부의 요청에 포함돼 있는 본문을 검사하는 기능을 구현합니다'''
from pydantic import BaseModel
'''
유저 생성 유스 케이스 호출'''
from user.application.user_service import UserService

router = APIRouter(prefix='/users') # FastAPI가 제공하는 APIRouter 객체를 생성합니다

class CreateUserBody(BaseModel): # 파이단틱의 BaseModel을 상속받아 파이단틱 모델을 선언합니다
    name: str
    email: str
    password: str

@router.post('', status_code=201, response_model=None) # post 메서드를 이용해 /users 라는 경로로 POST 요청을 받을 수 있습니다
@inject
def create_user(
    user: CreateUserBody, # 요청 매개변수나 본문을 라우터에 전달합니다
    user_service: UserService = Depends(Provide[Container.user_service]),
    # user_service: UserService = Depends(Provide["user_service"]),
):
    created_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return created_user

class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None
    
@router.put("/{user_id}")
@inject
def update_user(
    user_id: str,
    user: UpdateUser,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user = user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password,
    )
    
    return user

@router.get('')
@inject
def get_users(
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    users = user_service.get_users()
    
    return {
        "users": users,
    }