from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utillities.hash_utils import hash_password, verify_password
from utillities.JWT_TokenHandler import create_access_token, verify_token
from models.user import UserCreate, UserResponse
from database.mongo import user_collection
from bson import ObjectId
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl ="/auth/login") #type: ignore
def get_current_user(token: str = Depends(oauth2_scheme)):
   payload = verify_token(token)
   if not payload:
      raise HTTPException(status_code = 401, detail = "Invalid or expired token")
   user_id = payload.get("sub")
   user = user_collection.find_one({"_id": ObjectId(user_id)})
   if not user:
      raise HTTPException(status_code = 404, detail = "User not found") 
   return user

@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
   return {"email": current_user["sub"]}

                     
@router.post("/signup")
async def signup(user: UserCreate):
  existing_user = await user_collection.find_one({"email": user.email})
  if existing_user:
      raise HTTPException(status_code = 400, detail="Email already regisered")
  user_password = hash_password(user.password)
  user_dict = user.dict()
  user_dict["password"] = user_password
  result = await user_collection.insert_one(user_dict)
  return UserResponse(**{
      "id": str(ObjectId(result.inserted_id)),
      "email": user_dict["email"],
      "full_name": user_dict.get ("full_name"),
      "username": user_dict["username"]
  })


# @router.get("/protected")
# async def protected_route(current_user: dict = Depends(get_current_user)):
#    return {"message": "This is a protected route", "user": current_user}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
   user = await user_collection.find_one({"email": form_data.username})
   if not user or not verify_password(form_data.password,user["password"]):
      raise HTTPException(status_code = 401, detail="Invalid credentials")
   access_token = create_access_token({"sub": str(user["_id"])})
   return {"access_token": access_token, "token_type": "bearer", "user": UserResponse(**{
         "id": str(user["_id"]),
         "email": user["email"],
         "full_name": user.get("full_name"),
         "username": user["username"]
   })}
 

