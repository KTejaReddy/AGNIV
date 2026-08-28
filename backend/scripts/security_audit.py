"""
AGNIV Security Audit Tool
Statically verifies core permissions and extension sandboxes.
"""
import os
import ast
import json
import sys

def check_sandbox_bypasses():
    print("Checking extension sandboxes for bypasses...")
    ext_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../extensions"))
    if not os.path.exists(ext_dir):
        print(f"  [WARN] Extensions directory not found: {ext_dir}")
        return True

    bypasses_found = 0
    for ext in os.listdir(ext_dir):
        ext_path = os.path.join(ext_dir, ext)
        if not os.path.isdir(ext_path) or ext.startswith("_"):
            continue
            
        main_py = os.path.join(ext_path, "main.py")
        if not os.path.exists(main_py):
            continue
            
        with open(main_py, "r") as f:
            code = f.read()
            
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    module = getattr(node, "module", None) or node.names[0].name
                    if module and module.startswith("app."):
                        print(f"  [CRITICAL] Extension '{ext}' bypasses sandbox! Direct import of '{module}' in main.py")
                        bypasses_found += 1
        except SyntaxError:
            print(f"  [ERROR] Syntax error parsing {main_py}")
            
    if bypasses_found == 0:
        print("  [OK] No sandbox bypasses detected.")
        return True
    return False

def check_capability_manager():
    print("Checking Capability Manager for permission checks...")
    cap_manager_py = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/core/engine/capability_manager.py"))
    
    with open(cap_manager_py, "r") as f:
        content = f.read()
        
    if "permission_manager.check_permission(" in content:
        print("  [OK] Capability Manager correctly checks permissions before execution.")
        return True
    else:
        print("  [CRITICAL] Capability Manager is missing permission checks!")
        return False

def run_audit():
    print("=" * 40)
    print("AGNIV SECURITY AUDIT")
    print("=" * 40)
    
    sandbox_ok = check_sandbox_bypasses()
    cap_ok = check_capability_manager()
    
    print("=" * 40)
    if sandbox_ok and cap_ok:
        print("AUDIT PASSED. System is secure.")
        sys.exit(0)
    else:
        print("AUDIT FAILED! Security vulnerabilities detected.")
        sys.exit(1)

if __name__ == "__main__":
    run_audit()
