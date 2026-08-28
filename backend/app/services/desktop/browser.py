import webbrowser
from app.core.engine.capability_manager import capability_manager

async def open_url(params):
    url = params.get("url")
    webbrowser.open(url)
    return {"status": "success", "url": url}

async def open_google_search(params):
    query = params.get("query")
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return {"status": "success", "query": query}

async def open_html(params):
    path = params.get("path")
    webbrowser.open(f"file://{path}")
    return {"status": "success", "path": path}

def register():
    capability_manager.register_capability("OPEN_URL", "1.0", "Opens a URL in default browser", open_url)
    capability_manager.register_capability("OPEN_GOOGLE_SEARCH", "1.0", "Searches Google", open_google_search)
    capability_manager.register_capability("OPEN_HTML", "1.0", "Opens a local HTML file", open_html)
