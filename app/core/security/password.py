import bcrypt



async def hashed_password(password: str) -> str:
     return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()



async def check_password(password: str, old_password: str) -> bool:
     return bcrypt.checkpw(password.encode(), old_password.encode()) 


def sync_hashed_password(password: str) -> str:
     return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()