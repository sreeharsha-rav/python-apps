# Notion OAuth Flow - Python FastAPI Implementation

A Python FastAPI application implementing the Notion MCP OAuth flow with dynamic client registration, PKCE security, and Authlib integration.

## Features

- ✅ **OAuth 2.0 with PKCE** - Secure authorization code flow with Proof Key for Code Exchange
- ✅ **Dynamic Client Registration (RFC 7591)** - No hardcoded client credentials
- ✅ **OAuth Discovery (RFC 8414/9470)** - Auto-discover endpoints from Notion MCP
- ✅ **Session Management** - Secure state management via encrypted cookies
- ✅ **Token Storage** - File-based token persistence with refresh support
- ✅ **Authlib Integration** - Uses industry-standard OAuth library
- ✅ **CLI Tool** - Interactive command-line interface for authentication

## Architecture

The implementation uses a unified service layer for OAuth logic:

```
notion_oauth/
├── __init__.py         # Package init
├── models.py           # Pydantic models for OAuth types
├── service.py          # Unified OAuth service (Discovery, Registration, Auth)
├── storage.py          # JSON file-based token persistence
└── router.py           # FastAPI routes (/login, /callback, /status, /logout)
```

## Installation

```powershell
# Install dependencies
uv sync

# Run the server
uv run uvicorn main:app --reload --port 8000
```

## CLI Usage

The project includes a command-line interface for managing authentication:

```powershell
# Start the OAuth login flow
uv run python cli.py login

# Check authentication status
uv run python cli.py status

# Refresh usage tokens
uv run python cli.py refresh

# Logout (delete tokens)
uv run python cli.py logout
```

## API Usage

### 1. Start Authorization Flow

Open your browser to:
```
http://localhost:8000/auth/login
```

This will:
1. Discover OAuth metadata from `https://mcp.notion.com`
2. Register a dynamic client with Notion
3. Generate PKCE values (code_verifier, code_challenge)
4. Redirect you to Notion's authorization page

### 2. Check Status

```bash
curl http://localhost:8000/auth/status
```

Returns:
```json
{
  "status": "authenticated",
  "expires_in_seconds": 3234,
  "token_type": "Bearer"
}
```

## Key Differences from TypeScript Implementation

| TypeScript (CLI) | Python (FastAPI) |
|------------------|------------------|
| Temporary callback HTTP server | FastAPI routes handle callbacks |
| In-memory state during `await` | Session middleware stores state |
| `open` package opens browser | User manually opens browser (API) / Auto (CLI) |
| Node.js `crypto` module | Authlib's PKCE implementation |
| TypeScript types | Pydantic models |

## Security Notes

⚠️ **For Production:**
1. Move `SessionMiddleware` secret_key to environment variable
2. Use HTTPS for all endpoints
3. Encrypt token storage or use OS keychain
4. Implement proper error handling and logging
5. Add rate limiting on OAuth endpoints

## Token Storage

Tokens are stored in `.notion-tokens.json`:

```json
{
  "access_token": "secret_xyz...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_abc...",
  "client_id": "dynamic_id_123...",
  "client_secret": null,
  "updated_at": 1707734160000
}
```

This file is gitignored to prevent committing credentials.

## License

MIT
