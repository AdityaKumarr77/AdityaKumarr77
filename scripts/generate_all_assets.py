import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

CUTOUT_PATH = "assets/cutout.png"
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_BOLD = r"C:\Windows\Fonts\consolab.ttf"

def get_font(size, bold=False):
    fp = FONT_BOLD if bold else FONT_PATH
    if os.path.exists(fp):
        return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

CODE_TOKENS = [
    ("const ", "kw"), ("aditya = ", "id"), ("new ", "kw"), ("FullStackArchitect", "type"), ("({ ", "op"),
    ("focus: ", "prop"), ("'AI Engineering & Scalability', ", "str"), ("dsa: ", "prop"), ("'Competitive Programming' ", "str"),
    ("}); ", "op"), ("function ", "kw"), ("solveHardProblem", "fn"), ("(graph: ", "op"), ("Graph<T>", "type"),
    ("): ", "op"), ("OptimalSolution ", "type"), ("{ ", "op"), ("const ", "kw"), ("dp = ", "id"),
    ("new ", "kw"), ("Map<number, number>(); ", "type"), ("return ", "kw"), ("dp.memoize(solve); ", "fn"),
    ("} ", "op"), ("async function ", "kw"), ("streamInference", "fn"), ("(prompt: ", "op"), ("string", "type"),
    ("): ", "op"), ("AsyncIterable<Token> ", "type"), ("{ ", "op"), ("const ", "kw"), ("llm = ", "id"),
    ("await ", "kw"), ("AICluster.connect(); ", "fn"), ("yield* ", "kw"), ("llm.generateStream(prompt); ", "fn"),
    ("} ", "op"), ("template ", "kw"), ("<typename Node> ", "type"), ("class ", "kw"), ("SegmentTree ", "type"),
    ("{ ", "op"), ("void ", "kw"), ("update", "fn"), ("(int idx, int val); ", "op"), ("int ", "kw"),
    ("query", "fn"), ("(int l, int r); ", "op"), ("}; ", "op"), ("export const ", "kw"), ("useReactStream = ", "fn"),
    ("() => ", "op"), ("{ ", "op"), ("const [data, setData] = ", "id"), ("useState", "fn"), ("(null); ", "op"),
    ("useEffect", "fn"), ("(() => { ", "op"), ("ws.connect(); ", "fn"), ("return () => ws.close(); ", "op"),
    ("}, []); ", "op"), ("return ", "kw"), ("{ data, status: 'CONNECTED' }; ", "str"), ("}; ", "op"),
    ("SELECT ", "kw"), ("u.developer, ", "id"), ("COUNT(c.id) ", "fn"), ("AS total_commits ", "prop"),
    ("FROM ", "kw"), ("users u ", "id"), ("JOIN commits c ON ", "kw"), ("u.id = c.author_id ", "id"),
    ("WHERE ", "kw"), ("c.created_at >= NOW() - INTERVAL '1 YEAR' ", "str"), ("GROUP BY ", "kw"),
    ("u.developer ", "id"), ("ORDER BY total_commits DESC; ", "kw"),
    ("docker compose ", "kw"), ("up -d --build && kubectl apply -f deploy.yaml; ", "fn"),
    ("git commit ", "kw"), ("-m 'feat: ship production microservices' && git push origin main; ", "str"),
    ("while ", "kw"), ("(alive) { ", "op"), ("learn(); ", "fn"), ("build(); ", "fn"), ("optimize(); ", "fn"),
    ("scale(); ", "fn"), ("} ", "op"),
]

TOKEN_COLORS = {
    "kw":   (0, 247, 255),    # Cyan
    "fn":   (56, 189, 248),   # Sky blue
    "type": (192, 132, 252),  # Purple
    "str":  (52, 211, 153),   # Emerald green
    "prop": (251, 191, 36),   # Amber
    "op":   (226, 232, 240),  # White
    "id":   (255, 255, 255),  # Pure white
}

