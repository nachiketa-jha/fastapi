from dependency_injector import containers, providers

from database import Database

from repos.users import UserRepository
from services.users import UserService

from repos.posts import PostRepository
from services.posts import PostService

from repos.roles import RoleRepository
from services.roles import RoleService

from repos.user_roles import UserRoleRepository
from services.user_roles import UserRoleService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["routes.users","routes.posts","routes.user_roles","routes.roles"])

    config = providers.Configuration(yaml_files=["config.yml"])

    db = providers.Singleton(Database, db_url=config.db.url)

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    post_repository = providers.Factory(
        PostRepository,
        session_factory=db.provided.session,
    )

    post_service = providers.Factory(
        PostService,
        post_repository=post_repository,
    )

    role_repository = providers.Factory(
        RoleRepository,
        session_factory=db.provided.session,
    )

    role_service = providers.Factory(
        RoleService,
        role_repository=role_repository
    )

    user_role_repository = providers.Factory(
        UserRoleRepository,
        session_factory=db.provided.session,
    )

    user_role_service = providers.Factory(
        UserRoleService,
        user_role_repository=user_role_repository
    )