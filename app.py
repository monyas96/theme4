# Run prototype switcher directly (no navigation sidebar)
# The switcher will handle set_page_config as the first command
import sys
from pathlib import Path

# Add pages directory to path
pages_dir = str(Path(__file__).resolve().parent / "pages")
if pages_dir not in sys.path:
    sys.path.insert(0, pages_dir)

# Add parent directory to path for imports
parent_dir = str(Path(__file__).resolve().parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Run the prototype switcher - it will call set_page_config first
exec(open("pages/00_prototype_switcher.py").read())
