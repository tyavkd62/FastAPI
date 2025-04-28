'''
IUserRepository 클래스는 파이썬에서 제공하는 객체지향 인터페이스로 선언하기 위해
ABCMeta 클래스를 이용한다'''

from abc import ABCMeta, abstractmethod
from user.domain.user import User

class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError
    
    @abstractmethod
    def find_by_email(self, email: str) -> User:
        '''
        이메일로 유저를 검색하고,
        검색한 유저가 없을 경우 422 에러를 발생시킵니다.'''
        raise NotImplementedError
    
    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError
    
    # 유저 목록 조회 기능에 페이징 적용
    @abstractmethod
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        raise NotImplementedError
    
    # 유저 삭제 기능 구현
    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError