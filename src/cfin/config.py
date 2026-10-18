"""Application paths and runtime settings."""

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent

STATIC_DIR = PACKAGE_DIR / "static"
RESOURCES_DIR = PACKAGE_DIR / "resources"
MARKDOWN_DIR = RESOURCES_DIR / "markdown"
CSS_DIR = RESOURCES_DIR / "css"
TEMPLATES_DIR = RESOURCES_DIR / "templates"

HOST = os.getenv("CFIN_HOST", "0.0.0.0")
PORT = int(os.getenv("CFIN_PORT", os.getenv("PORT", "8000")))
RELOAD = os.getenv("CFIN_RELOAD", "").lower() in {"1", "true", "yes", "on"}
DEBUG = os.getenv("CFIN_DEBUG", "").lower() in {"1", "true", "yes", "on"}
