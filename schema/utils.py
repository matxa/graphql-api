"""Utility functions ⬇
   [ ▪️ hash_pwd, ▪️ check_pwd ]
"""
import hashlib


def hash_pwd(password):
    """function to hash user's password"""
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_pwd(password, hash):
    """check if password and hash match"""
    if hash_pwd(password) == hash:
        return True
    return False
