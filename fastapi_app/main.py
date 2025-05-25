import os
from fastapi import FastAPI, APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database imports
from database import Base, engine

# Import models to ensure they're registered with SQLAlchemy
import models

# Import router modules
from sanctions.routes import sanction_router

# Initialize FastAPI app
screening_app = FastAPI(
    title="Store API",
    version="1.0.0",
    description="API documentation for Store API"
)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Root endpoint
@screening_app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Store"}

# Setup versioned API router and include module routers
api_router = APIRouter(prefix="/v1")
api_router.include_router(sanction_router)

# Register the master router with the app
screening_app.include_router(api_router)

# Setup OAuth2 scheme for Swagger UI login flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

# Custom OpenAPI schema with security configuration
def custom_openapi():
    if screening_app.openapi_schema:
        return screening_app.openapi_schema

    openapi_schema = get_openapi(
        title=screening_app.title,
        version=screening_app.version,
        description=screening_app.description,
        routes=screening_app.routes,
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]

    screening_app.openapi_schema = openapi_schema
    return screening_app.openapi_schema

screening_app.openapi = custom_openapi

# Run the app using Uvicorn when executed directly
if __name__ == "__main__":
    port = os.environ.get("DB_PORT")
    if not port:
        raise EnvironmentError("PORT environment variable is not set")
    uvicorn.run("fastapi_app.main:app", host="0.0.0.0", port=int(port), reload=False)