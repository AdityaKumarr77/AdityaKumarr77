#!/usr/bin/env python3
"""Fetch live LeetCode stats and render assets/leetcode-stats.svg (self-hosted, no third-party card service)."""
import json, os, sys, datetime as dt, urllib.request

USER = os.environ.get("LEETCODE_USER", "AdityaKumar77")
OUT = os.environ.get("OUT", "assets/leetcode-stats.svg")

QUERY = """
query stats($u: String!) {
  allQuestionsCount { difficulty count }
  matchedUser(username: $u) {
    profile { ranking }
    submitStatsGlobal { acSubmissionNum { difficulty count } }
    submissionCalendar
    badges { displayName }
  }
  userContestRanking(username: $u) { rating attendedContestsCount topPercentage }
}"""

def fetch():
    if os.environ.get("LC_MOCK"):
        import random; random.seed(3)
        now = int(dt.datetime.now(dt.timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0).timestamp())
        cal = {str(now-86400*i): random.randint(1,6) for i in range(200) if random.random()<0.45}
        return {"data":{"allQuestionsCount":[{"difficulty":"All","count":3600},{"difficulty":"Easy","count":900},{"difficulty":"Medium","count":1880},{"difficulty":"Hard","count":820}],
          "matchedUser":{"profile":{"ranking":412345},"submitStatsGlobal":{"acSubmissionNum":[{"difficulty":"All","count":187},{"difficulty":"Easy","count":92},{"difficulty":"Medium","count":81},{"difficulty":"Hard","count":14}]},
          "submissionCalendar":json.dumps(cal),"badges":[{"displayName":"50 Days Badge 2025"}]},
          "userContestRanking":{"rating":1612.4,"attendedContestsCount":9,"topPercentage":38.2}}}
    body = json.dumps({"query": QUERY, "variables": {"u": USER}}).encode()
    req = urllib.request.Request("https://leetcode.com/graphql", data=body, headers={
        "Content-Type": "application/json", "Referer": f"https://leetcode.com/u/{USER}/",
        "User-Agent": "Mozilla/5.0 (compatible; profile-readme-bot)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;")

def render(d):
    data = d["data"]; mu = data["matchedUser"]
    if not mu: raise SystemExit(f"LeetCode user {USER} not found")
    solved = {x["difficulty"]: x["count"] for x in mu["submitStatsGlobal"]["acSubmissionNum"]}
    total = {x["difficulty"]: x["count"] for x in data["allQuestionsCount"]}
    rank = mu["profile"]["ranking"]
    cal = {int(k): v for k, v in json.loads(mu["submissionCalendar"] or "{}").items()}
    days = {dt.datetime.fromtimestamp(k, dt.timezone.utc).date(): v for k, v in cal.items()}
    today = dt.datetime.now(dt.timezone.utc).date()
    # streaks
    cur = 0; d0 = today if today in days else today - dt.timedelta(days=1)
    while d0 in days: cur += 1; d0 -= dt.timedelta(days=1)
    best = run = 0; prev = None
    for day in sorted(days):
        run = run + 1 if prev and (day - prev).days == 1 else 1
        best = max(best, run); prev = day
    year_active = sum(1 for dd in days if (today - dd).days < 365)
    cr = data.get("userContestRanking") or {}
    badges = len(mu.get("badges") or [])
    updated = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    W, H = 900, 330
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Fira Code, DejaVu Sans Mono, Consolas, monospace">',
      '<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#00f7ff"/><stop offset="1" stop-color="#ff00c8"/></linearGradient>'
      '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0f1c"/><stop offset="1" stop-color="#140a26"/></linearGradient></defs>',
      f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)" stroke="#00f7ff" stroke-opacity=".35"/>',
      f'<rect x="0" y="0" width="{W}" height="4" rx="2" fill="url(#g)"/>',
      f'<text x="28" y="40" fill="#e6edf3" font-size="18" font-weight="700">$ leetcode --user {esc(USER)} --live</text>',
      f'<text x="{W-28}" y="40" fill="#7d8590" font-size="11" text-anchor="end">updated {updated}</text>']
    # ring
    T = solved.get("All", 0); TT = max(total.get("All", 1), 1)
    import math
    cx, cy, r = 105, 150, 62; circ = 2*math.pi*r; frac = min(T/TT, 1)
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1c2433" stroke-width="12"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#g)" stroke-width="12" stroke-linecap="round" stroke-dasharray="{circ*frac:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy})"/>')
    s.append(f'<text x="{cx}" y="{cy+6}" fill="#fff" font-size="30" font-weight="700" text-anchor="middle">{T}</text>')
    s.append(f'<text x="{cx}" y="{cy+26}" fill="#7d8590" font-size="11" text-anchor="middle">SOLVED / {TT}</text>')
    # difficulty bars
    bx = 215
    for i, (name, col) in enumerate([("Easy", "#00e5a0"), ("Medium", "#ffb020"), ("Hard", "#ff4d6d")]):
        y = 92 + i*44; a = solved.get(name, 0); b = max(total.get(name, 1), 1)
        s.append(f'<text x="{bx}" y="{y}" fill="{col}" font-size="13" font-weight="700">{name}</text>')
        s.append(f'<text x="{bx+250}" y="{y}" fill="#c9d1d9" font-size="13" text-anchor="end">{a} / {b}</text>')
        s.append(f'<rect x="{bx}" y="{y+8}" width="250" height="8" rx="4" fill="#1c2433"/>')
        s.append(f'<rect x="{bx}" y="{y+8}" width="{max(250*a/b,4 if a else 0):.1f}" height="8" rx="4" fill="{col}"/>')
    # metrics
    metrics = [("GLOBAL RANK", f"{rank:,}" if rank else "—"), ("CURRENT STREAK", f"{cur} days"), ("LONGEST STREAK", f"{best} days"),
               ("ACTIVE DAYS (1Y)", str(year_active)),
               ("CONTEST RATING", f"{cr['rating']:.0f}" if cr.get("rating") else "—"),
               ("BADGES", str(badges))]
    for i, (k, v) in enumerate(metrics):
        x = 520 + (i % 2)*190; y = 82 + (i//2)*50
        s.append(f'<text x="{x}" y="{y}" fill="#7d8590" font-size="10">{k}</text>')
        s.append(f'<text x="{x}" y="{y+22}" fill="#00f7ff" font-size="19" font-weight="700">{esc(v)}</text>')
    # heatmap last 26 weeks
    weeks = 26; cell = 11; gap = 3
    start = today - dt.timedelta(days=today.weekday()+1 if today.weekday()!=6 else 0) - dt.timedelta(weeks=weeks-1)
    hx, hy = 215, 240
    s.append(f'<text x="28" y="{hy+30}" fill="#7d8590" font-size="10">ACTIVITY · 26 WEEKS</text>')
    for w in range(weeks):
        for dd in range(7):
            day = start + dt.timedelta(weeks=w, days=dd)
            if day > today: continue
            c = days.get(day, 0)
            col = "#161d2b" if c == 0 else "#0e5560" if c < 2 else "#0ca5b0" if c < 4 else "#00f7ff" if c < 7 else "#ff5ce1"
            s.append(f'<rect x="{hx+w*(cell+gap)}" y="{hy+dd*(cell+gap)-10}" width="{cell}" height="{cell}" rx="2" fill="{col}"/>')
    s.append('</svg>')
    return "\n".join(s)

if __name__ == "__main__":
    try:
        d = fetch()
    except Exception as e:
        print("fetch failed:", e, file=sys.stderr); sys.exit(1)
    if d.get("errors") and not d.get("data"): print(d["errors"], file=sys.stderr); sys.exit(1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(render(d))
    print("wrote", OUT)
