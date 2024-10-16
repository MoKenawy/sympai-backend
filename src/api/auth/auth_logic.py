import datetime
from datetime import timedelta
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

import os
import sys
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))
import init  # noqa: E402, F401

from auth_schemes import TokenData, UserInDB  # noqa: E402
from configs import ALGORITHM, SECRET_KEY  # noqa: E402
from dynamo_db.fetch_user import get_user_by_username  # noqa: E402


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
        user_data = get_user_by_username(username)[0]
        return UserInDB(**user_data)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire =  datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire =  datetime.datetime.now(datetime.UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request):
    """
    Get the current user from the JWT token stored in an HTTP-only cookie.

    If the token is invalid, raises a 401 HTTPException.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        UserInDB: The user represented by the given token.
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract the token from cookies instead of the Authorization header
    token = request.cookies.get("access_token")
    if not token:
        raise credential_exception

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    # Fetch the user by username (this assumes a `get_user` function exists)
    user = get_user(username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

if __name__ == "__main__":
    hashed_password = get_password_hash("2952002")
    print(f"DEBUG hashed_password : {hashed_password}")