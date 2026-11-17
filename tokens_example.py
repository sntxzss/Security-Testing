import base64
import json
from datetime import datetime, timedelta, timezone
import jwt

SECRET = "dev-secret-change-me-it-must-be-32-bytes-long"  # у житті — з .env
now = datetime.now(timezone.utc)

payload = {"sub": "42", "role": "user", "exp": now + timedelta(minutes=30)}
token = jwt.encode(payload, SECRET, algorithm="HS256")
print("Токен:", token)
# 1) підпис ≠ шифрування: payload читається без жодного секрету
middle = token.split(".")[1]
middle += "=" * (-len(middle) % 4)  # base64 потребує довжину кратну 4
print("Payload без секрету:", json.loads(base64.urlsafe_b64decode(middle)))
# 2) чесна перевірка: підпис і exp
data = jwt.decode(token, SECRET, algorithms=["HS256"])
print("sub:", data["sub"], "role:", data["role"])
# 3) підробка: чужий секрет → підпис не збігається
try:
    jwt.decode(token, "x" * 32, algorithms=["HS256"])
except jwt.InvalidSignatureError:
    print("Підпис не збігається!")
# 4) прострочений токен
old = jwt.encode({"sub": "42", "exp": now - timedelta(seconds=1)}, SECRET)
try:
    jwt.decode(old, SECRET, algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    print("Токен прострочений!")
