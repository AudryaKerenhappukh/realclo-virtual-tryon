import os
import time
import jwt
from dotenv import load_dotenv

def encode_jwt_token():
    # Load .env file
    load_dotenv()

    # Read values
    ak = os.getenv("ACCESS_KEY")
    sk = os.getenv("SECRET_KEY")

    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,  # valid 30 min
        "nbf": int(time.time()) - 5
    }
    token = jwt.encode(payload, sk, algorithm="HS256", headers=headers)
    print(f'token: {token}')
    return token if isinstance(token, str) else token.decode("utf-8")

