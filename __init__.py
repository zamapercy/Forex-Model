from __future__ import annotations

from pathlib import Path
import pkgutil

# Compatibility shim for environments (e.g. Streamlit Cloud) that don't add src/ to sys.path.
__path__ = pkgutil.extend_path(__path__, __name__)  # type: ignore[name-defined]
_src_pkg = Path(__file__).resolve().parent.parent / "src" / "forex_model"
if _src_pkg.exists():
    __path__.append(str(_src_pkg))
