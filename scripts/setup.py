"""
Template setup script.
Run this after cloning the template to customize your project.

Usage:
    uv run python scripts/setup.py \\
        --project-name "my-awesome-api" \\
        --author "Your Name" \\
        --company "Your Company" \\
        --python-version "3.12"
"""

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import subprocess
import sys


class TemplateSetup:
    """Setup and customize FastAPI template."""

    def __init__(
        self,
        project_name: str,
        author: str,
        company: str,
        python_version: str = "3.14",
        description: str | None = None,
    ):
        """
        Initialize template setup.

        Args:
            project_name: Project name (e.g., 'my-awesome-api').
            author: Author name.
            company: Company name.
            python_version: Python version (e.g., '3.12', '3.13').
            description: Project description (optional).
        """
        self.project_name = project_name
        self.author = author
        self.company = company
        self.python_version = python_version
        default_desc = f"{project_name} - FastAPI application"
        self.description = description or default_desc
        self.root = Path(__file__).parent.parent

    def run(self):
        """Execute all setup steps."""
        print(f"🚀 Setting up {self.project_name}...\n")

        self.update_pyproject()
        self.update_ide_config()
        self.update_docstrings()
        self.create_env_file()
        self.sync_dependencies()

        print("\n✅ Setup complete!")
        print("\n📝 Next steps:")
        print("  1. Review and edit .env file")
        print("  2. Start development: uv run python main.py")
        print("  3. Run tests: uv run pytest")
        print("  4. Happy coding! 🎉\n")

    def update_pyproject(self):
        """Update pyproject.toml with project info."""
        print("📦 Updating pyproject.toml...")

        pyproject_path = self.root / "pyproject.toml"
        content = pyproject_path.read_text()

        # Update project name
        content = re.sub(
            r'name = "fast-api-template".*',
            f'name = "{self.project_name}"',
            content,
        )

        # Update description
        content = re.sub(
            r'description = ".*?".*',
            f'description = "{self.description}"',
            content,
        )

        # Update Python version
        content = re.sub(
            r'requires-python = ">=[\d.]+"',
            f'requires-python = ">={self.python_version}"',
            content,
        )

        # Update target version for ruff
        py_version_short = self.python_version.replace(".", "")
        content = re.sub(
            r'target-version = "py\d+"',
            f'target-version = "py{py_version_short}"',
            content,
        )

        # Update known-first-party for isort
        package_name = self.project_name.replace("-", "_")
        content = re.sub(
            r'known-first-party = \[".*?"\]',
            f'known-first-party = ["{package_name}"]',
            content,
        )

        # Update mypy python_version
        content = re.sub(
            r'python_version = "[\d.]+"',
            f'python_version = "{self.python_version}"',
            content,
        )

        pyproject_path.write_text(content)
        print(f"   ✓ Updated project name: {self.project_name}")
        print(f"   ✓ Updated Python version: {self.python_version}")

    def update_ide_config(self):
        """Update .ideconfig/settings.json."""
        print("\n🔧 Updating IDE config...")

        config_path = self.root / ".ideconfig" / "settings.json"
        if not config_path.exists():
            print("   ⚠️  .ideconfig/settings.json not found, skipping")
            return

        with open(config_path) as f:
            config = json.load(f)

        # Update psi-header variables
        if "psi-header.variables" in config:
            for i, var in enumerate(config["psi-header.variables"]):
                if var[0] == "author":
                    config["psi-header.variables"][i][1] = self.author
                elif var[0] == "company":
                    config["psi-header.variables"][i][1] = self.company
                elif var[0] == "projectname":
                    config["psi-header.variables"][i][1] = self.project_name

        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        print(f"   ✓ Updated author: {self.author}")
        print(f"   ✓ Updated company: {self.company}")

    def update_docstrings(self):
        """Update all docstrings in Python files."""
        print("\n📝 Updating docstrings...")

        current_date = datetime.now().strftime("%A, %dth %B %Y")

        # Pattern to match dates like "Wednesday, 29th October 2025"
        date_pattern = re.compile(
            r"\w+day,\s+\d+(?:st|nd|rd|th)\s+\w+\s+\d{4}(?:\s+\d{1,2}:\d{2}:\d{2}\s+(?:am|pm))?"
        )

        python_files = []
        for pattern in ["app/**/*.py", "tests/**/*.py", "scripts/**/*.py"]:
            python_files.extend(self.root.glob(pattern))

        # Add root files
        python_files.extend(self.root.glob("*.py"))

        count = 0
        for file_path in python_files:
            # Skip virtual environments
            if any(
                skip in file_path.parts
                for skip in [".venv", "venv", "__pycache__"]
            ):
                continue

            # Skip this setup script itself
            if file_path.name == "setup.py" and "scripts" in file_path.parts:
                continue

            try:
                content = file_path.read_text()
                original = content

                # Update placeholders
                content = content.replace(
                    "replace with your project name", self.project_name
                )
                content = content.replace("replace with your name", self.author)
                content = content.replace(
                    "replace with your company", self.company
                )

                # Update creation date (smart pattern matching)
                content = date_pattern.sub(current_date, content)

                if content != original:
                    file_path.write_text(content)
                    count += 1

            except Exception as e:
                print(f"   ⚠️  Failed to update {file_path}: {e}")

        print(f"   ✓ Updated {count} files")

    def create_env_file(self):
        """Create .env from template if it doesn't exist."""
        print("\n🔧 Setting up environment file...")

        env_path = self.root / ".env"
        template_path = self.root / ".env.template"

        if env_path.exists():
            print("   [i] .env already exists, skipping")
            return

        if not template_path.exists():
            print("   [!] .env.template not found, skipping")
            return

        content = template_path.read_text()

        # Update APP_NAME
        content = re.sub(
            r"APP_NAME=.*", f"APP_NAME={self.project_name}", content
        )

        env_path.write_text(content)
        print(f"   ✓ Created .env with project name: {self.project_name}")
        print("   [i] Don't forget to update SECRET_KEY and other values!")

    def sync_dependencies(self):
        """Sync dependencies with uv."""
        print("\n📦 Setting up Python environment...")

        try:
            # Check if uv is available
            subprocess.run(
                ["uv", "--version"],
                capture_output=True,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ⚠️  uv not found. Please install uv and run:")
            print("      uv sync")
            return

        try:
            # Pin Python version
            print(f"   • Pinning Python {self.python_version}...")
            subprocess.run(
                ["uv", "python", "pin", self.python_version],
                cwd=self.root,
                check=True,
                capture_output=True,
            )

            # Regenerate lockfile for the new Python version
            print("   • Regenerating lockfile...")
            subprocess.run(
                ["uv", "lock"], cwd=self.root, check=True, capture_output=True
            )

            # Sync dependencies
            print("   • Installing dependencies...")
            subprocess.run(
                ["uv", "sync"], cwd=self.root, check=True, capture_output=True
            )

            print("   ✓ Dependencies synced successfully")

        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Failed to sync dependencies: {e}")
            print("   Please run manually:")
            print(f"      uv python pin {self.python_version}")
            print("      uv lock")
            print("      uv sync")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Setup FastAPI template with your project details",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python scripts/setup.py \\
    --project-name "my-awesome-api" \\
    --author "John Doe" \\
    --company "Acme Corp"

  uv run python scripts/setup.py \\
    --project-name "users-service" \\
    --author "Jane Smith" \\
    --python-version "3.12" \\
    --description "User management microservice"
        """,
    )

    parser.add_argument(
        "--project-name",
        required=True,
        help="Project name (e.g., 'my-awesome-api')",
    )
    parser.add_argument(
        "--author", required=True, help="Author name (e.g., 'John Doe')"
    )
    parser.add_argument(
        "--company", default="Your Company", help="Company name"
    )
    parser.add_argument(
        "--python-version",
        default="3.14",
        help="Python version (e.g., '3.12', '3.13', '3.14')",
    )
    parser.add_argument(
        "--description",
        help="Project description (optional)",
    )

    args = parser.parse_args()

    # Validate Python version format
    if not re.match(r"^\d+\.\d+$", args.python_version):
        print(f"❌ Invalid Python version: {args.python_version}")
        print("   Use format: '3.12' or '3.13'")
        sys.exit(1)

    setup = TemplateSetup(
        project_name=args.project_name,
        author=args.author,
        company=args.company,
        python_version=args.python_version,
        description=args.description,
    )

    try:
        setup.run()
    except KeyboardInterrupt:
        print("\n\n[!] Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
