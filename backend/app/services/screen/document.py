class DocumentUnderstanding:
    def __init__(self):
        pass

    def extract_document_structure(self, ui_tree):
        """
        Attempts to find large text/document panes within the UI tree 
        and extracts readable content logically.
        """
        content = []
        if ui_tree:
            def _find_documents(node):
                if node.get("type") in ["Document", "Edit"]:
                    content.append(node.get("name", ""))
                for child in node.get("children", []):
                    _find_documents(child)
            _find_documents(ui_tree)
            
        return "\n".join([c for c in content if c])

document_understanding = DocumentUnderstanding()
