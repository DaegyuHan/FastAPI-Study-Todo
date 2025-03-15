from database.repository import UserRepository
from fastapi import APIRouter, Depends
from schema.response import UserSchema

from service.user import UserService
from schema.request import SignUpRequest
from database.orm import User
from database.repository import UserRepository


router = APIRouter(prefix="/users")

@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
):
    # 1. requestbody(username, password)
    # 2. password -> hashing -> hashed_password
    hashed_password: str = user_service.hash_password(plain_password=request.password)
    # 4. user -> db save
    user: User = User.create(username=request.username, hashed_password=hashed_password)
    # 4. user -> db save
    user: User = user_repo.save_user(user=user)
    # 5. return user(id, username)
    return UserSchema.from_orm(user)