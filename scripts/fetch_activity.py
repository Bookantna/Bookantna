"""Fetch the last year of contributions into data/activity.json.

Needs a token in GITHUB_TOKEN (the Actions token is enough for public
contributions; a PAT with read:user also counts private ones).

    GITHUB_TOKEN=$(gh auth token) python scripts/fetch_activity.py
"""

import json
import os
import urllib.request
from datetime import date
from pathlib import Path

USER = os.environ.get("GH_USER", "Bookantna")
OUT = Path(__file__).resolve().parent.parent / "data" / "activity.json"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": USER},
    )
    with urllib.request.urlopen(req) as r:
        body = json.load(r)
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    # Today may not have activity yet; it shouldn't break the current streak.
    tail = days[:-1] if days and days[-1]["count"] == 0 else days
    current = 0
    for d in reversed(tail):
        if not d["count"]:
            break
        current += 1
    return longest, current


def main():
    cal = fetch()
    weeks = [
        [{"date": d["date"], "count": d["contributionCount"], "level": LEVELS[d["contributionLevel"]]}
         for d in w["contributionDays"]]
        for w in cal["weeks"]
    ]
    days = [d for w in weeks for d in w]
    longest, current = streaks(days)
    data = {
        "updated": date.today().isoformat(),
        "total": cal["totalContributions"],
        "active_days": sum(1 for d in days if d["count"]),
        "longest": longest,
        "current": current,
        "weeks": weeks,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    print(f"{data['total']} contributions, longest {longest}, current {current}")


if __name__ == "__main__":
    main()
