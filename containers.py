from dependency_injector import containers, providers
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['user'], # 의존성을 주입할 모듈 선언
    )
    
    user_repo = providers.Factory(UserRepository)
    '''
    UserService 객체를 생성할 팩토리를 제공합니다.
    이때, UserService 생성자로 전달될 user_repo 객체 역시 컨테이너에 있는 팩토리로 선언합니다
    '''
    user_service = providers.Factory(UserService, user_repo=user_repo)