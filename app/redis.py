import redis

redis_client  = redis.Redis(host="redis", port= 6379, db=0, decode_responses=True)

def set_otp(email: str, otp: str, expire: int = 300):
    redis_client.setex(f"otp:{email}", expire, otp)

def get_otp(email:str):
    return redis_client.get(f"otp:{email}")

def delete_otp(email :str):
    redis_client.delete(f"otp:{email}")