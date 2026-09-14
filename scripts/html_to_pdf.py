"""
Render an HTML report to PDF.

Tries weasyprint first (pure-Python, fast, no subprocess) since it's the
cleanest path when installed. Falls back to headless Microsoft Edge's
--print-to-pdf, which ships on every Windows 11 install and needs no extra
dependency -- this is the reliable default path for this skill.

Usage:
    python html_to_pdf.py <input.html> <output.pdf>
"""
import sys
import subprocess
import shutil
from pathlib import Path

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def try_weasyprint(html_path: Path, pdf_path: Path) -> bool:
    try:
        from weasyprint import HTML
    except ImportError:
        return False
    HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    return True


def find_browser() -> str | None:
    for candidate in EDGE_CANDIDATES + CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    # Fall back to whatever's on PATH
    for name in ("msedge", "msedge.exe", "chrome", "chrome.exe", "google-chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def try_headless_browser(html_path: Path, pdf_path: Path) -> bool:
    browser = find_browser()
    if not browser:
        return False
    # Edge/Chrome headless requires an ABSOLUTE output path -- a relative
    # one fails silently with "Access is denied" regardless of cwd.
    abs_pdf_path = pdf_path.resolve()
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf_path}",
        str(html_path.resolve().as_uri()),
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    return result.returncode == 0 and abs_pdf_path.exists()


def main():
    if len(sys.argv) != 3:
        print("Usage: python html_to_pdf.py <input.html> <output.pdf>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2])

    if not html_path.exists():
        print(f"Input HTML not found: {html_path}")
        sys.exit(1)

    if try_weasyprint(html_path, pdf_path):
        print(f"PDF written via weasyprint: {pdf_path}")
        return

    if try_headless_browser(html_path, pdf_path):
        print(f"PDF written via headless browser: {pdf_path}")
        return

    print("FAILED: no PDF renderer available. Install weasyprint "
          "(`pip install weasyprint`) or ensure Edge/Chrome is installed.")
    sys.exit(2)


if __name__ == "__main__":
    main()