def render_code_texture_on_canvas(canvas_w, canvas_h, target_cutout, px_offset, py_offset, font_size=6, char_w=3.6, line_h=7.0):
    photo_canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    photo_canvas.paste(target_cutout, (px_offset, py_offset), target_cutout)
    
    code_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(code_layer)
    font = get_font(font_size, bold=True)
    
    char_stream = []
    for text, tag in CODE_TOKENS:
        for ch in text:
            char_stream.append((ch, tag))
    stream_len = len(char_stream)
    stream_idx = 0
    
    num_lines = int(canvas_h // line_h) + 1
    
    for row in range(num_lines):
        y = row * line_h
        x = 0
        while x < canvas_w:
            ch, tag = char_stream[stream_idx % stream_len]
            stream_idx += 1
            
            sx = min(canvas_w - 1, max(0, int(x + char_w / 2)))
            sy = min(canvas_h - 1, max(0, int(y + line_h / 2)))
            
            pr, pg, pb, pa = photo_canvas.getpixel((sx, sy))
            base_col = TOKEN_COLORS.get(tag, (0, 247, 255))
            
            if pa > 25:
                lum = (0.299 * pr + 0.587 * pg + 0.114 * pb) / 255.0
                factor = max(0.25, lum)
                cr = int(min(255, (0.55 * base_col[0] + 0.45 * pr) * factor * 1.5))
                cg = int(min(255, (0.55 * base_col[1] + 0.45 * pg) * factor * 1.5))
                cb = int(min(255, (0.55 * base_col[2] + 0.45 * pb) * factor * 1.5))
                ca = int(min(255, 120 + lum * 135))
                c_draw.text((x, y), ch, font=font, fill=(cr, cg, cb, ca))
            else:
                if (row + int(x // 20)) % 3 == 0:
                    c_draw.text((x, y), ch, font=font, fill=(base_col[0], base_col[1], base_col[2], 28))
                elif (row + int(x // 15)) % 4 == 0:
                    c_draw.text((x, y), ch, font=font, fill=(0, 247, 255, 22))
                else:
                    c_draw.text((x, y), ch, font=font, fill=(20, 35, 60, 32))
            x += char_w
            
    return photo_canvas, code_layer

def create_code_portrait(out_path):
    W, H = 540, 680
    bg = Image.new("RGBA", (W, H), (8, 12, 22, 255))
    
    # Backlight glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    cx, cy = W // 2, int(H * 0.44)
    for r in range(270, 0, -8):
        a_cyan = int(48 * (1 - r / 270))
        g_draw.ellipse([cx - r, cy - r * 0.9, cx + r, cy + r * 0.9], fill=(0, 247, 255, a_cyan))
    for r in range(170, 0, -6):
        a_purp = int(52 * (1 - r / 170))
        g_draw.ellipse([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], fill=(168, 85, 247, a_purp))
    bg = Image.alpha_composite(bg, glow)

    # Cutout
    cutout = Image.open(CUTOUT_PATH).convert("RGBA")
    cw, ch = cutout.size
    target_h = int(H * 0.94)
    target_w = int(cw * (target_h / ch))
    src = cutout.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    src_rgb = ImageEnhance.Contrast(src.convert("RGB")).enhance(1.22)
    src_rgb = ImageEnhance.Sharpness(src_rgb).enhance(1.35)
    src_graded = src_rgb.convert("RGBA")
    src_graded.putalpha(src.split()[3])

    px_offset = (W - target_w) // 2
    py_offset = H - target_h

    photo_canvas, code_layer = render_code_texture_on_canvas(W, H, src_graded, px_offset, py_offset, font_size=6, char_w=3.6, line_h=7.0)

    # Ghost under-layer
    ghost = photo_canvas.copy()
    g_a = ghost.split()[3].point(lambda p: int(p * 0.52))
    ghost.putalpha(g_a)
    
    comp = Image.alpha_composite(bg, ghost)
    comp = Image.alpha_composite(comp, code_layer)

    # HUD Elements
    hud = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hud)

    cb = 26
    cyan = (0, 247, 255, 230)
    purp = (168, 85, 247, 230)
    h_draw.line([(10, 10), (10 + cb, 10)], fill=cyan, width=2)
    h_draw.line([(10, 10), (10, 10 + cb)], fill=cyan, width=2)
    h_draw.line([(W - 10, 10), (W - 10 - cb, 10)], fill=cyan, width=2)
    h_draw.line([(W - 10, 10), (W - 10, 10 + cb)], fill=cyan, width=2)
    h_draw.line([(10, H - 10), (10 + cb, H - 10)], fill=purp, width=2)
    h_draw.line([(10, H - 10), (10, H - 10 - cb)], fill=purp, width=2)
    h_draw.line([(W - 10, H - 10), (W - 10 - cb, H - 10)], fill=purp, width=2)
    h_draw.line([(W - 10, H - 10), (W - 10 - cb, H - 10)], fill=purp, width=2)

    h_draw.rounded_rectangle([14, 14, W - 14, H - 14], radius=12, outline=(0, 247, 255, 75), width=1)

    h_draw.rounded_rectangle([24, 22, 190, 46], radius=12, fill=(10, 16, 28, 235), outline=(0, 247, 255, 140), width=1)
    h_draw.ellipse([34, 31, 42, 39], fill=(0, 255, 157, 255))
    h_draw.text((48, 27), "SYSTEM // CODE_MATRIX", font=get_font(10), fill=(0, 247, 255, 240))
    h_draw.text((W - 145, 27), "ID: ADITYA.DEV-26", font=get_font(10), fill=(148, 163, 184, 200))

    bw = 370
    bx1 = (W - bw) // 2
    by1 = H - 54
    h_draw.rounded_rectangle([bx1, by1, bx1 + bw, by1 + 38], radius=19, fill=(10, 16, 28, 240), outline=(0, 247, 255, 160), width=1)
    h_draw.text((bx1 + 16, by1 + 11), "[#] ADITYA KUMAR JHA", font=get_font(11, bold=True), fill=(255, 255, 255, 255))
    h_draw.text((bx1 + 195, by1 + 12), "FULL STACK · AI · DSA", font=get_font(10), fill=(0, 247, 255, 240))

    comp = Image.alpha_composite(comp, hud)
    comp.convert("RGB").save(out_path, "PNG", quality=95)
    print("Generated code words portrait:", out_path)

def create_hero_banner(out_path):
    W, H = 1600, 640
    hero = Image.new("RGBA", (W, H), (8, 12, 22, 255))

    # Glows
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    px_center = 1250
    py_center = 320
    for r in range(450, 0, -15):
        alpha = int(48 * (1 - r / 450))
        g_draw.ellipse([px_center - r, py_center - r * 0.9, px_center + r, py_center + r * 0.9], fill=(0, 247, 255, alpha))
    for r in range(250, 0, -10):
        alpha = int(42 * (1 - r / 250))
        g_draw.ellipse([px_center - r, py_center - r * 0.8, px_center + r, py_center + r * 0.8], fill=(168, 85, 247, alpha))
    for r in range(350, 0, -15):
        alpha = int(25 * (1 - r / 350))
        g_draw.ellipse([350 - r, 300 - r * 0.8, 350 + r, 300 + r * 0.8], fill=(168, 85, 247, alpha))

    hero = Image.alpha_composite(hero, glow)

    # Right side: Aditya's photo in code texture
    cutout = Image.open(CUTOUT_PATH).convert("RGBA")
    cw, ch = cutout.size
    p_h = int(H * 0.98)
    p_w = int(cw * (p_h / ch))
    p_resized = cutout.resize((p_w, p_h), Image.Resampling.LANCZOS)
    
    p_rgb = ImageEnhance.Contrast(p_resized.convert("RGB")).enhance(1.2)
    p_rgb = ImageEnhance.Sharpness(p_rgb).enhance(1.35)
    p_graded = p_rgb.convert("RGBA")
    p_graded.putalpha(p_resized.split()[3])

    p_x = W - p_w - 60
    p_y = H - p_h

    # Render code texture over canvas
    photo_canvas, code_layer = render_code_texture_on_canvas(W, H, p_graded, p_x, p_y, font_size=7, char_w=4.2, line_h=8.0)

    # Fade mask for left edge of subject
    fade_mask = Image.new("L", (W, H), 255)
    f_draw = ImageDraw.Draw(fade_mask)
    for x in range(p_x, p_x + 140):
        ratio = (x - p_x) / 140.0
        f_draw.line([(x, 0), (x, H)], fill=int(255 * ratio))
        
    p_alpha = ImageChops.multiply(photo_canvas.split()[3], fade_mask)
    ghost = photo_canvas.copy()
    g_a = ImageChops.multiply(p_alpha, ghost.split()[3].point(lambda p: int(p * 0.50)))
    ghost.putalpha(g_a)

    code_alpha = ImageChops.multiply(code_layer.split()[3], fade_mask)
    code_layer.putalpha(code_alpha)

    hero = Image.alpha_composite(hero, ghost)
    hero = Image.alpha_composite(hero, code_layer)

    # Left terminal card
    term_x1, term_y1 = 60, 60
    term_x2, term_y2 = 980, 580
    term_w, term_h = term_x2 - term_x1, term_y2 - term_y1

    term_card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(term_card)

    t_draw.rounded_rectangle([term_x1, term_y1, term_x2, term_y2], radius=20, fill=(10, 16, 28, 235), outline=(0, 247, 255, 90), width=1)
    
    for i in range(term_w - 40):
        t = i / (term_w - 40)
        r_col = int(0 * (1 - t) + 255 * t)
        g_col = int(247 * (1 - t) + 0 * t)
        b_col = int(255 * (1 - t) + 200 * t)
        t_draw.line([(term_x1 + 20 + i, term_y1 + 1), (term_x1 + 21 + i, term_y1 + 1)], fill=(r_col, g_col, b_col, 255), width=3)

    t_draw.ellipse([term_x1 + 28, term_y1 + 22, term_x1 + 40, term_y1 + 34], fill=(255, 95, 86, 255))
    t_draw.ellipse([term_x1 + 48, term_y1 + 22, term_x1 + 60, term_y1 + 34], fill=(255, 189, 46, 255))
    t_draw.ellipse([term_x1 + 68, term_y1 + 22, term_x1 + 80, term_y1 + 34], fill=(39, 201, 63, 255))

    t_draw.text((term_x1 + 105, term_y1 + 20), "aditya@dev-matrix:~$ whoami", font=get_font(15), fill=(0, 247, 255, 230))
    t_draw.line([(term_x1 + 20, term_y1 + 52), (term_x2 - 20, term_y1 + 52)], fill=(30, 41, 59, 200), width=1)

    t_draw.text((term_x1 + 32, term_y1 + 72), "ADITYA KUMAR JHA", font=get_font(46, bold=True), fill=(255, 255, 255, 255))

    t_draw.text((term_x1 + 34, term_y1 + 144), "Full Stack Developer", font=get_font(21, bold=True), fill=(0, 247, 255, 255))
    t_draw.text((term_x1 + 310, term_y1 + 144), "|", font=get_font(21), fill=(100, 116, 139, 255))
    t_draw.text((term_x1 + 335, term_y1 + 144), "AI Builder", font=get_font(21, bold=True), fill=(255, 0, 200, 255))
    t_draw.text((term_x1 + 475, term_y1 + 144), "|", font=get_font(21), fill=(100, 116, 139, 255))
    t_draw.text((term_x1 + 500, term_y1 + 144), "DSA Architect", font=get_font(21, bold=True), fill=(0, 255, 157, 255))

    bullets = [
        ("> engineering scalable systems that grow, adapt and create impact", (226, 232, 240)),
        ("> primary stack: React · Next.js · Node.js · Python · TypeScript · PyTorch", (148, 163, 184)),
        ("> core strengths: Problem Solving · Clean Architecture · System Optimization", (148, 163, 184)),
        ("> credentials: B.Tech CSE · Certified Data Science & Analytics", (148, 163, 184)),
    ]

    for idx, (b_text, b_col) in enumerate(bullets):
        by = term_y1 + 200 + idx * 36
        t_draw.text((term_x1 + 34, by), b_text, font=get_font(16), fill=(b_col[0], b_col[1], b_col[2], 255))

    status_y = term_y1 + 380
    t_draw.rounded_rectangle([term_x1 + 34, status_y, term_x1 + 350, status_y + 44], radius=22, fill=(16, 24, 40, 240), outline=(0, 255, 157, 160), width=1)
    t_draw.ellipse([term_x1 + 52, status_y + 16, term_x1 + 64, status_y + 28], fill=(0, 255, 157, 255))
    t_draw.text((term_x1 + 76, status_y + 12), "OPEN TO OPPORTUNITIES", font=get_font(14, bold=True), fill=(255, 255, 255, 255))

    t_draw.rounded_rectangle([term_x1 + 370, status_y, term_x1 + 680, status_y + 44], radius=22, fill=(16, 24, 40, 240), outline=(0, 247, 255, 120), width=1)
    t_draw.text((term_x1 + 390, status_y + 12), "Ranchi, Jharkhand, India · Global Remote", font=get_font(13), fill=(0, 247, 255, 240))

    h_draw = ImageDraw.Draw(term_card)
    cb_len = 24
    h_draw.line([(16, 16), (16 + cb_len, 16)], fill=(0, 247, 255, 200), width=2)
    h_draw.line([(16, 16), (16, 16 + cb_len)], fill=(0, 247, 255, 200), width=2)
    h_draw.line([(W - 16, 16), (W - 16 - cb_len, 16)], fill=(0, 247, 255, 200), width=2)
    h_draw.line([(W - 16, 16), (W - 16, 16 + cb_len)], fill=(0, 247, 255, 200), width=2)
    h_draw.line([(16, H - 16), (16 + cb_len, H - 16)], fill=(255, 0, 200, 200), width=2)
    h_draw.line([(16, H - 16), (16, H - 16 - cb_len)], fill=(255, 0, 200, 200), width=2)
    h_draw.line([(W - 16, H - 16), (W - 16 - cb_len, H - 16)], fill=(255, 0, 200, 200), width=2)
    h_draw.line([(W - 16, H - 16), (W - 16 - cb_len, H - 16)], fill=(255, 0, 200, 200), width=2)

    hero = Image.alpha_composite(hero, term_card)
    hero.convert("RGB").save(out_path, "PNG", quality=95)
    print("Generated code texture hero:", out_path)

if __name__ == "__main__":
    create_code_portrait("assets/portrait-code.png")
    create_hero_banner("assets/hero.png")
