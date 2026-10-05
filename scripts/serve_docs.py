"""Build fresh Sphinx HTML and serve it on localhost."""

import argparse
import errno
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit


class DocsHandler(SimpleHTTPRequestHandler):
    """Serve static docs and redirect bookmarks for intentionally removed pages."""

    def do_GET(self):
        if self.redirect_removed_page():
            return
        super().do_GET()

    def do_HEAD(self):
        if self.redirect_removed_page():
            return
        super().do_HEAD()

    def redirect_removed_page(self):
        if urlsplit(self.path).path not in {"/examples.html", "/architecture.html"}:
            return False
        self.send_response(302)
        self.send_header("Location", "/index.html")
        self.send_header("Content-Length", "0")
        self.end_headers()
        return True


def build_html(docs, output):
    result = subprocess.run([
        sys.executable, "-m", "sphinx", "-E", "-a", "-W", "--keep-going",
        "-b", "html", str(docs), str(output),
    ])
    if result.returncode:
        return result.returncode
    if not (output / "index.html").is_file():
        print("Sphinx produced no index.html; server was not started.", file=sys.stderr)
        return 1
    return 0


def publish_html(snapshot, html):
    """Replace exported HTML only after successful build, restoring on failure."""
    with tempfile.TemporaryDirectory(prefix="previous-docs-", dir=html.parent) as backup:
        previous = Path(backup) / "html"
        if html.exists():
            html.rename(previous)
        try:
            shutil.move(str(snapshot), str(html))
        except Exception:
            if previous.exists():
                previous.rename(html)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535 (0 selects an available port)")
    docs = Path(__file__).resolve().parents[1] / "docs"
    build = docs / "_build"
    build.mkdir(exist_ok=True)
    html = build / "html"
    # Each live server owns a fresh snapshot. Another build cannot delete its
    # document root or make its homepage/assets disappear mid-request.
    with tempfile.TemporaryDirectory(prefix="local-docs-", dir=build) as staging:
        snapshot = Path(staging)
        if args.build_only:
            result = build_html(docs, snapshot)
            if result:
                return result
            publish_html(snapshot, html)
            print(f"HTML exported to {html}", flush=True)
            return 0
        handler = partial(DocsHandler, directory=str(snapshot))
        try:
            server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
        except OSError as error:
            advice = ("This environment blocks socket binding; run from a normal terminal."
                      if error.errno in {errno.EACCES, errno.EPERM} else
                      "Stop the existing server or use --port 0 for an available port.")
            print(f"Cannot bind localhost:{args.port}: {error}. "
                  f"{advice} Existing HTML was not changed.", file=sys.stderr)
            return 1
        with server:
            result = build_html(docs, snapshot)
            if result:
                return result
            print(f"Serving {snapshot}", flush=True)
            print(f"Documentation: http://127.0.0.1:{server.server_port}/index.html", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
