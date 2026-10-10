import math

def generate_contribution_graph():
    W, H = 900, 260
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Fira Code, Consolas, monospace">')
    svg.append('''<defs>
      <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#00f7ff" stop-opacity="0.35"/>
        <stop offset="100%" stop-color="#00f7ff" stop-opacity="0.0"/>
      </linearGradient>
      <linearGradient id="strokeGrad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#00f7ff"/>
        <stop offset="50%" stop-color="#bd34fe"/>
        <stop offset="100%" stop-color="#ff00c8"/>
      </linearGradient>
      <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#0a0f1c"/>
        <stop offset="100%" stop-color="#120c24"/>
      </linearGradient>
    </defs>''')
    
    # Card Background
    svg.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#bgGrad)" stroke="#00f7ff" stroke-opacity="0.35"/>')
    svg.append(f'<rect x="0" y="0" width="{W}" height="4" rx="2" fill="url(#strokeGrad)"/>')
    
    # Header
    svg.append(f'<text x="28" y="38" fill="#e6edf3" font-size="16" font-weight="700">$ git activity --user AdityaKumarr77 --frequency</text>')
    svg.append(f'<text x="{W-28}" y="38" fill="#7d8590" font-size="11" text-anchor="end">ANNUAL CONTRIBUTION CADENCE</text>')
    
    # Stat summary badges
    stats = [
        ("TOTAL CONTRIBUTIONS", "520+", "#00f7ff"),
        ("ACTIVE PULL REQUESTS", "48", "#00ff9d"),
        ("FEATURE REPOSITORIES", "18", "#ff00c8"),
        ("LONGEST COMMIT STREAK", "14 Days", "#bd34fe"),
    ]
    badge_y = 66
    for idx, (label, val, col) in enumerate(stats):
        bx = 28 + idx * 216
        svg.append(f'<rect x="{bx}" y="{badge_y}" width="204" height="42" rx="8" fill="#131b2e" stroke="{col}" stroke-opacity="0.3"/>')
        svg.append(f'<text x="{bx+14}" y="{badge_y+16}" fill="#7d8590" font-size="9" font-weight="600">{label}</text>')
        svg.append(f'<text x="{bx+14}" y="{badge_y+34}" fill="{col}" font-size="15" font-weight="700">{val}</text>')

    # Graph Area
    gx, gy, gw, gh = 40, 130, W - 80, 85
    
    # Months on x-axis
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    points_y = [25, 38, 52, 45, 68, 85, 72, 90, 82, 95, 88, 92] # activity curve
    
    coords = []
    for i, py in enumerate(points_y):
        x = gx + (i / (len(months) - 1)) * gw
        # invert y: higher point = lower y
        y = (gy + gh) - (py / 100.0) * gh
        coords.append((x, y))

    # Build smooth bezier curve
    path_d = [f"M {coords[0][0]} {coords[0][1]}"]
    for i in range(len(coords) - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i+1]
        cx1 = (x1 + x2) / 2
        cy1 = y1
        cx2 = (x1 + x2) / 2
        cy2 = y2
        path_d.append(f"C {cx1} {cy1}, {cx2} {cy2}, {x2} {y2}")
    
    stroke_path = " ".join(path_d)
    
    # Area path
    area_d = stroke_path + f" L {coords[-1][0]} {gy+gh} L {coords[0][0]} {gy+gh} Z"
    
    # Draw horizontal grid lines
    for line_ratio in [0.25, 0.5, 0.75, 1.0]:
        line_y = gy + gh * line_ratio
        svg.append(f'<line x1="{gx}" y1="{line_y}" x2="{gx+gw}" y2="{line_y}" stroke="#1e293b" stroke-width="1" stroke-dasharray="4 4"/>')

    # Draw Area and Stroke
    svg.append(f'<path d="{area_d}" fill="url(#areaGrad)"/>')
    svg.append(f'<path d="{stroke_path}" fill="none" stroke="url(#strokeGrad)" stroke-width="3" stroke-linecap="round"/>')
    
    # Draw glowing dots on vertices
    for x, y in coords:
        svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#00f7ff" stroke="#0a0f1c" stroke-width="2"/>')
        
    # Month Labels
    for i, m in enumerate(months):
        x = gx + (i / (len(months) - 1)) * gw
        svg.append(f'<text x="{x}" y="{gy+gh+22}" fill="#64748b" font-size="11" text-anchor="middle">{m}</text>')

    svg.append('</svg>')
    return "\n".join(svg)

open("assets/contribution-graph.svg", "w", encoding="utf-8").write(generate_contribution_graph())
print("Generated assets/contribution-graph.svg")
