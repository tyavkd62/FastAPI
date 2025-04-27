from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from typing import Annotated

'''
유저를 저장하는 함수를 user_service.py에서 구현합니다'''
from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
'''
유저를 데이터베이스에 저장하기 전에 이미 가입되어 있는 유저인지 검사하는 기능을 구현합니다'''
from fastapi import HTTPException, Depends
'''
유저를 생성할 때 패스워드를 암호화해서 저정하는 기능을 구현합니다'''
from utils.crypto import Crypto

class UserService:
    @inject # 데커레이터를 명시해 주입받은 객체를 사용한다고 선언
    def __init__(
        self,
        user_repo: IUserRepository,
    ):
        self.user_repo = user_repo # 의존성 주입
        self.ulid = ULID()
        self.crypto = Crypto() # GPT 추가

    def create_user(
        self,
        name: str,
        email: str,
        password: str,
        memo: str | None = None
    ):
        _user = None
        
        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e
            
        if _user:
            raise HTTPException(status_code=422)
        
        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),
            created_at=now,
            updated_at=now,
            memo=memo,
        )
        self.user_repo.save(user)
        
        return user
    
    def update_user(
        self,
        user_id: str,
        name: str | None = None,
        password: str | None = None,
    ):
        user = self.user_repo.find_by_id(user_id)
        
        if name:
            user.name = name
        if password:
            user.password = self.crypto.encrypt(password)
        user.updated_at = datetime.now()
        
        self.user_repo.update(user)
        
        return user