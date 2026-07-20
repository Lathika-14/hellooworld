from app.auth.jwt_handler import (
    create_access_token,
    verify_access_token
)

data = {
    "user_id": 1,
    "email": "customer@gmail.com",
    "role": "CUSTOMER"
}

token = create_access_token(data)

print("Generated Token:\n")
print(token)

print("\nDecoded Payload:\n")

payload = verify_access_token(token)

print(payload)