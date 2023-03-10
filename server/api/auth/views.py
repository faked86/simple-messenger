from fastapi import APIRouter, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from server.db.session import get_session
from server.db.db_models import User
from server.oauth2.core import get_current_user
from server.api.auth.core import create_user, get_token, delete_user
from server.api.api_models import Token, UserIn, UserOut


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    responses={422: {
        "description": "Username is already taken",
    }},
)
async def create_user_view(user: UserIn,
                           db: AsyncSession = Depends(get_session)):
    """Creates user in DB."""
    return await create_user(user, db)


@auth_router.post(
    "/login",
    response_model=Token,
    responses={403: {
        "description": "Invalid Credentials"
    }},
)
async def login_view(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_session),
):
    """Provides access_token and token_type if credentials are right."""
    return await get_token(user_credentials, db)


@auth_router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={401: {
        "description": "Could not validate credentials"
    }},
)
async def delete_user_view(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):
    """
    Deletes user from DB.
    """
    return await delete_user(user, db)
