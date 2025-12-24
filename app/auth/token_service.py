from app.core.security import create_access_token
from app.schemas.user import LoginResponse, UserRead
from app.models.user import User

def issue_login_response(user: User) -> LoginResponse:
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return LoginResponse(
        access_token=access_token,
        user=UserRead.from_orm(user),
    )
