"""
AGNIV Extension SDK CLI
=======================
Usage:
    python -m agniv_sdk.cli create <name> <type>
    python -m agniv_sdk.cli validate <path>
    python -m agniv_sdk.cli package <path>
    python -m agniv_sdk.cli install <path>
"""
import argparse
import json
import os
import shutil
import zipfile
import sys
import re


EXTENSION_TYPES = [
    "capability",
    "skill",
    "workflow_pack",
    "integration",
    "ui_panel",
    "accessibility_pack",
]

MANIFEST_TEMPLATE = {
    "id": "{id}",
    "name": "{name}",
    "version": "1.0.0",
    "type": "{type}",
    "description": "Describe your extension here.",
    "author": {
        "name": "Your Name",
        "email": "you@example.com"
    },
    "agniv_version": ">=1.0.0",
    "entry_point": "main.py",
    "permissions": [],
    "tags": [],
    "license": "MIT"
}

MAIN_TEMPLATE = '''"""
{name}
{underline}
Extension type: {type}
"""


class Extension:
    def __init__(self, sdk):
        self.sdk = sdk

    def on_enable(self):
        self.sdk.log("{name} extension enabled.")

    def on_disable(self):
        self.sdk.log("{name} extension disabled.")

    def metadata(self) -> dict:
        return {{
            "name": "{name}",
            "type": "{type}",
        }}
'''


def cmd_create(args):
    name = args.name
    ext_type = args.type
    ext_id = re.sub(r"[^a-z0-9]", "-", name.lower()).strip("-")
    dir_name = ext_id
    output = args.output or "."
    target = os.path.join(output, dir_name)

    if os.path.exists(target):
        print(f"Error: Directory '{target}' already exists.")
        sys.exit(1)

    os.makedirs(target)

    manifest = dict(MANIFEST_TEMPLATE)
    manifest["id"] = ext_id
    manifest["name"] = name
    manifest["type"] = ext_type

    with open(os.path.join(target, "agniv-extension.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    underline = "=" * len(name)
    main_code = MAIN_TEMPLATE.format(name=name, type=ext_type, underline=underline)
    with open(os.path.join(target, "main.py"), "w") as f:
        f.write(main_code)

    with open(os.path.join(target, "README.md"), "w") as f:
        f.write(f"# {name}\n\nType: `{ext_type}`\n\nAGNIV Extension SDK v1.0\n")

    print(f"✅ Created extension scaffold at: {target}")
    print(f"   ID: {ext_id}")
    print(f"   Type: {ext_type}")
    print(f"   Edit 'agniv-extension.json' and 'main.py' to implement your extension.")


def cmd_validate(args):
    path = args.path
    manifest_path = os.path.join(path, "agniv-extension.json")
    if not os.path.exists(manifest_path):
        print(f"Error: No 'agniv-extension.json' found in '{path}'")
        sys.exit(1)

    with open(manifest_path, "r") as f:
        raw = json.load(f)

    # Basic validations
    errors = []
    required = ["id", "name", "version", "type", "description", "author"]
    for field in required:
        if field not in raw:
            errors.append(f"Missing required field: '{field}'")

    if raw.get("type") not in EXTENSION_TYPES:
        errors.append(f"Invalid type '{raw.get('type')}'. Must be one of: {EXTENSION_TYPES}")

    if not re.match(r"^\d+\.\d+\.\d+$", raw.get("version", "")):
        errors.append(f"Version must be semver (x.y.z), got: '{raw.get('version', '')}'")

    entry = os.path.join(path, raw.get("entry_point", "main.py"))
    if not os.path.exists(entry):
        errors.append(f"Entry point '{raw.get('entry_point')}' not found.")

    if errors:
        print(f"❌ Validation failed with {len(errors)} error(s):")
        for e in errors:
            print(f"   • {e}")
        sys.exit(1)
    else:
        print(f"✅ Extension manifest is valid.")
        print(f"   ID: {raw.get('id')}")
        print(f"   Name: {raw.get('name')}")
        print(f"   Version: {raw.get('version')}")
        print(f"   Type: {raw.get('type')}")


def cmd_package(args):
    path = args.path
    manifest_path = os.path.join(path, "agniv-extension.json")
    if not os.path.exists(manifest_path):
        print(f"Error: No 'agniv-extension.json' found in '{path}'")
        sys.exit(1)

    with open(manifest_path, "r") as f:
        raw = json.load(f)

    ext_id = raw.get("id", "extension")
    version = raw.get("version", "1.0.0")
    package_name = f"{ext_id}-{version}.agniv"
    output = args.output or "."
    output_path = os.path.join(output, package_name)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(path))
                zf.write(file_path, arcname)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ Packaged extension to: {output_path}")
    print(f"   Package size: {size_kb:.1f} KB")


def cmd_install(args):
    pkg_path = args.path
    extensions_dir = args.target or "extensions"

    if not os.path.exists(extensions_dir):
        os.makedirs(extensions_dir)

    if pkg_path.endswith(".agniv"):
        # Unzip package
        pkg_name = os.path.basename(pkg_path).replace(".agniv", "")
        target_dir = os.path.join(extensions_dir, pkg_name.rsplit("-", 1)[0])
        with zipfile.ZipFile(pkg_path, "r") as zf:
            zf.extractall(extensions_dir)
        print(f"✅ Installed extension from package: {pkg_path}")
        print(f"   Extracted to: {extensions_dir}")
    else:
        # Directory copy
        dir_name = os.path.basename(pkg_path.rstrip("/\\"))
        target_dir = os.path.join(extensions_dir, dir_name)
        if os.path.exists(target_dir):
            print(f"Extension directory '{dir_name}' already exists. Overwriting...")
            shutil.rmtree(target_dir)
        shutil.copytree(pkg_path, target_dir)
        print(f"✅ Installed extension to: {target_dir}")
    print("   Restart AGNIV or call POST /extensions/scan to activate.")


def main():
    parser = argparse.ArgumentParser(
        prog="agniv-sdk",
        description="AGNIV Extension SDK CLI"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Create
    p_create = sub.add_parser("create", help="Scaffold a new extension")
    p_create.add_argument("name", help="Extension display name")
    p_create.add_argument("type", choices=EXTENSION_TYPES, help="Extension type")
    p_create.add_argument("--output", "-o", help="Output directory (default: .)")
    p_create.set_defaults(func=cmd_create)

    # Validate
    p_validate = sub.add_parser("validate", help="Validate an extension directory")
    p_validate.add_argument("path", help="Path to extension directory")
    p_validate.set_defaults(func=cmd_validate)

    # Package
    p_package = sub.add_parser("package", help="Package extension into a .agniv file")
    p_package.add_argument("path", help="Path to extension directory")
    p_package.add_argument("--output", "-o", help="Output directory (default: .)")
    p_package.set_defaults(func=cmd_package)

    # Install
    p_install = sub.add_parser("install", help="Install an extension directory or .agniv package")
    p_install.add_argument("path", help="Path to extension directory or .agniv file")
    p_install.add_argument("--target", "-t", help="Extensions directory (default: extensions/)")
    p_install.set_defaults(func=cmd_install)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
