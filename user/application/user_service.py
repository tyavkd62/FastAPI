'''
유저를 저장하는 함수를 user_service.py에서 구현합니다'''

from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
'''
유저를 데이터베이스에 저장하기 전에 이미 가입되어 있는 유저인지 검사하는 기능을 구현합니다'''
from fastapi import HTTPException
'''
유저를 생성할 때 패스워드를 암호화해서 저정하는 기능을 구현합니다'''
from utils.crypto import Crypto

class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = UserRepository() # 의존성 역전
        self.ulid = ULID()
        self.crypto = Crypto() # GPT 추가

    def create_user(self, name: str, email: str, password: str):
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
            memo='',
        )
        self.user_repo.save(user)
        
        return user