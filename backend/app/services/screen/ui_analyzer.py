import pywinauto
from app.core.logging import logger

class UIAnalyzer:
    def __init__(self):
        pass

    def extract_ui_tree(self):
        """
        Extracts a structural representation of the currently active window
        using Windows UIAutomation (UIA).
        """
        try:
            # We connect to the desktop and get the active window
            app = pywinauto.Desktop(backend="uia")
            active_window = app.active()
            
            if not active_window:
                return {"error": "No active window found"}

            def _parse_element(element, depth=0, max_depth=3):
                if depth > max_depth:
                    return None
                
                # Element wrapping can fail for weird windows, catching it
                try:
                    name = element.window_text()
                    control_type = element.element_info.control_type
                    rect = element.rectangle()
                    
                    # Filtering out empty and tiny elements to reduce noise
                    if not name and control_type not in ['Button', 'Document', 'Edit', 'List', 'Tree']:
                        return None
                        
                    node = {
                        "name": name,
                        "type": control_type,
                        "rect": {
                            "left": rect.left,
                            "top": rect.top,
                            "right": rect.right,
                            "bottom": rect.bottom
                        },
                        "children": []
                    }
                    
                    for child in element.children():
                        child_node = _parse_element(child, depth + 1, max_depth)
                        if child_node:
                            node["children"].append(child_node)
                            
                    return node
                except Exception:
                    return None
                    
            tree = _parse_element(active_window)
            return tree
            
        except Exception as e:
            logger.error(f"UIAnalyzer failed: {e}")
            return {"error": str(e)}

ui_analyzer = UIAnalyzer()
