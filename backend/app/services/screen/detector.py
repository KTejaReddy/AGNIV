class ScreenElementDetector:
    def __init__(self):
        pass

    def detect_elements(self, ocr_results, ui_tree):
        """
        Takes OCR results and UI tree to find logical elements on the screen.
        (e.g., Notifications, Dialogs, Loading states).
        """
        elements = []
        
        # Simple heuristic based detection
        if ui_tree:
            def _find_dialogs(node):
                if node.get("type") == "Window" and "Dialog" in node.get("name", ""):
                    elements.append({"type": "DIALOG", "name": node.get("name"), "rect": node.get("rect")})
                if node.get("type") == "Pane" and "Notification" in node.get("name", ""):
                    elements.append({"type": "NOTIFICATION", "name": node.get("name"), "rect": node.get("rect")})
                    
                for child in node.get("children", []):
                    _find_dialogs(child)
                    
            _find_dialogs(ui_tree)
            
        return elements

element_detector = ScreenElementDetector()
