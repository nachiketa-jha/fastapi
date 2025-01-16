from fastapi import FastAPI

from container import Container
import routes.users as users
import routes.posts as posts
import routes.user_roles as user_roles
import routes.roles as roles

def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(users.router)
    app.include_router(user_roles.router)
    app.include_router(posts.router)
    app.include_router(roles.router)
    return app


app = create_app()