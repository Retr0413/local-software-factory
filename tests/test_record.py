"""Verify the delivery semantics of the record skill in a disposable repository."""

import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/factory-record/scripts/record.py"


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.cwd = Path(temp.name)
        subprocess.run(["git", "init", "-q", self.cwd], check=True)
        self.log = self.cwd / ".git/local-software-factory/runs.jsonl"

    def deliver(self, **fields):
        entry = {"task": "#8", "outcome": "confirmed", **fields}
        return subprocess.run([sys.executable, SCRIPT], cwd=self.cwd, input=json.dumps(entry),
                              text=True, capture_output=True)

    def entries(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_parallel_redelivery_and_distinct_observations(self):
        with concurrent.futures.ThreadPoolExecutor(4) as pool:
            jobs = [pool.submit(self.deliver, event_id="s-1") for _ in range(8)]
        for job in jobs:
            job.result().check_returncode()
        self.deliver(event_id="s-2").check_returncode()
        self.deliver(task="#9", event_id="s-1").check_returncode()
        self.assertEqual([(r["task"], r["event_id"]) for r in self.entries()],
                         [("#8", "s-1"), ("#8", "s-2"), ("#9", "s-1")])

    def test_conflicting_payload_fails_without_overwriting(self):
        self.deliver(event_id="s-1").check_returncode()
        original = self.log.read_bytes()
        self.assertNotEqual(self.deliver(event_id="s-1", outcome="failed").returncode, 0)
        self.assertEqual(self.log.read_bytes(), original)

    def test_legacy_entries_and_optional_key(self):
        self.deliver().check_returncode()
        self.deliver().check_returncode()
        self.deliver(event_id="s-1").check_returncode()
        self.assertEqual(len(self.entries()), 3)
