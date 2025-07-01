from services.external_api import verify_token

async def authenticate_user(token: str) -> bool:
    data,status = await verify_token(token)
    print(data) #TODO: use logging instead
    return status == 200