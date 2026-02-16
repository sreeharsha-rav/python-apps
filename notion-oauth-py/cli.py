#!/usr/bin/env python
"""
Notion OAuth CLI - Terminal interface for OAuth authentication.

Usage:
    python cli.py login    - Start OAuth flow
    python cli.py status   - Check authentication status
    python cli.py logout   - Delete stored tokens
    python cli.py refresh  - Refresh expired tokens
"""
import sys
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from threading import Thread

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from notion_oauth.service import (
    discover_oauth_metadata,
    register_client,
    create_authorization_url,
    exchange_code_for_tokens,
    refresh_access_token
)
from notion_oauth.storage import save_tokens, load_tokens, delete_tokens
from notion_oauth.models import OAuthMetadata

# Constants
NOTION_MCP_SERVER_URL = "https://mcp.notion.com"
CALLBACK_PORT = 3456
CALLBACK_URI = f"http://localhost:{CALLBACK_PORT}/callback"

console = Console()

# Global variable to store callback result
callback_result = {
    'code': None,
    'state': None,
    'error': None,
    'received': False
}


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""
    
    def do_GET(self):
        """Handle GET request to /callback."""
        global callback_result
        
        parsed_url = urlparse(self.path)
        
        if parsed_url.path != '/callback':
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
            return
        
        # Parse query parameters
        params = parse_qs(parsed_url.query)
        code = params.get('code', [None])[0]
        state = params.get('state', [None])[0]
        error = params.get('error', [None])[0]
        error_description = params.get('error_description', [None])[0]
        
        if error:
            callback_result['error'] = f"{error}: {error_description or 'Unknown error'}"
            callback_result['received'] = True
            
            self.send_response(400)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = f"""
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1 style="color: red;">❌ Authorization Failed</h1>
                    <p>Error: {error}</p>
                    <p>{error_description or ''}</p>
                    <p>You can close this window.</p>
                </body>
            </html>
            """
            self.wfile.write(html.encode())
            return
        
        if code and state:
            callback_result['code'] = code
            callback_result['state'] = state
            callback_result['received'] = True
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = """
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1 style="color: green;">✅ Authorization Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                    <script>
                        // Auto-close after 3 seconds
                        setTimeout(() => window.close(), 3000);
                    </script>
                </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing code or state parameters')
    
    def log_message(self, format, *args):
        """Suppress server logs."""
        pass


def start_callback_server():
    """Start temporary HTTP server for OAuth callback."""
    server = HTTPServer(('localhost', CALLBACK_PORT), CallbackHandler)
    console.print(f"[dim]Callback server listening on {CALLBACK_URI}[/dim]")
    
    # Run server in a thread
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    return server


def cmd_login():
    """Execute the OAuth login flow."""
    global callback_result
    
    console.print(Panel.fit(
        "[bold blue]🔐 Notion OAuth Authentication[/bold blue]\n"
        "Starting OAuth flow with dynamic client registration...",
        border_style="blue"
    ))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Step 1: Discovery
            task1 = progress.add_task("[cyan]1/7[/cyan] 🔍 Discovering OAuth metadata...", total=None)
            metadata = discover_oauth_metadata(NOTION_MCP_SERVER_URL)
            progress.update(task1, completed=True)
            console.print("✓ OAuth metadata discovered")
            
            # Step 2: Registration
            task2 = progress.add_task("[cyan]2/7[/cyan] 📝 Registering dynamic client...", total=None)
            credentials = register_client(metadata, CALLBACK_URI)
            progress.update(task2, completed=True)
            console.print(f"✓ Client registered (ID: {credentials.client_id[:20]}...)")
            
            # Step 3: PKCE
            task3 = progress.add_task("[cyan]3/7[/cyan] 🔐 Generating PKCE security values...", total=None)
            from authlib.common.security import generate_token
            oauth_state = generate_token(32)
            progress.update(task3, completed=True)
            console.print("✓ PKCE values generated")
            
            # Step 4: Start callback server
            task4 = progress.add_task("[cyan]4/7[/cyan] 🌐 Starting local callback server...", total=None)
            server = start_callback_server()
            progress.update(task4, completed=True)
            console.print(f"✓ Server listening on port {CALLBACK_PORT}")
            
            # Step 5: Create auth URL and open browser
            task5 = progress.add_task("[cyan]5/7[/cyan] 🚀 Opening browser for authorization...", total=None)
            auth_url, code_verifier = create_authorization_url(
                metadata=metadata,
                client_id=credentials.client_id,
                redirect_uri=CALLBACK_URI,
                state=oauth_state,
                scopes=[]
            )
            progress.update(task5, completed=True)
            
            console.print("\n[yellow]Opening browser... Please authorize the application.[/yellow]")
            webbrowser.open(auth_url)
            
            # Step 6: Wait for callback
            task6 = progress.add_task("[cyan]6/7[/cyan] ⏳ Waiting for callback...", total=None)
            
            # Wait for callback with timeout
            timeout = 300  # 5 minutes
            start_time = time.time()
            while not callback_result['received']:
                if time.time() - start_time > timeout:
                    raise TimeoutError("Authorization timeout after 5 minutes")
                time.sleep(0.5)
            
            progress.update(task6, completed=True)
            
            # Shutdown server
            server.shutdown()
            
            # Check for errors
            if callback_result['error']:
                raise Exception(callback_result['error'])
            
            # Validate state
            if callback_result['state'] != oauth_state:
                raise Exception("State mismatch! Possible CSRF attack.")
            
            console.print("✓ Authorization code received")
            
            # Step 7: Exchange code for tokens
            task7 = progress.add_task("[cyan]7/7[/cyan] 🔄 Exchanging code for tokens...", total=None)
            tokens = exchange_code_for_tokens(
                code=callback_result['code'],
                code_verifier=code_verifier,
                metadata=metadata,
                client_id=credentials.client_id,
                client_secret=credentials.client_secret,
                redirect_uri=CALLBACK_URI
            )
            progress.update(task7, completed=True)
            
            # Save tokens
            save_tokens(
                tokens,
                client_id=credentials.client_id,
                client_secret=credentials.client_secret
            )
            console.print("✓ Tokens saved to .notion-tokens.json")
        
        console.print("\n[bold green]✅ Authentication successful![/bold green]")
        console.print("[dim]You can now use the Notion API with your access token.[/dim]")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Authentication failed:[/bold red] {e}")
        sys.exit(1)


def cmd_status():
    """Check authentication status."""
    tokens = load_tokens()
    
    if not tokens:
        console.print(Panel.fit(
            "[yellow]⚠ Not authenticated[/yellow]\n"
            "Run [bold]python cli.py login[/bold] to authenticate.",
            border_style="yellow"
        ))
        return
    
    # Calculate token age and expiry
    token_age_ms = int(time.time() * 1000) - tokens.updated_at
    expires_in_ms = (tokens.expires_in or 3600) * 1000
    remaining_ms = expires_in_ms - token_age_ms
    remaining_seconds = remaining_ms // 1000
    
    # Create status table
    table = Table(title="🔐 Authentication Status", show_header=True, header_style="bold cyan")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    if remaining_seconds <= 0:
        status = "[red]Expired[/red]"
        table.add_row("Status", status)
        table.add_row("Has Refresh Token", "✓" if tokens.refresh_token else "✗")
        console.print(table)
        console.print("\n[yellow]Token expired. Run [bold]python cli.py refresh[/bold] to refresh.[/yellow]")
    elif remaining_seconds <= 300:  # 5 minutes
        status = "[yellow]Expiring Soon[/yellow]"
        table.add_row("Status", status)
        table.add_row("Expires In", f"{remaining_seconds // 60} minutes {remaining_seconds % 60} seconds")
        table.add_row("Token Type", tokens.token_type)
        console.print(table)
        console.print("\n[yellow]Token expiring soon. Consider running [bold]python cli.py refresh[/bold][/yellow]")
    else:
        status = "[green]✓ Authenticated[/green]"
        table.add_row("Status", status)
        table.add_row("Expires In", f"{remaining_seconds // 60} minutes {remaining_seconds % 60} seconds")
        table.add_row("Token Type", tokens.token_type)
        table.add_row("Client ID", f"{tokens.client_id[:20]}..." if tokens.client_id else "N/A")
        console.print(table)


def cmd_logout():
    """Delete stored tokens."""
    tokens = load_tokens()
    
    if not tokens:
        console.print("[yellow]No tokens found. Already logged out.[/yellow]")
        return
    
    delete_tokens()
    console.print("[green]✓ Tokens deleted successfully.[/green]")
    console.print("[dim]You have been logged out.[/dim]")


def cmd_refresh():
    """Refresh expired tokens."""
    tokens = load_tokens()
    
    if not tokens:
        console.print("[red]❌ No tokens found. Please login first.[/red]")
        sys.exit(1)
    
    if not tokens.refresh_token:
        console.print("[red]❌ No refresh token available. Please re-authenticate.[/red]")
        sys.exit(1)
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            task1 = progress.add_task("[cyan]Discovering OAuth metadata...", total=None)
            metadata = discover_oauth_metadata(NOTION_MCP_SERVER_URL)
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("[cyan]Refreshing access token...", total=None)
            new_tokens = refresh_access_token(
                refresh_token=tokens.refresh_token,
                metadata=metadata,
                client_id=tokens.client_id,
                client_secret=tokens.client_secret
            )
            progress.update(task2, completed=True)
            
            # Save new tokens
            save_tokens(
                new_tokens,
                client_id=tokens.client_id,
                client_secret=tokens.client_secret
            )
        
        console.print("[green]✓ Token refreshed successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Token refresh failed:[/red] {e}")
        console.print("[yellow]You may need to re-authenticate with [bold]python cli.py login[/bold][/yellow]")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        console.print(Panel.fit(
            "[bold cyan]Notion OAuth CLI[/bold cyan]\n\n"
            "Available commands:\n"
            "  [green]login[/green]   - Start OAuth authentication flow\n"
            "  [green]status[/green]  - Check authentication status\n"
            "  [green]logout[/green]  - Delete stored tokens\n"
            "  [green]refresh[/green] - Refresh expired tokens\n\n"
            "Usage: [bold]python cli.py [command][/bold]",
            border_style="cyan"
        ))
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == 'login':
        cmd_login()
    elif command == 'status':
        cmd_status()
    elif command == 'logout':
        cmd_logout()
    elif command == 'refresh':
        cmd_refresh()
    else:
        console.print(f"[red]Unknown command: {command}[/red]")
        console.print("Available commands: login, status, logout, refresh")
        sys.exit(1)


if __name__ == '__main__':
    main()
