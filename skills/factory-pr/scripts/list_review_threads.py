"""List unresolved review threads on one GitHub PR without modifying it."""

import argparse
import json
import subprocess
import sys


QUERY = """
query($owner: String!, $repo: String!, $number: Int!, $after: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      url
      reviewThreads(first: 100, after: $after) {
        nodes {
          id isResolved isOutdated path line originalLine
          opening: comments(first: 1) { nodes { url body } }
          latest: comments(last: 1) { nodes { url body } }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
"""


def collect(owner, repo, number):
    threads = {}
    cursor = None
    seen_cursors = set()
    while True:
        command = ["gh", "api", "graphql", "-f", "query=" + QUERY,
                   "-f", "owner=" + owner, "-f", "repo=" + repo,
                   "-F", f"number={number}"]
        if cursor:
            command.extend(["-f", "after=" + cursor])
        response = json.loads(subprocess.check_output(command, text=True))
        if response.get("errors"):
            raise ValueError("GitHub returned an incomplete GraphQL result")
        repository = response["data"]["repository"]
        pr = repository and repository["pullRequest"]
        if not pr:
            raise ValueError("repository or PR unavailable")
        page = pr["reviewThreads"]
        for thread in page["nodes"]:
            threads[thread["id"]] = thread
        info = page["pageInfo"]
        if not info["hasNextPage"]:
            break
        cursor = info["endCursor"]
        if not cursor or cursor in seen_cursors:
            raise ValueError("incomplete review thread pagination")
        seen_cursors.add(cursor)
    return {"pr": pr["url"], "unresolved": [t for t in threads.values() if not t["isResolved"]]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("number", type=int)
    args = parser.parse_args()
    try:
        print(json.dumps(collect(args.owner, args.repo, args.number), ensure_ascii=False, indent=2))
    except (OSError, subprocess.CalledProcessError, KeyError, TypeError, ValueError) as exc:
        sys.exit(f"Could not read all PR review threads: {exc}")
