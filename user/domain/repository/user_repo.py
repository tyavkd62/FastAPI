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