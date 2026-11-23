"""Verify that PR triage never reports an incomplete thread list as complete."""

import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/factory-pr/scripts/list_review_threads.py"
spec = importlib.util.spec_from_file_location("review_threads", SCRIPT)
threads = importlib.util.module_from_spec(spec)
spec.loader.exec_module(threads)


def page(nodes, has_next=False, cursor=None):
    return json.dumps({"data": {"repository": {"pullRequest": {
        "url": "https://github.com/example/repo/pull/41",
        "reviewThreads": {"nodes": nodes, "pageInfo": {"hasNextPage": has_next, "endCursor": cursor}},
    }}}})


class ReviewThreadPagination(unittest.TestCase):
    def test_returns_unresolved_by_id_including_outdated(self):
        old = {"id": "A", "isResolved": False, "isOutdated": True}
        other = {"id": "B", "isResolved": False, "isOutdated": False}
        done = {"id": "C", "isResolved": True}
        with patch.object(threads.subprocess, "check_output", side_effect=[
            page([old, done], True, "next"), page([old, other]),
        ]) as gh:
            result = threads.collect("example", "repo", 41)
            self.assertEqual(result["unresolved"], [old, other])
            self.assertIn("after=next", gh.call_args.args[0])

    def test_partial_response_is_an_error(self):
        with patch.object(threads.subprocess, "check_output", side_effect=[
            page([], True, "next"), json.dumps({"errors": [{"message": "unavailable"}]}),
        ]):
            with self.assertRaises(ValueError):
                threads.collect("example", "repo", 41)

    def test_refuses_a_stuck_cursor(self):
        with patch.object(threads.subprocess, "check_output", return_value=page([], True, "same")):
            with self.assertRaises(ValueError):
                threads.collect("example", "repo", 41)
