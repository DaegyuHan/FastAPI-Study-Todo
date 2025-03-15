import bcrypt
from jose import jwt
from datetime import datetime, timedelta


class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "3a86045e90623055658008024ff4e09577f177f9a5173c9eb4ac39223a675d21"
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hashed_password=bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {
                "sub": username,    # unique id
                "exp": datetime.now() + timedelta(days=1),  # 시간 하루 유효
            },
            self.secret_key,
            algorithm=self.jwt_algorithm)

    def decode_jwt(self, access_token: str):
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        # expire
        return payload["sub"]   # username