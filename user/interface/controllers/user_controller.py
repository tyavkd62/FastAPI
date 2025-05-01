from common.auth import get_admin_user
from common.auth import CurrentUser, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

from datetime import datetime

from dependency_injector.wiring import inject, Provide
from containers import Container

'''
의존성 주입'''
from typing import Annotated
from fastapi import APIRouter, Depends
'''
회원 가입 라우터로 전달된 외부의 요청에 포함돼 있는 본문을 검사하는 기능을 구현합니다'''
from pydantic import BaseModel, EmailStr, Field
'''
유저 생성 유스 케이스 호출'''
from user.application.user_service import UserService

router = APIRouter(prefix='/users') # FastAPI가 제공하는 APIRouter 객체를 생성합니다

class CreateUserBody(BaseModel): # 파이단틱의 BaseModel을 상속받아 파이단틱 모델을 선언합니다
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    
class GetUserResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]
    
    
@router.post('', status_code=201) # post 메서드를 이용해 /users 라는 경로로 POST 요청을 받을 수 있습니다
@inject
def create_user(
    user: CreateUserBody, # 요청 매개변수나 본문을 라우터에 전달합니다
    user_service: UserService = Depends(Provide[Container.user_service]),
    # user_service: UserService = Depends(Provide["user_service"]),
) -> UserResponse:
    created_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return created_user

class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)
    
@router.put("", response_model=UserResponse)
@inject
def update_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user = user_service.update_user(
        user_id=current_user.id,
        name=body.name,
        password=body.password,
    )
    
    return user


@router.get('')
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_admin_user),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> GetUserResponse:
    total_count, users = user_service.get_users(page, items_per_page)
    
    return {
        "total_count": total_count,
        "page": page,
        "users": users,
    }


@router.delete("", status_code=204)
@inject
def delete_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user_service.delete_user(current_user)
    

@router.post('/login')
@inject
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    access_token = user_service.login(
        email=form_data.username,
        password=form_data.password,
    )
    
    return {'access_token': access_token, 'token_type': 'bearer'}
