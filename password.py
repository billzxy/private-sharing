from hashlib import md5

def hashPassword(password):
    pass_hash = md5(password.encode())
    return pass_hash.hexdigest()