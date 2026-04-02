import pygame
import sys
import os
import subprocess

pygame.init()

# ── Window ────────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 620
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GAME SELECTION")

# ── Colours ───────────────────────────────────────────────────────────────────
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
GREEN      = (0,   220, 80)
DARK_GREEN = (0,   150, 50)
GRAY       = (128, 128, 128)
LIGHT_BLUE = (100, 150, 255)
DARK_BG    = (22,  22,  35)
CARD_BG    = (40,  40,  60)
YELLOW     = (255, 215,  0)
RED        = (220,  50,  50)
ACCENT     = (90,  180, 255)

# ── Fonts ─────────────────────────────────────────────────────────────────────
font_small  = pygame.font.Font(None, 22)
font_large  = pygame.font.Font(None, 38)
font_title  = pygame.font.Font(None, 54)

# ── Card layout ───────────────────────────────────────────────────────────────
CARD_WIDTH   = 420
CARD_HEIGHT  = 310
CARD_SPACING = 40
IMG_PADDING  = 12
LABEL_HEIGHT = 36
IMG_WIDTH    = CARD_WIDTH  - IMG_PADDING * 2
IMG_HEIGHT   = CARD_HEIGHT - IMG_PADDING * 2 - LABEL_HEIGHT
CENTER_Y     = 140

# ── Button ────────────────────────────────────────────────────────────────────
BTN_WIDTH  = 220
BTN_HEIGHT = 52
BTN_Y      = SCREEN_HEIGHT - 90

# ── Build paths ───────────────────────────────────────────────────────────────
#
#   WORKSPACE/
#   ├── Game_project/
#   │   ├── QUESTION_1.py   <-- THIS file
#   │   └── video_player.py
#   ├── assets-20260331T.../
#   │   └── assets/
#   │       └── game selection cards/
#   └── video/              <-- videos are HERE
#       ├── escape_the_lava.mp4
#       ├── find_the_color.mp4
#       ├── red_light_green_light.mp4
#       └── sharp_shooter.mp4

THIS_DIR  = os.path.dirname(os.path.abspath(__file__))  # Game_project/
WORKSPACE = os.path.dirname(THIS_DIR)                    # one level up

# Video folder is directly inside the Game_project folder (where this script lives)
VIDEO_DIR = os.path.join(THIS_DIR, "video")

# Find the assets folder location
ASSETS_ROOT = None
candidates = [
    os.path.join(THIS_DIR, "assets"),
    os.path.join(WORKSPACE, "assets"),
]
for folder in candidates:
    if os.path.isdir(folder):
        ASSETS_ROOT = folder
        break

# game selection cards may be directly under assets, or under assets/game selection cards for old layout
CARDS_DIR = ""
if ASSETS_ROOT:
    direct = os.path.join(ASSETS_ROOT, "game selection cards")
    nested = os.path.join(ASSETS_ROOT, "assets", "game selection cards")
    if os.path.isdir(direct):
        CARDS_DIR = direct
    elif os.path.isdir(nested):
        CARDS_DIR = nested

print(f"[paths] WORKSPACE : {WORKSPACE}")
print(f"[paths] VIDEO_DIR : {VIDEO_DIR}")
print(f"[paths] CARDS_DIR : {CARDS_DIR}")

# ── Game data ─────────────────────────────────────────────────────────────────
games = [
    {
        "name"      : "Escape The Lava",
        "color"     : (200, 80,  60),
        "image"     : None,
        "filename"  : os.path.join(CARDS_DIR, "escape_the_lava.jpg"),
        "video_path": "https://drive.google.com/file/d/1q4xLStjq-ZqZn62eSUoY0tmLAgwD0w1I/view?usp=sharing",
    },
    {
        "name"      : "Find The Color",
        "color"     : (200, 160, 60),
        "image"     : None,
        "filename"  : os.path.join(CARDS_DIR, "find_the_color.jpg"),
        "video_path": "https://drive.google.com/file/d/1tELPmu0XY-2VylqNAdjMpmlLFn_yac52/view?usp=sharing",
    },
    {
        "name"      : "Red Light Green Light",
        "color"     : (60,  180, 80),
        "image"     : None,
        "filename"  : os.path.join(CARDS_DIR, "red_light_green_light.jpg"),
        "video_path": "https://drive.google.com/file/d/1PB1KMRokKApwNof6834C7YtevsWysaiv/view?usp=sharing",
    },
    {
        "name"      : "Sharp Shooter",
        "color"     : (110, 80,  220),
        "image"     : None,
        "filename"  : os.path.join(CARDS_DIR, "shooter.jpg"),
        "video_path": "https://drive.google.com/file/d/1JWug9EKKuPEpibwT6RxDvtwHgdyb6xRa/view?usp=sharing",
    },
]

