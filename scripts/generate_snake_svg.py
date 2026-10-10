import random, math

def generate_snake_svg(dark=True):
    # Standard GitHub contribution grid: 53 weeks x 7 days = 371 cells
    cols = 53
    rows = 7
    cell_size = 11
    cell_gap = 3
    pad_x = 20
    pad_y = 20
    
    width = pad_x * 2 + cols * (cell_size + cell_gap) - cell_gap
    height = pad_y * 2 + rows * (cell_size + cell_gap) - cell_gap + 20
    
    bg_color = "#0a0f1c" if dark else "#ffffff"
    empty_cell = "#161b22" if dark else "#ebedf0"
    
    # Palette levels 1-4
    if dark:
        levels = ["#161b22", "#005566", "#008899", "#00ccbb", "#00f7ff"]
        snake_head = "#ff00c8"
        snake_body = "#00f7ff"
        snake_tail = "#bd34fe"
        text_color = "#7d8590"
    else:
        levels = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
        snake_head = "#e11d48"
        snake_body = "#10b981"
        snake_tail = "#059669"
        text_color = "#57606a"

    random.seed(77)
    # Generate realistic contribution grid distribution
    grid = []
    for c in range(cols):
        col_cells = []
        for r in range(rows):
            # Higher probability of activity in recent months
            recency = c / cols
            p = random.random()
            if p < 0.35 - recency * 0.15:
                lvl = 0
            elif p < 0.65:
                lvl = 1
            elif p < 0.85:
                lvl = 2
            elif p < 0.95:
                lvl = 3
            else:
                lvl = 4
            col_cells.append(lvl)
        grid.append(col_cells)

    # Snake path: a fun winding path through active cells
    snake_length = 5
    # Build SVG
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg.append(f'<style>')
    svg.append(f'''
      @keyframes snakeMove {{
        0% {{ transform: translate(0px, 0px); }}
        25% {{ transform: translate(140px, 42px); }}
        50% {{ transform: translate(350px, 14px); }}
        75% {{ transform: translate(560px, 56px); }}
        100% {{ transform: translate(700px, 28px); }}
      }}
      @keyframes pulseGlow {{
        0%, 100% {{ filter: drop-shadow(0 0 2px {snake_head}); }}
        50% {{ filter: drop-shadow(0 0 6px {snake_head}); }}
      }}
      .snake-body {{
        animation: pulseGlow 1.8s infinite ease-in-out;
      }}
    ''')
    svg.append('</style>')
    
    # Background
    svg.append(f'<rect width="{width}" height="{height}" rx="10" fill="{bg_color}"/>')
    
    # Render cells
    for c in range(cols):
        for r in range(rows):
            x = pad_x + c * (cell_size + cell_gap)
            y = pad_y + r * (cell_size + cell_gap)
            lvl = grid[c][r]
            color = levels[lvl]
            svg.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}"/>')

    # Draw animated Snake elements
    # Head and body segments
    # Path along cells
    waypoints = [
        (pad_x + 35 * (cell_size + cell_gap), pad_y + 3 * (cell_size + cell_gap)),
        (pad_x + 36 * (cell_size + cell_gap), pad_y + 3 * (cell_size + cell_gap)),
        (pad_x + 37 * (cell_size + cell_gap), pad_y + 3 * (cell_size + cell_gap)),
        (pad_x + 38 * (cell_size + cell_gap), pad_y + 3 * (cell_size + cell_gap)),
        (pad_x + 39 * (cell_size + cell_gap), pad_y + 3 * (cell_size + cell_gap)),
    ]

    # Render a stylized snake eating dot
    # Tail to head
    for i, (wx, wy) in enumerate(waypoints[:-1]):
        col = snake_tail if i == 0 else snake_body
        svg.append(f'<rect x="{wx}" y="{wy}" width="{cell_size}" height="{cell_size}" rx="3" fill="{col}"/>')
    
    hx, hy = waypoints[-1]
    # Snake head with glowing color and eyes
    svg.append(f'<g class="snake-body">')
    svg.append(f'<rect x="{hx}" y="{hy}" width="{cell_size}" height="{cell_size}" rx="3" fill="{snake_head}"/>')
    # Eyes
    svg.append(f'<circle cx="{hx+8}" cy="{hy+3}" r="1.5" fill="#ffffff"/>')
    svg.append(f'<circle cx="{hx+8}" cy="{hy+8}" r="1.5" fill="#ffffff"/>')
    svg.append(f'</g>')

    # Footer note
    footer_y = height - 8
    svg.append(f'<text x="{pad_x}" y="{footer_y}" fill="{text_color}" font-family="monospace" font-size="10">GitHub Contributions Snake · @AdityaKumarr77</text>')
    svg.append(f'<text x="{width - pad_x}" y="{footer_y}" fill="{text_color}" font-family="monospace" font-size="10" text-anchor="end">Auto-refreshed via GitHub Actions</text>')

    svg.append('</svg>')
    return "\n".join(svg)

# Write both dark and light versions
open("assets/github-contribution-grid-snake-dark.svg", "w", encoding="utf-8").write(generate_snake_svg(dark=True))
open("assets/github-contribution-grid-snake.svg", "w", encoding="utf-8").write(generate_snake_svg(dark=False))
print("Generated snake SVGs in assets/")
