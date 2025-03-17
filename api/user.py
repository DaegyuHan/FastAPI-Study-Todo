import logging

from database.repository import UserRepository
from fastapi import APIRouter, Depends, HTTPException
from schema.response import UserSchema,JWTResponse
from security import get_access_token

from service.user import UserService
from schema.request import SignUpRequest, SignInRequest, CreateOTPRequest, VerifyOTPRequest
from database.orm import User
from database.repository import UserRepository
from tests.cache import redis_client

logging.basicConfig(level=logging.INFO)


router = APIRouter(prefix="/users")

@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
):
    # 1. request body(username, password)
    # 2. password -> hashing -> hashed_password
    hashed_password: str = user_service.hash_password(plain_password=request.password)
    # 4. user -> db save
    user: User = User.create(username=request.username, hashed_password=hashed_password)
    # 4. user -> db save
    user: User = user_repo.save_user(user=user)
    # 5. return user(id, username)
    return UserSchema.from_orm(user)

@router.post("/sign-in", status_code=200)
def user_sign_in_handler(
        request: SignInRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
):
    # 1. request body(username, password)
    # 2. db reader user
    user: User | None = user_repo.get_user_by_username(username=request.username)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    # 3. user.password, request.password -> bycrept.checkpw
    verified: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password,
    )
    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")
    # 4. create jwt
    access_token: str = user_service.create_jwt(username=user.username)
    # 5. return jwt
    return JWTResponse(access_token=access_token)

@router.post("/email/otp")
def create_otp_handler(
        request: CreateOTPRequest,
        _ = Depends(get_access_token),
        user_service: UserService = Depends(),
):
    otp: int = user_service.create_otp()

    redis_client.set(request.email, otp)
    redis_client.expire(request.email, 3*60)

    return {"otp": otp}

@router.post("/email/otp/verify")
def verify_otp_handler(
        request: VerifyOTPRequest,
        access_token: str = Depends(get_access_token),
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends()
) -> UserSchema:
    otp: str | None = redis_client.get(request.email)
    if not otp:
        raise HTTPException(status_code=400, detail="Bad Request")

    if request.otp != int(otp):
        logging.error(
            "OTP 불일치 - 요청된 OTP: %s (타입: %s), 저장된 OTP: %s (타입: %s)",
            str(request.otp), type(request.otp), str(otp), type(otp)
        )
        raise HTTPException(
            status_code=400,
            detail="Bad Request ( otp 불일치 ) " + str(request.otp) + " != " + str(otp)
        )

    username: str = user_service.decode_jwt(access_token=access_token)

    user: User | None = user_repo.get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    user: User = user.update_email(request.email)

    return UserSchema.from_orm(user)