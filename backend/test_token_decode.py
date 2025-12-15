"""
Test token decoding with both keys
"""
import sys
import os
from jose import jwt, JWTError

sys.path.insert(0, os.path.dirname(__file__))

from src.config.settings import settings

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXItMDAxIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJpYXQiOjE3NjUxMTY0NTgsImV4cCI6MTc2NTEyMDA1OH0.1_42xDSOZX-1D4RQ79LI1IfL3l8xl-dUGgkeZrPXTDY"

print("\n" + "="*60)
print("TOKEN DECODING TEST")
print("="*60)

print("\n1. Trying with SUPABASE_JWT_SECRET...")
try:
    payload = jwt.decode(TOKEN, settings.SUPABASE_JWT_SECRET, algorithms=["HS256"])
    print("   ✅ SUCCESS!")
    print(f"   User ID: {payload.get('sub')}")
    print(f"   Role: {payload.get('role')}")
except JWTError as e:
    print(f"   ❌ FAILED: {e}")

print("\n2. Trying with SECRET_KEY...")
try:
    payload = jwt.decode(TOKEN, settings.SECRET_KEY, algorithms=["HS256"])
    print("   ✅ SUCCESS!")
    print(f"   User ID: {payload.get('sub')}")
    print(f"   Role: {payload.get('role')}")
except JWTError as e:
    print(f"   ❌ FAILED: {e}")

print("\n" + "="*60 + "\n")
