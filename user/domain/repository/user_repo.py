'''
IUserRepository 클래스는 파이썬에서 제공하는 객체지향 인터페이스로 선언하기 위해
ABCMeta 클래스를 이용한다'''

from abc import ABCMeta
from user.domain.user import User

class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError