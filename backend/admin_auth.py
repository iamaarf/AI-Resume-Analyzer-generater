import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

import jwt

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordBearer
)

from pwdlib import PasswordHash


load_dotenv()


SECRET_KEY = os.getenv("ADMIN_SECRET_KEY")

ALGORITHM = "HS256"

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

ADMIN_PASSWORD_HASH = os.getenv(
    "ADMIN_PASSWORD_HASH"
)


password_hash = PasswordHash.recommended()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/admin/login"
)


def verify_admin_password(
    password: str
) -> bool:

    if not ADMIN_PASSWORD_HASH:
        return False

    return password_hash.verify(
        password,
        ADMIN_PASSWORD_HASH
    )


def authenticate_admin(
    username: str,
    password: str
) -> bool:

    if username != ADMIN_USERNAME:
        return False

    return verify_admin_password(
        password
    )


def create_admin_token() -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(hours=8)
    )

    payload = {
        "sub": ADMIN_USERNAME,
        "role": "admin",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def login_admin(
    username: str,
    password: str
):

    if not authenticate_admin(
        username,
        password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_admin_token()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_current_admin(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if (
            username != ADMIN_USERNAME
            or role != "admin"
        ):
            raise credentials_exception

        return {
            "username": username,
            "role": role
        }

    except jwt.InvalidTokenError:

        raise credentials_exception