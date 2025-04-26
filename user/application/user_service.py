'''
유저를 저장하는 함수를 user_service.py에서 구현합니다'''

from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository

class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = UserRepository() # 의존성 역전
        self.ulid = ULID()
        
    def create_user(self, name: str, email: str, password: str):
        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=password,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)
        return user