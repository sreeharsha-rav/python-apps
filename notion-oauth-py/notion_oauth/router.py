"""FastAPI router for Notion OAuth endpoints."""
import logging
import time
from typing import Annotated
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from authlib.common.security import generate_token

from .service import (
    discover_oauth_metadata,
    register_client,
    create_authorization_url,
    exchange_code_for_tokens,
    refresh_access_token
)
from .storage import save_tokens, load_tokens, delete_tokens

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["OAuth"])

NOTION_MCP_SERVER_URL = "https://mcp.notion.com"


@router.get("/login")
async def login(request: Request):
    """
    Initiate OAuth flow.
    
    Steps:
    1. Discover OAuth metadata
    2. Register dynamic client
    3. Generate PKCE values
    4. Store state in session
    5. Redirect to Notion authorization endpoint
    """
    try:
        # Get redirect URI (construct from request)
        redirect_uri = str(request.url_for('callback'))
        
        # 1. Discover OAuth Metadata
        metadata = discover_oauth_metadata(NOTION_MCP_SERVER_URL)
        
        # 2. Dynamic Client Registration
        credentials = register_client(metadata, redirect_uri)
        
        # 3. Generate state for CSRF protection
        state = generate_token(32)
        
        # 4. Create authorization URL with PKCE
        auth_url, code_verifier = create_authorization_url(
            metadata=metadata,
            client_id=credentials.client_id,
            redirect_uri=redirect_uri,
            state=state,
            scopes=[]
        )
        
        # 5. Store values in session for callback
        request.session['oauth_state'] = state
        request.session['code_verifier'] = code_verifier
        request.session['client_id'] = credentials.client_id
        request.session['client_secret'] = credentials.client_secret
        request.session['token_endpoint'] = metadata.token_endpoint
        
        logger.info(f"Redirecting to Notion authorization: {auth_url[:50]}...")
        
        # Redirect user to Notion
        return RedirectResponse(url=auth_url)
        
    except Exception as e:
        logger.error(f"Login failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate OAuth flow: {str(e)}"
        )


@router.get("/callback", name="callback")
async def callback(request: Request, code: str | None = None, state: str | None = None, error: str | None = None):
    """
    OAuth callback endpoint.
    
    Notion redirects here after user authorization.
    
    Steps:
    1. Validate state (CSRF check)
    2. Exchange code for tokens
    3. Save tokens to file
    4. Clear session
    5. Return success page
    """
    # Handle authorization error
    if error:
        logger.error(f"Authorization failed: {error}")
        return HTMLResponse(
            content=f"""
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1 style="color: red;">Authorization Failed</h1>
                    <p>Error: {error}</p>
                </body>
            </html>
            """,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    if not code or not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing code or state parameters"
        )
    
    try:
        # 1. Validate state (CSRF protection)
        saved_state = request.session.get('oauth_state')
        if not saved_state or saved_state != state:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="State mismatch! Possible CSRF attack."
            )
        
        # 2. Retrieve session data
        code_verifier = request.session.get('code_verifier')
        client_id = request.session.get('client_id')
        client_secret = request.session.get('client_secret')
        token_endpoint = request.session.get('token_endpoint')
        
        if not all([code_verifier, client_id, token_endpoint]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing session data. Please try logging in again."
            )
        
        # Reconstruct metadata for token exchange
        from .models import OAuthMetadata
        metadata = OAuthMetadata(
            issuer="",
            authorization_endpoint="",
            token_endpoint=token_endpoint
        )
        
        redirect_uri = str(request.url_for('callback'))
        
        # 3. Exchange code for tokens
        logger.info("Exchanging authorization code for tokens...")
        tokens = exchange_code_for_tokens(
            code=code,
            code_verifier=code_verifier,
            metadata=metadata,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri
        )
        
        # 4. Save tokens to file
        save_tokens(tokens, client_id=client_id, client_secret=client_secret)
        
        # 5. Clear session
        request.session.clear()
        
        logger.info("✅ Authentication successful! Tokens saved.")
        
        # Return success page
        return HTMLResponse(
            content="""
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1 style="color: green;">Authorization Successful! ✅</h1>
                    <p>You can close this window and return to your application.</p>
                    <p>Tokens have been saved to <code>.notion-tokens.json</code></p>
                    <script>
                        // Auto-close after 3 seconds
                        setTimeout(() => window.close(), 3000);
                    </script>
                </body>
            </html>
            """
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Callback failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token exchange failed: {str(e)}"
        )


@router.get("/status")
async def get_status():
    """
    Get current authentication status.
    
    Returns:
        JSON with authentication status and token info
    """
    tokens = load_tokens()
    
    if not tokens:
        return JSONResponse(
            content={
                "status": "not_authenticated",
                "message": "No tokens found. Please visit /auth/login to authenticate."
            }
        )
    
    # Calculate token age and expiry
    token_age_ms = int(time.time() * 1000) - tokens.updated_at
    expires_in_ms = (tokens.expires_in or 3600) * 1000
    remaining_ms = expires_in_ms - token_age_ms
    
    if remaining_ms <= 0:
        return JSONResponse(
            content={
                "status": "expired",
                "message": "Token has expired. Please re-authenticate.",
                "has_refresh_token": bool(tokens.refresh_token)
            }
        )
    
    if remaining_ms <= 300000:  # 5 minutes
        return JSONResponse(
            content={
                "status": "expiring_soon",
                "expires_in_seconds": remaining_ms // 1000,
                "message": "Token expiring soon. Consider refreshing."
            }
        )
    
    return JSONResponse(
        content={
            "status": "authenticated",
            "expires_in_seconds": remaining_ms // 1000,
            "token_type": tokens.token_type
        }
    )


@router.post("/logout")
async def logout():
    """
    Delete stored tokens.
    
    Returns:
        Success message
    """
    delete_tokens()
    
    return JSONResponse(
        content={
            "status": "success",
            "message": "Tokens deleted successfully"
        }
    )