# video_player.py is in the same folder as QUESTION_1.py
PLAYER_SCRIPT = os.path.join(THIS_DIR, "video_player.py")


import webbrowser

def launch_video(video_path: str, game_name: str):
    """Spawn video_player.py as a completely separate process or open URL in browser."""
    # Allow remote links (Google Drive or any HTTP link)
    if video_path.startswith("http://") or video_path.startswith("https://"):
        print(f"[video] Opening remote link in browser: {video_path}")
        webbrowser.open(video_path)
        return

    if not os.path.exists(PLAYER_SCRIPT):
        print(f"[ERROR] video_player.py not found at: {PLAYER_SCRIPT}")
        return

    if not os.path.exists(video_path):
        print(f"[ERROR] Video not found: {video_path}")
        return

    print(f"[video] Launching: {video_path}")
    subprocess.Popen(
        [sys.executable, PLAYER_SCRIPT, video_path, game_name],
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  IMAGE LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def make_placeholder(w, h, color, label):
    surf = pygame.Surface((w, h))
    surf.fill(color)
    pygame.draw.rect(surf, WHITE, (0, 0, w, h), 2)
    big = pygame.font.Font(None, 80)
    txt = big.render(label[0].upper(), True, WHITE)
    surf.blit(txt, txt.get_rect(center=(w // 2, h // 2)))
    return surf


def load_game_images():
    for i, game in enumerate(games):
        loaded = False
        path = game["filename"]
        if path and os.path.exists(path):
            try:
                img = pygame.image.load(path).convert()
                games[i]["image"] = pygame.transform.smoothscale(img, (IMG_WIDTH, IMG_HEIGHT))
                loaded = True
                print(f"[image] ✓ {game['name']}")
            except Exception as e:
                print(f"[image] ✗ {path}: {e}")
        else:
            print(f"[image] ✗ Not found: {path}")

        if not loaded:
            games[i]["image"] = make_placeholder(IMG_WIDTH, IMG_HEIGHT,
                                                  game["color"], game["name"])

load_game_images()


# ═══════════════════════════════════════════════════════════════════════════════
#  CARD DRAWING
# ═══════════════════════════════════════════════════════════════════════════════

def draw_card(x: int, game_data: dict, is_selected: bool, scale: float = 1.0):
    sw = int(CARD_WIDTH  * scale)
    sh = int(CARD_HEIGHT * scale)
    ox = (CARD_WIDTH  - sw) // 2
    oy = (CARD_HEIGHT - sh) // 2
    cx = x  + ox
    cy = CENTER_Y + oy

    # glow ring for selected card
    if is_selected:
        for ring in range(4, 0, -1):
            alpha = 60 + ring * 20
            gs = pygame.Surface((sw + ring * 6, sh + ring * 6), pygame.SRCALPHA)
            pygame.draw.rect(gs, (*YELLOW, alpha),
                             (0, 0, sw + ring * 6, sh + ring * 6), border_radius=14)
            screen.blit(gs, (cx - ring * 3, cy - ring * 3))

    # card background
    card_col = LIGHT_BLUE if is_selected else CARD_BG
    pygame.draw.rect(screen, card_col, (cx, cy, sw, sh), border_radius=12)
    pygame.draw.rect(screen, WHITE,    (cx, cy, sw, sh), 2, border_radius=12)

    # image (clipped so it never bleeds outside card)
    if game_data["image"]:
        iw = int(IMG_WIDTH  * scale)
        ih = int(IMG_HEIGHT * scale)
        img_scaled = pygame.transform.smoothscale(game_data["image"], (iw, ih))
        pad = int(IMG_PADDING * scale)
        screen.set_clip(pygame.Rect(cx, cy, sw, sh))
        screen.blit(img_scaled, (cx + pad, cy + pad))
        screen.set_clip(None)

    # label strip at bottom
    label_h    = int(LABEL_HEIGHT * scale)
    label_rect = pygame.Rect(cx, cy + sh - label_h, sw, label_h)
    label_surf = pygame.Surface((label_rect.w, label_rect.h), pygame.SRCALPHA)
    label_surf.fill((0, 0, 0, 200))
    screen.blit(label_surf, label_rect)

    name = game_data["name"]
    fs   = max(14, int(20 * scale))
    lf   = pygame.font.Font(None, fs)
    txt  = lf.render(name, True, WHITE)
    while txt.get_width() > sw - 16 and len(name) > 4:
        name = name[:-4] + "…"
        txt  = lf.render(name, True, WHITE)
    screen.blit(txt, txt.get_rect(center=(cx + sw // 2, label_rect.centery)))

    # SELECTED badge
    if is_selected:
        bf = pygame.font.Font(None, max(12, int(16 * scale)))
        bt = bf.render("SELECTED", True, BLACK)
        bw = bt.get_width() + 12
        bh = bt.get_height() + 6
        bx = cx + sw - bw - 8
        by = cy + 8
        pygame.draw.rect(screen, YELLOW, (bx, by, bw, bh), border_radius=6)
        screen.blit(bt, bt.get_rect(center=(bx + bw // 2, by + bh // 2)))

    # small play icon (shows video is clickable)
    r   = int(14 * scale)
    pcx = cx + sw - r - 10
    pcy = cy + sh - label_h - r - 8
    pygame.draw.circle(screen, RED,   (pcx, pcy), r)
    pygame.draw.circle(screen, WHITE, (pcx, pcy), r, 1)
    pygame.draw.polygon(screen, WHITE, [
        (pcx - r // 3, pcy - r // 2),
        (pcx + r // 2, pcy),
        (pcx - r // 3, pcy + r // 2),
    ])


# ═══════════════════════════════════════════════════════════════════════════════
#  START BUTTON
# ═══════════════════════════════════════════════════════════════════════════════

def draw_start_button(game_name: str, hovered: bool) -> pygame.Rect:
    bx   = SCREEN_WIDTH // 2 - BTN_WIDTH // 2
    rect = pygame.Rect(bx, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
    pygame.draw.rect(screen, BLACK, (bx + 4, BTN_Y + 4, BTN_WIDTH, BTN_HEIGHT), border_radius=12)
    pygame.draw.rect(screen, LIGHT_BLUE if hovered else DARK_BG, rect, border_radius=12)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=12)
    btn_txt = font_large.render("▶  START GAME", True, WHITE)
    screen.blit(btn_txt, btn_txt.get_rect(center=rect.center))
    lbl = font_small.render(f"Selected:  {game_name}", True, YELLOW)
    screen.blit(lbl, lbl.get_rect(center=(SCREEN_WIDTH // 2, BTN_Y - 22)))
    return rect


# ═══════════════════════════════════════════════════════════════════════════════
#  BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════════

def draw_background():
    screen.fill(DARK_BG)
    for gx in range(0, SCREEN_WIDTH, 60):
        pygame.draw.line(screen, (30, 30, 48), (gx, 0), (gx, SCREEN_HEIGHT))
    for gy in range(0, SCREEN_HEIGHT, 60):
        pygame.draw.line(screen, (30, 30, 48), (0, gy), (SCREEN_WIDTH, gy))
    for i in range(110):
        v = 28 + i // 3
        pygame.draw.line(screen, (v, v, v + 20), (0, i), (SCREEN_WIDTH, i))


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def _snap(idx):
    return float(SCREEN_WIDTH // 2 - CARD_WIDTH // 2 - idx * (CARD_WIDTH + CARD_SPACING))

selected_game  = 0
current_offset = _snap(0)
target_offset  = current_offset
ANIM_SPEED     = 0.18

mouse_dragging = False
drag_start_x   = 0
drag_start_off = 0.0
SWIPE_THRESH   = 50

clock   = pygame.time.Clock()
running = True

while running:
    btn_hover = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and selected_game > 0:
                selected_game -= 1
                target_offset  = _snap(selected_game)
            elif event.key == pygame.K_RIGHT and selected_game < len(games) - 1:
                selected_game += 1
                target_offset  = _snap(selected_game)
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                print(f"🚀 Launching {games[selected_game]['name']}")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # check start button
            btn_r = pygame.Rect(SCREEN_WIDTH // 2 - BTN_WIDTH // 2, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
            if btn_r.collidepoint(mx, my):
                print(f"🚀 Launching {games[selected_game]['name']}")
            else:
                # check card clicks
                for i in range(len(games)):
                    lx = int(current_offset) + i * (CARD_WIDTH + CARD_SPACING)
                    if pygame.Rect(lx, CENTER_Y, CARD_WIDTH, CARD_HEIGHT).collidepoint(mx, my):
                        selected_game = i
                        target_offset = _snap(selected_game)
                        launch_video(games[i]["video_path"], games[i]["name"])
                        break

            mouse_dragging = True
            drag_start_x   = mx
            drag_start_off = current_offset

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if mouse_dragging:
                dist = event.pos[0] - drag_start_x
                if abs(dist) > SWIPE_THRESH:
                    if dist > 0 and selected_game > 0:
                        selected_game -= 1
                    elif dist < 0 and selected_game < len(games) - 1:
                        selected_game += 1
                target_offset  = _snap(selected_game)
                mouse_dragging = False

    if mouse_dragging:
        current_offset = drag_start_off + (pygame.mouse.get_pos()[0] - drag_start_x)
        target_offset  = current_offset

    current_offset += (target_offset - current_offset) * ANIM_SPEED

    btn_r     = pygame.Rect(SCREEN_WIDTH // 2 - BTN_WIDTH // 2, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
    btn_hover = btn_r.collidepoint(pygame.mouse.get_pos())

    # ── draw ─────────────────────────────────────────────────────────────────
    draw_background()

    screen.blit(font_title.render("GAME SELECTION", True, WHITE),
                font_title.render("GAME SELECTION", True, WHITE).get_rect(
                    center=(SCREEN_WIDTH // 2, 50)))
    hint = font_small.render("← → browse  |  click card to preview video  |  START to play", True, GRAY)
    screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 90)))

    for i, game in enumerate(games):
        lx = int(current_offset) + i * (CARD_WIDTH + CARD_SPACING)
        if lx + CARD_WIDTH < -50 or lx > SCREEN_WIDTH + 50:
            continue
        dist  = abs(lx + CARD_WIDTH // 2 - SCREEN_WIDTH // 2)
        scale = max(0.72, 1.0 - dist / (SCREEN_WIDTH * 0.9) * 0.30)
        draw_card(lx, game, i == selected_game, scale)

    if selected_game > 0:
        a = font_title.render("◀", True, WHITE)
        screen.blit(a, a.get_rect(center=(28, CENTER_Y + CARD_HEIGHT // 2)))
    if selected_game < len(games) - 1:
        a = font_title.render("▶", True, WHITE)
        screen.blit(a, a.get_rect(center=(SCREEN_WIDTH - 28, CENTER_Y + CARD_HEIGHT // 2)))

    draw_start_button(games[selected_game]["name"], btn_hover)

    # dot indicators
    dot_gap   = 18
    dot_start = SCREEN_WIDTH // 2 - (len(games) * dot_gap) // 2
    for di in range(len(games)):
        pygame.draw.circle(screen, YELLOW if di == selected_game else GRAY,
                           (dot_start + di * dot_gap, BTN_Y - 40),
                           5 if di == selected_game else 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()