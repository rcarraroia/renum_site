"""
Test settings to verify JWT secret configuration
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.config.settings import settings

print("\n" + "="*60)
print("SETTINGS VERIFICATION")
print("="*60)
print(f"\nSECRET_KEY: {settings.SECRET_KEY[:20]}...")
print(f"SUPABASE_JWT_SECRET: {settings.SUPABASE_JWT_SECRET[:20]}...")
print(f"ALGORITHM: {settings.ALGORITHM}")
print("\n" + "="*60 + "\n")
