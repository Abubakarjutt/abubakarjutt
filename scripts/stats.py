"""Render assets/stats.svg and assets/stats-dark.svg: public GitHub stats
in the sage-and-rust style of the banner and the portfolio site.

Runs in the daily workflow with the built-in GITHUB_TOKEN, so it only
sees public data. No third-party service is involved.
"""
import base64
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

# Engineering-manual palette, shared with the banner and abubakarjutt.github.io:
# cream paper (or green-black at night), sage for structure, rust for signal.
THEMES = {
    "light": {
        "bg": "#fafaf5", "dot": "rgba(26,26,26,0.08)", "cell": "#fafaf5",
        "ink": "#1a1a1a", "soft": "#4a4a4a", "rule": "rgba(26,26,26,0.16)",
        "sage": "#55705a", "rust": "#b4532a",
        "langs": ["#b4532a", "#55705a", "#8fa592", "#c3cfc4", "#d9d7cf"],
    },
    "dark": {
        "bg": "#10130f", "dot": "rgba(232,230,220,0.07)", "cell": "#10130f",
        "ink": "#e8e6dc", "soft": "#b4b2ab", "rule": "rgba(232,230,220,0.18)",
        "sage": "#9db89f", "rust": "#e08a5c",
        "langs": ["#e08a5c", "#9db89f", "#6f8a72", "#45574a", "#33392f"],
    },
}
MONO = "'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
HERE = os.path.dirname(os.path.abspath(__file__))
# VT323 (SIL OFL, see VT323-OFL.txt) is embedded so the numbers keep their
# pixel face: GitHub serves SVGs as images, which can't load web fonts.
with open(os.path.join(HERE, "vt323.woff2"), "rb") as f:
    VT323 = base64.b64encode(f.read()).decode()
PIXEL = "VT323, ui-monospace, monospace"


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


def render(data, theme):
    t = THEMES[theme]
    w, h, pad = 900, 236, 32
    title = (
        "GitHub stats for Muhammad Abubakar: "
        + ", ".join(f"{label} {value}" for label, value in data["stats"])
        + ". Languages: "
        + ", ".join(f"{n} {round(s * 100)}%" for n, s in data["langs"])
    )
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">',
        f'<title id="t">{escape(title)}</title>',
        "<defs>"
        f'<style>@font-face{{font-family:VT323;src:url(data:font/woff2;base64,{VT323}) format("woff2")}}</style>'
        f'<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t["dot"]}"/></pattern>'
        "</defs>",
        f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>',
        f'<rect width="{w}" height="{h}" fill="url(#dots)"/>',
        f'<text x="{pad}" y="{pad + 8}" font-family="{MONO}" font-size="11" letter-spacing="1.8" fill="{t["sage"]}">ON GITHUB · PUBLIC ACTIVITY</text>',
    ]
    # Four stat cells in one bordered strip.
    top, cell_h = pad + 24, 84
    col = (w - pad * 2) / 4
    out.append(f'<rect x="{pad + 0.5}" y="{top + 0.5}" width="{w - pad * 2 - 1}" height="{cell_h}" fill="{t["cell"]}" stroke="{t["rule"]}"/>')
    for i, (label, value) in enumerate(data["stats"]):
        x = pad + i * col
        if i:
            out.append(f'<line x1="{x + 0.5}" y1="{top}" x2="{x + 0.5}" y2="{top + cell_h}" stroke="{t["rule"]}"/>')
        out.append(f'<text x="{x + 18}" y="{top + 48}" font-family="{PIXEL}" font-size="48" fill="{t["rust"]}">{value:,}</text>')
        out.append(f'<text x="{x + 18}" y="{top + 70}" font-family="{MONO}" font-size="10" letter-spacing="1.2" fill="{t["soft"]}">{escape(label.upper())}</text>')
    # Language share: square segments, the lead language in rust.
    bar_y, bar_w = top + cell_h + 28, w - pad * 2
    x = pad
    for i, (name, share) in enumerate(data["langs"]):
        seg = max(bar_w * share, 2)
        out.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{seg - 2:.1f}" height="8" fill="{t["langs"][i]}"/>')
        x += seg
    lx = pad
    for i, (name, share) in enumerate(data["langs"]):
        label = f"{name} {round(share * 100)}%"
        out.append(f'<rect x="{lx}" y="{bar_y + 24}" width="10" height="10" fill="{t["langs"][i]}"/>')
        out.append(f'<text x="{lx + 18}" y="{bar_y + 33}" font-family="{MONO}" font-size="13" fill="{t["ink"]}">{escape(label)}</text>')
        lx += 18 + len(label) * 7.9 + 28
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    data = summarise(fetch())
    for theme, path in (("light", "assets/stats.svg"), ("dark", "assets/stats-dark.svg")):
        with open(path, "w") as f:
            f.write(render(data, theme))
