from user.application.send_welcome_email_task import SendWelcomeEmailTask

from fastapi import status, BackgroundTasks
from common.auth import Role, create_access_token
from user.application.email_service import EmailService

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
        email_service: EmailService,
        ulid: ULID,
        crypto: Crypto,
        send_welcom_email_task: SendWelcomeEmailTask,
    ):
        self.user_repo = user_repo # 의존성 주입
        self.ulid = ulid
        self.crypto = crypto # GPT 추가
        self.email_service = email_service
        self.send_welcom_email_task = send_welcom_email_task

    def create_user(
        self,
        # background_tasks: BackgroundTasks,
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
        # background_tasks.add_task(
        #     self.email_service.send_email, user.email
        # )
        SendWelcomeEmailTask().run(user.email)
        self.send_welcom_email_task.delay(user.email)
        
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
    
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = self.user_repo.get_users(page, items_per_page)
        
        return users
    
    def delete_user(self, user_id: str):
        self.user_repo.delete(user_id)
        
    def login(self, email: str, password: str):
        user = self.user_repo.find_by_email(email)
        
        if not self.crypto.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        access_token = create_access_token(
            payload={'user_id': user.id},
            role=Role.USER,
        )
        
        return access_token