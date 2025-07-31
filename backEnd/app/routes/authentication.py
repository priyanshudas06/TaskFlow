from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utillities.hash_utils import hash_password, verify_password
from utillities.authentication_handler import create_access_token, verify_token
from models.user import UserCreate, UserLogin

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl ="/auth/login") #type: ignore
def get_current_user(token: str = Depends(oauth2_scheme)):
   payload = verify_token(token)
   if not payload:
      raise HTTPException(status_code = 401, detail = "Invalid or expired token")
   return payload

@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
   return {"email": current_user["sub"]}

                     
@router.post("/signup")
async def signup(user: UserCreate):
  user_password = hash_password(user.password)

  return {"message": "User successfully created"}

@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
   return {"message": "This is a protected route", "user": current_user}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
   user = {"email": form_data.username, "password": hash_password("123456")}
   if not verify_password(form_data.password,user["password"]):
      raise HTTPException(status_code = 401, detail="Invalid credentials")
   access_token = create_access_token(data={"sub": user["email"]})
   return {"access_token": access_token, "token_type": "bearer"}
 

