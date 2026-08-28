import pyperclip
from app.core.engine.capability_manager import capability_manager

async def read_clipboard(params):
    text = pyperclip.paste()
    return {"status": "success", "text": text}

async def copy_text(params):
    text = params.get("text", "")
    pyperclip.copy(text)
    return {"status": "success"}

async def clear_clipboard(params):
    pyperclip.copy("")
    return {"status": "success"}

def register():
    capability_manager.register_capability("READ_CLIPBOARD", "1.0", "Reads text from clipboard", read_clipboard)
    capability_manager.register_capability("COPY_TEXT", "1.0", "Copies text to clipboard", copy_text)
    capability_manager.register_capability("CLEAR_CLIPBOARD", "1.0", "Clears the clipboard", clear_clipboard)
