"""Check local hosting without requiring permission to bind network sockets."""

import errno
import importlib.util
from io import BytesIO, StringIO
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "serve_docs", Path(__file__).resolve().parents[1] / "scripts" / "serve_docs.py")
serve_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(serve_docs)


class QuietHandler(serve_docs.DocsHandler):
    def log_message(self, *args):
        pass


class RequestSocket:
    def __init__(self, request):
        self.request = BytesIO(request)
        self.response = BytesIO()

    def makefile(self, *args):
        return self.request

    def sendall(self, data):
        self.response.write(data)


class LocalDocsTests(unittest.TestCase):
    def request(self, root, path, method="GET"):
        connection = RequestSocket(f"{method} {path} HTTP/1.0\r\n\r\n".encode())
        QuietHandler(connection, ("127.0.0.1", 1234), SimpleNamespace(), directory=str(root))
        return connection.response.getvalue()

    def test_home_assets_removed_bookmarks_and_unknown_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("current homepage")
            (root / "asset.css").write_text("body {}")
            for path in ("/", "/index.html", "/index.html?refresh=1", "/asset.css"):
                response = self.request(root, path)
                self.assertIn(b"200 OK", response)
            for path in ("/examples.html", "/architecture.html?old=1"):
                for method in ("GET", "HEAD"):
                    response = self.request(root, path, method)
                    self.assertIn(b"302 Found", response)
                    self.assertIn(b"Location: /index.html", response)
            self.assertIn(b"404 File not found", self.request(root, "/unknown.html"))

    def test_port_conflict_does_not_build_or_replace_existing_html(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            html = root / "docs" / "_build" / "html"
            html.mkdir(parents=True)
            (html / "index.html").write_text("previous site")
            with patch.object(serve_docs, "__file__", str(root / "scripts" / "serve_docs.py")), \
                    patch("sys.argv", ["serve_docs.py"]), \
                    patch.object(serve_docs, "ThreadingHTTPServer",
                                 side_effect=OSError(errno.EADDRINUSE, "Address in use")), \
                    patch.object(serve_docs, "build_html") as build, \
                    patch("sys.stderr", new_callable=StringIO) as error:
                self.assertEqual(serve_docs.main(), 1)
                build.assert_not_called()
                self.assertIn("--port 0", error.getvalue())
            self.assertEqual((html / "index.html").read_text(), "previous site")

    def test_failed_build_preserves_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            html = root / "docs" / "_build" / "html"
            html.mkdir(parents=True)
            (html / "index.html").write_text("previous site")
            with patch.object(serve_docs, "__file__", str(root / "scripts" / "serve_docs.py")), \
                    patch("sys.argv", ["serve_docs.py", "--build-only"]), \
                    patch.object(serve_docs, "build_html", return_value=1):
                self.assertEqual(serve_docs.main(), 1)
            self.assertEqual((html / "index.html").read_text(), "previous site")

    def test_export_removes_stale_pages_without_touching_live_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            html, snapshot, live = (root / name for name in ("html", "snapshot", "live"))
            for folder in (html, snapshot, live):
                folder.mkdir()
                (folder / "index.html").write_text(folder.name)
            (html / "examples.html").write_text("obsolete")
            serve_docs.publish_html(snapshot, html)
            self.assertEqual((html / "index.html").read_text(), "snapshot")
            self.assertFalse((html / "examples.html").exists())
            self.assertIn(b"live", self.request(live, "/index.html"))
