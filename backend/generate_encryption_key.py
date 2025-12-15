"""
Generate encryption key for Sprint 07A
Used to encrypt sensitive integration credentials
"""

from cryptography.fernet import Fernet

print("=" * 60)
print("ENCRYPTION KEY GENERATOR")
print("=" * 60)
print()
print("Generating new encryption key...")
print()

key = Fernet.generate_key()
key_str = key.decode()

print("✅ Key generated successfully!")
print()
print("Add this to your .env file:")
print()
print(f"ENCRYPTION_KEY={key_str}")
print()
print("⚠️  IMPORTANT:")
print("- Keep this key secret")
print("- Never commit it to git")
print("- If you lose it, you won't be able to decrypt existing data")
print("- Use the same key across all environments for the same database")
print()
print("=" * 60)
