from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utilities.hash_utils import hash_password, verify_password
from utilities.JWT_TokenHandler import refreshToken, verify_token, create_access_token
from models.user import UserCreate, UserResponse
from database.mongo import user_collection, task_collection, refresh_token_collection
from models.user import UserProfileWithTasks, RefreshTokenResponse
from bson import ObjectId
from jose import  jwt, JWTError
from datetime import datetime, timedelta

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl ="/auth/login") #type: ignore
async def get_current_user(token: str = Depends(oauth2_scheme)):
   payload = verify_token(token)
   if not payload:
      raise HTTPException(status_code = 401, detail = "Invalid or expired token")
   user_id = payload.get("sub")
   user = await user_collection.find_one({"_id": ObjectId(user_id)})
   if not user:
      raise HTTPException(status_code = 404, detail = "User not found") 
   return user

@router.get("/{username}", response_model=UserProfileWithTasks)
async def read_user_profile(username: str, current_user: dict = Depends(get_current_user)):
   if current_user.get("username") != username:
      raise HTTPException(status_code=403, detail="Not authorized to view this profile")
   
   user_tasks_cursor = task_collection.find({"user_id": str(current_user["_id"])})
   user_tasks = []
   async for task in user_tasks_cursor:
        user_tasks.append(task)

   return UserProfileWithTasks(**{
      "id": str(current_user["_id"]),
      "email": current_user["email"],
      "full_name": current_user.get("full_name"),
      "username": current_user.get("username"),
      "tasks": user_tasks
   })

                     
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

REFRESH_TOKEN_EXPIRE_DAYS = 7
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
   user = await user_collection.find_one({"email": form_data.username})
   if not user or not verify_password(form_data.password,user["password"]):
      raise HTTPException(status_code = 401, detail="Invalid credentials")
   access_token = create_access_token({"sub": str(user["_id"])})
   new_refresh_token = refreshToken({"sub": str(user["_id"])})
   expiry = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
   await refresh_token_collection.insert_one({
      "user_id": str(user["_id"]),
      "refresh_token": new_refresh_token,
      "expiry_at": expiry
   })
   return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer", "user": UserResponse(**{
         "id": str(user["_id"]),
         "email": user["email"],
         "full_name": user.get("full_name"),
         "username": user["username"]
   })}

@router.post("/logout")
async def logout(request: RefreshTokenResponse):
   deleted_token = await refresh_token_collection.delete_one({"refresh_token": request.refresh_token})
   if deleted_token.deleted_count == 0:
      raise HTTPException(status_code=404, detail="Refresh token not found")
   return {"message": "Logged out successfully"}

@router.post("/logoutall")
async def logoutAll(current_user: dict = Depends(get_current_user)):
   deleted_token = await refresh_token_collection.delete_many({"user_id": str(current_user["_id"])})
   if deleted_token.deleted_count == 0:
      raise HTTPException(status_code=404, detail="No active session found")
   return {"message": "Logged out successfully"}

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
@router.post("/refresh")
async def refresh_access_token(request: RefreshTokenResponse):
   try:
      stored_token = await refresh_token_collection.find_one({"refresh_token": request.refresh_token})
      if not stored_token:
         raise HTTPException(status_code=401, detail="Invalid refresh token")
      if stored_token["expiry_at"] < datetime.utcnow():
         raise HTTPException(status_code=401, detail="Refresh token expired")
      payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
      user_id = payload.get("sub")
      if not user_id:
         raise HTTPException(status_code=401, detail="Invalid refresh token")
      user = await user_collection.find_one({"_id": ObjectId(user_id)})
      if not user:
         raise HTTPException(status_code=404, detail="User not found")
      new_access_token = create_access_token({"sub": str(user["_id"])})
      return {"access_token": new_access_token, "token_type": "bearer"}
   except JWTError:
      raise HTTPException(status_code=401, detail="Invalid refresh token")