# utils.py
from cryptography.fernet import Fernet
from django.conf import settings

cipher = Fernet(settings.ENCRYPTION_KEY)

def encrypt_password(plain_password):
    return cipher.encrypt(plain_password.encode())

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password).decode()
