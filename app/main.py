from fastapi import FastAPI
from app.routes import users, auth, org, login
from app.database import Base, engine

# ✅ Create the database tables
Base.metadata.create_all(bind=engine)

# ✅ Create FastAPI instance
app = FastAPI(title="User Management API", version="1.0")

# ✅ Include API routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(org.org, prefix="/org", tags=["Organization"])
app.include_router(auth.auth, tags=["Auth"])

