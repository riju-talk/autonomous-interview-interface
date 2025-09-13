from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import httpx
from typing import Any, Optional

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.schemas.token import Token, TokenPayload
from app.schemas.user import UserCreate, UserInDB, UserPublic, UserLogin
from app.services.auth_service import auth_service
from app.models.user import User

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Try to authenticate user
    user = await auth_service.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    
    # Set refresh token in HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # days to seconds
        secure=not settings.DEBUG,  # Only send over HTTPS in production
        samesite="lax"
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": access_token_expires.seconds,
        "refresh_token": refresh_token
    }

@router.post("/login/test-token", response_model=UserPublic)
async def test_token(current_user: User = Depends(auth_service.get_current_user)):
    """
    Test access token.
    """
    return current_user

@router.post("/register", response_model=UserPublic)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create new user.
    """
    # Check if user already exists
    user = await User.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system."
        )
    
    # Create new user
    user = await auth_service.create_user(db=db, user_in=user_in)
    
    # Send welcome email (in background)
    # background_tasks.add_task(send_welcome_email, user.email, user.full_name)
    
    return user

@router.post("/login/github")
async def github_login():
    """
    Initiate GitHub OAuth flow.
    """
    if not settings.GITHUB_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth is not configured"
        )
    
    # Redirect to GitHub OAuth page
    oauth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&scope=user:email"
    )
    
    return {"authorization_url": oauth_url}

@router.get("/login/github/callback")
async def github_callback(
    code: str,
    db: AsyncSession = Depends(get_db),
    response: Response = None
) -> Any:
    """
    GitHub OAuth callback.
    """
    if not settings.GITHUB_CLIENT_ID or not settings.GITHUB_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth is not configured"
        )
    
    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            params={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
        )
        
        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get access token from GitHub"
            )
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token received from GitHub"
            )
        
        # Get user info from GitHub
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"},
        )
        
        if user_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from GitHub"
            )
        
        user_data = user_response.json()
        
        # Get primary email
        email_response = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"token {access_token}"},
        )
        
        if email_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user email from GitHub"
            )
        
        emails = email_response.json()
        primary_email = next(
            (email["email"] for email in emails if email.get("primary") and email.get("verified")),
            None
        )
        
        if not primary_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No verified primary email found on GitHub"
            )
        
        # Check if user exists, create if not
        user = await User.get_by_email(db, email=primary_email)
        
        if not user:
            # Create new user
            user_data = {
                "email": primary_email,
                "username": user_data["login"],
                "full_name": user_data.get("name", ""),
                "github_id": user_data["id"],
                "avatar_url": user_data.get("avatar_url"),
                "is_active": True,
            }
            
            user = await User.create(db, **user_data)
        
        # Update last login
        user.last_login = datetime.utcnow()
        await db.commit()
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        # Create refresh token
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = auth_service.create_refresh_token(
            data={"sub": user.email}, expires_delta=refresh_token_expires
        )
        
        # Set refresh token in HTTP-only cookie
        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {refresh_token}",
            httponly=True,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # days to seconds
            secure=not settings.DEBUG,  # Only send over HTTPS in production
            samesite="lax"
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": access_token_expires.seconds,
            "user": user
        }

@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Refresh access token using refresh token from cookie.
    """
    # Get refresh token from cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token found"
        )
    
    # Remove 'Bearer ' prefix if present
    if refresh_token.startswith("Bearer "):
        refresh_token = refresh_token[7:]
    
    try:
        # Verify refresh token
        payload = auth_service.verify_token(refresh_token, settings.REFRESH_TOKEN_SECRET)
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user
        user = await User.get_by_email(db, email=email)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": access_token_expires.seconds
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
def logout(response: Response) -> dict:
    """
    Log out by removing the refresh token cookie.
    """
    response.delete_cookie("refresh_token")
    return {"message": "Successfully logged out"}
