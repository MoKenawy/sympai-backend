from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from auth.auth_logic import authenticate_user, create_access_token, get_password_hash
from auth.auth_schemes import Token, UserRegisterSchema
from configs import ACCESS_TOKEN_EXPIRE_MINUTES
from dynamo_db.insert_user import insert_user_to_db
from fastapi.middleware.cors import CORSMiddleware


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




auth_app = FastAPI()

# Define the allowed origins (you can limit this to your frontend URL in production)
origins = [
    "http://localhost:3000",  # Your Next.js frontend URL
    "http://127.0.0.1:3000",  # Another form of localhost URL
    "*",
    "https://master.d3qfb4jv3hhifa.amplifyapp.com",  
]

# Apply the CORS middleware
auth_app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included in the request
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow OPTIONS method
    allow_headers=["*"],  # Allow all headers
)



# # --- Middleware for Authentication --- #
# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Check for the Authorization header
#         auth_header = request.headers.get("Authorization")
#         if auth_header:
#             token_type, token = auth_header.split()
#             if token_type.lower() == "bearer":
#                 try:
#                     # Decode and validate the JWT token
#                     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#                     request.state.user = payload  # Attach the user info to the request
#                 except Exception:
#                     return RedirectResponse(url='/test_middleware')  # Redirect to login on token failure
#             else:
#                 return RedirectResponse(url='/test_middleware')  # Redirect to login if token type is invalid
#         else:
#             return RedirectResponse(url='/test_middleware')  # Redirect if the token is missing

#         response = await call_next(request)
#         return response


# # Add middleware to the FastAPI app
# auth_app.add_middleware(AuthMiddleware)



@auth_app.post("/token", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    
    # Set the token in an HTTP-only cookie
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True, 
        secure=True,  # Set True for production to enforce HTTPS
        samesite="Lax"  # or "Strict" depending on your use case
    )

    return {"access_token": access_token, "token_type": "bearer"}


@auth_app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterSchema):
    # Validate password using the custom validator
    try:
        user_data.password = UserRegisterSchema.validate_password(user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Hash the password before storing
    hashed_password = get_password_hash(user_data.password)

    # Insert the user data into DynamoDB
    success = insert_user_to_db(
        username=user_data.username,
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password,
        disabled=user_data.disabled
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user. Please try again later."
        )

    return {"message": "User registered successfully!"}




@auth_app.get("/test_middleware")
async def test_middleware():
    return "Hey there"



