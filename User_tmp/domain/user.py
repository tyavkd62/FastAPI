'''
User 도메인 만들기
'''
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    memo: str | None
    created_at: datetime # 생성된 시각
    updated_at: datetime # 갱신된 시각