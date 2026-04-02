"""
video_player.py  –  launched as a subprocess by game_selection_ui.py
Usage: python video_player.py "C:/path/to/video.mp4" "Game Name"
"""
import sys
import os
import pygame
import cv2

def main():
    if len(sys.argv) < 3:
        print("Usage: video_player.py <video_path> <game_name>")
        sys.exit(1)

    video_path = sys.argv[1]
    game_name  = sys.argv[2]

    # ── window ──────────────────────────────────────────────────────────────
    pygame.init()
    VW, VH = 860, 520
    win    = pygame.display.set_mode((VW, VH))
    pygame.display.set_caption(f"▶  {game_name}")
    clock  = pygame.time.Clock()

    # ── colours / fonts ─────────────────────────────────────────────────────
    BLACK  = (0,   0,   0)
    WHITE  = (255, 255, 255)
    GRAY   = (100, 100, 100)
    ACCENT = (90,  180, 255)
    RED    = (220,  50,  50)
    YELLOW = (255, 215,  0)

    font_sm  = pygame.font.Font(None, 22)
    font_med = pygame.font.Font(None, 32)
    font_big = pygame.font.Font(None, 54)

    # ── open video ──────────────────────────────────────────────────────────
    if not os.path.exists(video_path):
        # show "not found" screen and exit after key/click
        win.fill(BLACK)
        t1 = font_med.render(f"Video not found:", True, RED)
        t2 = font_sm.render(video_path, True, GRAY)
        t3 = font_sm.render("Press any key or close this window", True, WHITE)
        win.blit(t1, t1.get_rect(center=(VW//2, VH//2 - 30)))
        win.blit(t2, t2.get_rect(center=(VW//2, VH//2 + 10)))
        win.blit(t3, t3.get_rect(center=(VW//2, VH//2 + 50)))
        pygame.display.flip()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False
        pygame.quit()
        sys.exit(0)

    cap   = cv2.VideoCapture(video_path)
    fps   = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"[video_player] {video_path}  |  {total} frames @ {fps:.1f} fps")

    paused  = False
    surface = None
    pos     = 0

    BAR_X = 40
    BAR_Y = VH - 52
    BAR_W = VW - 80
    BAR_H = 7

    running = True
    while running:
        # ── events ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RIGHT:
                    seek = min(pos + int(fps * 5), total - 1)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, seek)
                    pos = seek
                elif event.key == pygame.K_LEFT:
                    seek = max(pos - int(fps * 5), 0)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, seek)
                    pos = seek

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if BAR_Y - 10 < my < BAR_Y + BAR_H + 10 and BAR_X < mx < BAR_X + BAR_W:
                    ratio = (mx - BAR_X) / BAR_W
                    seek  = int(ratio * total)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, seek)
                    pos = seek

        # ── read next frame ─────────────────────────────────────────────────
        if not paused:
            ret, frame = cap.read()
            if not ret:          # end of video → loop
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                pos = 0
                ret, frame = cap.read()
            if ret:
                # OpenCV gives BGR; convert to RGB then make pygame surface
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb = cv2.resize(rgb, (VW, VH - 70))   # leave room for HUD
                surface = pygame.surfarray.make_surface(rgb.swapaxes(0, 1))
                pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # ── draw ────────────────────────────────────────────────────────────
        win.fill(BLACK)

        if surface:
            win.blit(surface, (0, 0))

        # semi-transparent HUD bar at bottom
        hud = pygame.Surface((VW, 70), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 160))
        win.blit(hud, (0, VH - 70))

        # progress bar track
        pygame.draw.rect(win, GRAY,   (BAR_X, BAR_Y, BAR_W, BAR_H), border_radius=4)
        # filled
        if total > 0:
            filled = int(BAR_W * pos / total)
            pygame.draw.rect(win, ACCENT, (BAR_X, BAR_Y, filled, BAR_H), border_radius=4)
            pygame.draw.circle(win, WHITE, (BAR_X + filled, BAR_Y + BAR_H // 2), 8)

        # time stamps
        def fmt(f):
            secs = int(f / fps) if fps else 0
            return f"{secs // 60:02d}:{secs % 60:02d}"

        win.blit(font_sm.render(f"{fmt(pos)} / {fmt(total)}", True, WHITE),
                 (BAR_X, BAR_Y - 20))

        # status
        status = font_sm.render("⏸  PAUSED" if paused else "▶  PLAYING", True, YELLOW)
        win.blit(status, (VW - status.get_width() - BAR_X, BAR_Y - 20))

        # hint
        hint = font_sm.render("SPACE: pause  |  ← → : seek 5s  |  ESC: close", True, GRAY)
        win.blit(hint, hint.get_rect(center=(VW // 2, VH - 16)))

        pygame.display.flip()
        clock.tick(fps)

    cap.release()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()