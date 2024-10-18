from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
db = {
    "kenawy": {
        "username": "kenawy",
        "full_name": "Mohammed Kenawy",
        "email": "test@gmail.com",
        "hashed_password": "$2b$12$ugy0BJRVyEynFX1oUFE/R.IXcjo/XO3YbJ2oD5ufwrXlW28UZbjCO",
        "disabled": False
    }
}
