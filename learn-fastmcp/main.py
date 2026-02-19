from fastmcp import FastMCP
from starlette.responses import JSONResponse
from middleware import configure_logging, LoggingMiddleware


configure_logging()

mcp = FastMCP(
    name="todos-mcp",
    instructions="This server provides tools, resources, and prompts for managing todo items. Call add, list, modify and remove todo items.",
)

mcp.add_middleware(LoggingMiddleware())

@mcp.tool("add_todo", description="Add a new todo item", parameters={"item": "The todo item to add"})
def add_todo(item: str):    # Code to add the todo item to a database or list
    return f"Todo item '{item}' added successfully."

@mcp.tool("remove_todo", description="Remove a todo item", parameters={"item": "The todo item to remove"})
def remove_todo(item: str):    # Code to remove the todo item from a database or list
    return f"Todo item '{item}' removed successfully."

@mcp.tool("list_todos", description="List all todo items")
def list_todos():    # Code to retrieve and return all todo items from a database or list
    return "Here are your current todo items: ..."

@mcp.tool("set_reminder", description="Set a reminder for a todo item", parameters={"item": "The todo item to set a reminder for", "time": "The time to set the reminder for"})
def set_reminder(item: str, time: str):    # Code to set a reminder for the specified todo item at the given time
    return f"Reminder set for todo item '{item}' at {time}."

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "todos-mcp"})
