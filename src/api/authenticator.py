## Authenticator Class
import jwt
import datetime
import bcrypt
import secrets

## This class is used to authenticate the user and get the jwt token

## it does the following:
## 1. Authenticates the user
## 2. Generates the jwt token
## 3. Returns the jwt token

# Example User Data Class
class UserData:
    def __init__(self, username, password, password_hash):
        self.username = username
        self.password = password
        self.password_hash = password_hash

class Authenticator:
    def __init__(self, user_data : UserData):
        self.username = user_data.username
        self.password = user_data.password
        self.password_hash = user_data.password_hash
    def authenticate_using_email_and_password(self, username, password):
        """Authenticate the user based on the provided username and password."""
        try:
            if username == self.username and bcrypt.checkpw(password.encode('utf-8'), self.password_hash):
                return True
            else:
                raise ValueError("Invalid credentials")
        except TypeError:
            raise ValueError("Invalid credentials")
        except Exception as e:
            raise ValueError("Error authenticating user: {}".format(str(e)))
    @classmethod
    def hash_password (cls, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    



class JWTAuthenticator(Authenticator):
    def __init__(self, user_data, secret_key, algorithm='HS256'):
        super().__init__(user_data)
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.audience = 'http://www.example.com'
    def generate_jwt_token(self, user_data):
        """Generate a JWT token for the authenticated user with flexible user data."""
        expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)  # Token valid for 1 hour
        payload = {
            'sub': user_data.get('username'),  # Include the username from user_data
            'exp': expiration,
        }
        # Add additional claims from user_data
        payload.update(user_data)

        token = jwt.encode(payload, self.secret_key, self.algorithm)
        return token

    def get_jwt_token(self, user_data):
        """Authenticate the user and return a JWT token if successful."""
        username = user_data.get('username')
        password = user_data.get('password')

        if self.authenticate_using_email_and_password(username, password):
            return self.generate_jwt_token(user_data)
        else:
            raise ValueError("Invalid credentials")
    def decode_jwt_token(self, token):
        try:
            # Decode the token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            # Validate the claims
            self.validate_claims(payload)
            return payload  # Return the decoded payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
        except Exception as e:
            raise Exception(f"Error decoding token: {str(e)}")

    def validate_claims(self, payload):
        # Check if the token has expired
        if payload['exp'] < datetime.datetime.now(datetime.UTC).timestamp():
            raise Exception("Token has expired")
        
        # # Check the audience claim
        # if self.audience and payload.get('aud') != self.audience:
        #     raise Exception("Token audience does not match")
        
        

    # Example usage
if __name__ == "__main__":
    user_data = {
        "username": "john_doe",
        "password": "password123",
        "email": "john@example.com",  # Additional user data
        "role": "admin"                # Another custom claim
    }

    secret_key = 'Jou7NCyxpqdhfKzvLhaBkHLxLqA4pG7gEDesu8g7xEY'
    username = user_data.get('username')
    password = user_data.get('password')
    
    ## Fetch hash password from database in real scenario
    password_hash=Authenticator.hash_password(password)

    email_auth_data = UserData(username, password, password_hash)

    authenticator = JWTAuthenticator(email_auth_data, secret_key)

    # Generate a token
    try:
        token = authenticator.get_jwt_token(user_data)
        print(f"Generated Token: {token}")

        # Decode the token
        decoded_payload = authenticator.decode_jwt_token(token)
        print(f"Decoded Payload: {decoded_payload}")
    except Exception as e:
        print(f"Error: {e}")