"""Render assets/stats.svg: a graphite card of public GitHub stats.

Runs in the daily workflow with the built-in GITHUB_TOKEN, so it only
sees public data. No third-party service is involved.
"""
import json
import os
from datetime import datetime, timezone
import urllib.request
from html import escape

LOGIN = "Abubakarjutt"
QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    contributionsCollection {
      contributionCalendar { totalContributions }
      totalCommitContributions
      totalPullRequestContributions
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""

# Graphite board palette, shared with the banner.
BG_TOP, BG_BOTTOM = "#16191d", "#0f1114"
RULE, FLAP_TOP, FLAP_BOTTOM, FLAP_EDGE = "#2b3036", "#262a31", "#1d2126", "#30353d"
GLYPH, SOFT, LAMP = "#eef0ea", "#a3abb6", "#5cc995"
# Languages after the first fade from glyph to rule, so only the lead is green.
LANG_FILLS = [LAMP, "#c9cec6", "#8f969e", "#5d646c", "#3b4148"]
SANS = "Overpass, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'Overpass Mono', ui-monospace, 'SF Mono', Menlo, Consolas, monospace"


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}"},
    )
    with urllib.request.urlopen(req) as res:
        body = json.load(res)
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]["user"]


def summarise(user):
    repos = user["repositories"]
    cc = user["contributionsCollection"]
    joined = datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00"))
    years = (datetime.now(timezone.utc) - joined).days // 365
    sizes = {}
    for repo in repos["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            sizes[name] = sizes.get(name, 0) + edge["size"]
    total = sum(sizes.values()) or 1
    top = sorted(sizes.items(), key=lambda kv: kv[1], reverse=True)[:4]
    langs = [(name, size / total) for name, size in top]
    rest = 1 - sum(share for _, share in langs)
    if rest > 0.005:
        langs.append(("Other", rest))
    return {
        "stats": [
            ("Contributions, last year", cc["contributionCalendar"]["totalContributions"]),
            ("Commits, last year", cc["totalCommitContributions"]),
            ("Pull requests, last year", cc["totalPullRequestContributions"]),
            ("Years on GitHub", years),
        ],
        "langs": langs,
    }


def render(data):
    w, h, pad = 900, 236, 48
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">',
        '<title id="t">GitHub stats for Muhammad Abubakar: '
        + escape(", ".join(f"{label} {value}" for label, value in data["stats"]))
        + ". Languages: "
        + escape(", ".join(f"{n} {round(s * 100)}%" for n, s in data["langs"]))
        + "</title>",
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/></linearGradient>'
        f'<linearGradient id="flap" x1="0" y1="0" x2="0" y2="1"><stop offset="0.5" stop-color="{FLAP_TOP}"/><stop offset="0.5" stop-color="{FLAP_BOTTOM}"/></linearGradient></defs>',
        f'<rect width="{w}" height="{h}" fill="url(#bg)"/>',
    ]
    col = (w - pad * 2) / 4
    for i, (label, value) in enumerate(data["stats"]):
        x = pad + i * col
        out.append(f'<rect x="{x}" y="{pad - 8}" width="{col - 16}" height="58" rx="4" fill="url(#flap)" stroke="{FLAP_EDGE}"/>')
        out.append(f'<text x="{x + 16}" y="{pad + 32}" font-family="{MONO}" font-size="30" font-weight="600" fill="{GLYPH}">{value:,}</text>')
        out.append(f'<text x="{x}" y="{pad + 76}" font-family="{SANS}" font-size="13" fill="{SOFT}">{escape(label)}</text>')
    bar_y, bar_w = pad + 112, w - pad * 2
    out.append(f'<line x1="{pad}" y1="{bar_y - 16}" x2="{w - pad}" y2="{bar_y - 16}" stroke="{RULE}"/>')
    x = pad
    for i, (name, share) in enumerate(data["langs"]):
        seg = max(bar_w * share, 2)
        out.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{seg - 2:.1f}" height="8" rx="2" fill="{LANG_FILLS[i]}"/>')
        x += seg
    lx = pad
    for i, (name, share) in enumerate(data["langs"]):
        label = f"{name} {round(share * 100)}%"
        out.append(f'<circle cx="{lx + 5}" cy="{bar_y + 33}" r="5" fill="{LANG_FILLS[i]}"/>')
        out.append(f'<text x="{lx + 16}" y="{bar_y + 38}" font-family="{SANS}" font-size="14" fill="{GLYPH}">{escape(label)}</text>')
        lx += 16 + len(label) * 7.4 + 32
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    with open("assets/stats.svg", "w") as f:
        f.write(render(summarise(fetch())))
