#!/usr/bin/env python3
"""
SentinelAgent — Professional Video Demo Generator
Renders a 1080p 30fps MP4 product demonstration video.
"""
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1920, 1080
FPS = 30

FONT_CODE_TITLE = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 38)
FONT_CODE = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 26)
FONT_CODE_SM = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)
FONT_HERO = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 64)
FONT_SUB = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 32)
FONT_TAG = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)

# Colors
BG_DARK = (11, 15, 23)
TERM_BG = (15, 20, 31)
CARD_BORDER = (45, 55, 72)
TEXT_WHITE = (241, 245, 249)
TEXT_MUTED = (148, 163, 184)
ACCENT_CYAN = (56, 189, 248)
ACCENT_BLUE = (129, 140, 248)
SUCCESS_GREEN = (16, 185, 129)
DANGER_RED = (239, 68, 68)
WARN_YELLOW = (245, 158, 11)

def draw_header(draw, title, subtitle=None):
    # Brand Bar
    draw.rectangle([0, 0, WIDTH, 80], fill=(15, 23, 42))
    draw.line([(0, 80), (WIDTH, 80)], fill=CARD_BORDER, width=2)
    
    # Logo
    draw.rounded_rectangle([40, 18, 84, 62], radius=8, fill=ACCENT_CYAN)
    draw.text((54, 22), "⚡", font=FONT_CODE, fill=(15, 23, 42))
    draw.text((100, 24), "SentinelAgent", font=FONT_CODE_TITLE, fill=TEXT_WHITE)
    
    # Event badge
    draw.rounded_rectangle([WIDTH - 480, 22, WIDTH - 40, 60], radius=16, fill=(30, 41, 59), outline=CARD_BORDER)
    draw.text((WIDTH - 460, 28), "OmniRush Frontier Buildathon 2026", font=FONT_TAG, fill=ACCENT_CYAN)

    if title:
        draw.text((80, 110), title, font=FONT_HERO, fill=TEXT_WHITE)
    if subtitle:
        draw.text((80, 185), subtitle, font=FONT_SUB, fill=TEXT_MUTED)

def draw_window(draw, x, y, w, h, title="terminal — bash"):
    # Window container
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=TERM_BG, outline=CARD_BORDER, width=2)
    # Window header bar
    draw.rounded_rectangle([x, y, x + w, y + 44], radius=12, fill=(24, 32, 47))
    draw.rectangle([x, y + 24, x + w, y + 44], fill=(24, 32, 47)) # square bottom corners of bar
    draw.line([(x, y + 44), (x + w, y + 44)], fill=CARD_BORDER, width=2)
    
    # Traffic light dots
    draw.ellipse([x + 18, y + 16, x + 30, y + 28], fill=(255, 95, 86))
    draw.ellipse([x + 38, y + 16, x + 50, y + 28], fill=(255, 189, 46))
    draw.ellipse([x + 58, y + 16, x + 70, y + 28], fill=(39, 201, 63))
    
    # Header title
    draw.text((x + w//2 - 80, y + 12), title, font=FONT_CODE_SM, fill=TEXT_MUTED)

def create_frame(scene_type, progress=1.0):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    if scene_type == "intro":
        draw_header(draw, None)
        # Center card
        cx, cy = WIDTH // 2, HEIGHT // 2
        draw.rounded_rectangle([cx - 550, cy - 260, cx + 550, cy + 240], radius=20, fill=TERM_BG, outline=ACCENT_CYAN, width=2)
        
        draw.text((cx - 480, cy - 200), "SentinelAgent", font=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 80), fill=ACCENT_CYAN)
        draw.text((cx - 480, cy - 100), "Autonomous SRE Incident Remediation & Self-Healing Agent", font=FONT_HERO, fill=TEXT_WHITE)
        draw.text((cx - 480, cy - 10), "Built with OmniRush for the Frontier Buildathon 2026", font=FONT_SUB, fill=TEXT_MUTED)
        
        # Track Badge
        draw.rounded_rectangle([cx - 480, cy + 60, cx - 140, cy + 115], radius=12, fill=(30, 58, 138), outline=ACCENT_BLUE)
        draw.text((cx - 460, cy + 73), "Track: Agents & Automation", font=FONT_TAG, fill=TEXT_WHITE)
        
        # Participant Badge
        draw.rounded_rectangle([cx - 120, cy + 60, cx + 180, cy + 115], radius=12, fill=(19, 78, 74), outline=SUCCESS_GREEN)
        draw.text((cx - 100, cy + 73), "Author: @sundeep8967", font=FONT_TAG, fill=TEXT_WHITE)

        # Rebuildable Badge
        draw.rounded_rectangle([cx + 200, cy + 60, cx + 480, cy + 115], radius=12, fill=(49, 46, 129), outline=ACCENT_CYAN)
        draw.text((cx + 220, cy + 73), "✓ 8/8 Judge Rebuild Verified", font=FONT_TAG, fill=TEXT_WHITE)

    elif scene_type == "incident":
        draw_header(draw, "1. Production Incident Ingestion", "Simulated production webhook alerts on high crash rates in transaction batch worker")
        draw_window(draw, 100, 240, WIDTH - 200, 720, "incident_webhook.json")
        
        lines = [
            ('{', TEXT_WHITE),
            ('  "incident_id": "inc_2026_98124_alpha",', ACCENT_CYAN),
            ('  "service": "billing-metrics-worker",', TEXT_WHITE),
            ('  "severity": "CRITICAL",', DANGER_RED),
            ('  "alert": "HighCrashRate_BatchMetrics",', WARN_YELLOW),
            ('  "exception": {', TEXT_WHITE),
            ('    "type": "ZeroDivisionError",', DANGER_RED),
            ('    "message": "float division by zero at process_batch_transactions:34",', DANGER_RED),
            ('    "secondary": "TypeError: unsupported operand type(s) for *: \'NoneType\' and \'float\'",', DANGER_RED),
            ('    "source_file": "demo_repo/metrics_engine.py",', ACCENT_CYAN),
            ('    "reproduction_suite": "demo_repo/test_metrics_engine.py"', SUCCESS_GREEN),
            ('  }', TEXT_WHITE),
            ('}', TEXT_WHITE),
            ('', TEXT_WHITE),
            ('🚨 [STATUS]: Alert ingested. SentinelAgent initiating autonomous resolution loop...', WARN_YELLOW)
        ]
        
        y_cursor = 310
        visible_count = int(len(lines) * progress)
        for i in range(min(visible_count, len(lines))):
            text, color = lines[i]
            draw.text((140, y_cursor), text, font=FONT_CODE, fill=color)
            y_cursor += 36

    elif scene_type == "test_fail":
        draw_header(draw, "2. Baseline Pytest Verification", "Reproducing seeded failures against untouched demo repository")
        draw_window(draw, 100, 240, WIDTH - 200, 720, "terminal — pytest")
        
        lines = [
            ('$ pytest demo_repo/test_metrics_engine.py -v', ACCENT_CYAN),
            ('============================= test session starts =============================', TEXT_MUTED),
            ('platform darwin -- Python 3.11.14, pytest-8.3.4, pluggy-1.5.0', TEXT_MUTED),
            ('rootdir: .', TEXT_MUTED),
            ('collected 3 items', TEXT_WHITE),
            ('', TEXT_WHITE),
            ('demo_repo/test_metrics_engine.py::test_standard_batch PASSED            [ 33%]', SUCCESS_GREEN),
            ('demo_repo/test_metrics_engine.py::test_empty_batch FAILED               [ 66%]', DANGER_RED),
            ('demo_repo/test_metrics_engine.py::test_missing_and_none_amounts FAILED [100%]', DANGER_RED),
            ('', TEXT_WHITE),
            ('================================== FAILURES ===================================', DANGER_RED),
            ('______________________________ test_empty_batch _______________________________', DANGER_RED),
            ('    average = total_amount / valid_count', DANGER_RED),
            ('E   ZeroDivisionError: float division by zero', DANGER_RED),
            ('demo_repo/metrics_engine.py:34: ZeroDivisionError', DANGER_RED),
            ('', TEXT_WHITE),
            ('=========================== 2 failed, 1 passed in 0.08s ========================', DANGER_RED),
            ('❌ Seeded failure confirmed. Launching SentinelAgent autonomous repair...', WARN_YELLOW)
        ]
        
        y_cursor = 310
        visible_count = int(len(lines) * progress)
        for i in range(min(visible_count, len(lines))):
            text, color = lines[i]
            draw.text((140, y_cursor), text, font=FONT_CODE, fill=color)
            y_cursor += 34

    elif scene_type == "agent_heal":
        draw_header(draw, "3. Autonomous Healing & Self-Reflection", "SentinelAgent explores AST, formulates candidate repair, and verifies in sandbox")
        draw_window(draw, 100, 240, WIDTH - 200, 720, "terminal — python3 app/main.py")
        
        lines = [
            ('$ python3 app/main.py', ACCENT_CYAN),
            ('######################################################################', TEXT_MUTED),
            ('      🚀 SENTINEL AGENT: AUTONOMOUS SRE & AUTO-HEALING ENGINE', ACCENT_CYAN),
            ('      OmniRush Frontier Buildathon 2026 Submission', TEXT_WHITE),
            ('######################################################################', TEXT_MUTED),
            ('🚨 [SENTINEL AGENT] INCOMING INCIDENT WEBHOOK DETECTED', DANGER_RED),
            ('🔍 [DISCOVERY] Indexed repository files: [\'metrics_engine.py\', \'test_metrics_engine.py\']', ACCENT_CYAN),
            ('🧪 [VERIFICATION] Running initial test suite with pytest...', TEXT_WHITE),
            ('❌ Initial test failed as expected (Exit code 1). Initiating healing loop...', DANGER_RED),
            ('', TEXT_WHITE),
            ('🔄 --- [ITERATION 1/3] FORMULATING REMEDIATION ---', WARN_YELLOW),
            ('💡 [HYPOTHESIS]: (1) ZeroDivisionError on empty transactions batch (count=0).', TEXT_WHITE),
            ('                (2) TypeError when amount is None or missing from item dict.', TEXT_WHITE),
            ('🛠️ [ACTION]: Applying synthesized patch to demo_repo/metrics_engine.py...', ACCENT_CYAN),
            ('🧪 [SANDBOX]: Executing verification pytest demo_repo/test_metrics_engine.py...', TEXT_WHITE),
            ('   ======================== 3 passed in 0.04s ========================', SUCCESS_GREEN),
            ('✨ [SUCCESS] All unit & regression tests passed in Iteration 1!', SUCCESS_GREEN),
            ('', TEXT_WHITE),
            ('======================================================================', TEXT_MUTED),
            ('📋 [FINAL STATUS]: RESOLVED (0 errors remaining)', SUCCESS_GREEN),
            ('======================================================================', TEXT_MUTED),
        ]
        
        y_cursor = 300
        visible_count = int(len(lines) * progress)
        for i in range(min(visible_count, len(lines))):
            text, color = lines[i]
            draw.text((140, y_cursor), text, font=FONT_CODE_SM, fill=color)
            y_cursor += 30

    elif scene_type == "diff":
        draw_header(draw, "4. Generated Pull Request & Clean Unified Diff", "Emits verified code remediation with zero unnecessary side effects")
        draw_window(draw, 100, 240, WIDTH - 200, 720, "git diff demo_repo/metrics_engine.py")
        
        lines = [
            ('Title: fix(metrics): resolve ZeroDivisionError & TypeError in batch processor', ACCENT_CYAN),
            ('Branch: sentinel/fix-inc-2026-98124-alpha', TEXT_MUTED),
            ('Status: ✅ Tests Verified (3 passed, 0 failed)', SUCCESS_GREEN),
            ('', TEXT_WHITE),
            ('--- a/demo_repo/metrics_engine.py', TEXT_MUTED),
            ('+++ b/demo_repo/metrics_engine.py', TEXT_MUTED),
            ('@@ -28,9 +28,15 @@ def process_batch_transactions(batch):', ACCENT_CYAN),
            ('     total_amount = 0.0', TEXT_WHITE),
            ('     valid_count = 0', TEXT_WHITE),
            (' ', TEXT_WHITE),
            ('     for tx in batch:', TEXT_WHITE),
            ('-        total_amount += tx["amount"] * tx.get("rate", 1.0)', DANGER_RED),
            ('-        valid_count += 1', DANGER_RED),
            ('+        amount = tx.get("amount")', SUCCESS_GREEN),
            ('+        if amount is None or not isinstance(amount, (int, float)):', SUCCESS_GREEN),
            ('+            continue', SUCCESS_GREEN),
            ('+        rate = tx.get("rate", 1.0)', SUCCESS_GREEN),
            ('+        total_amount += amount * rate', SUCCESS_GREEN),
            ('+        valid_count += 1', SUCCESS_GREEN),
            (' ', TEXT_WHITE),
            ('-    average = total_amount / valid_count', DANGER_RED),
            ('+    if valid_count == 0:', SUCCESS_GREEN),
            ('+        return {"total": 0.0, "average": 0.0, "count": 0}', SUCCESS_GREEN),
            ('+    average = total_amount / valid_count', SUCCESS_GREEN),
            ('     return {"total": total_amount, "average": average, "count": valid_count}', TEXT_WHITE),
        ]
        
        y_cursor = 300
        visible_count = int(len(lines) * progress)
        for i in range(min(visible_count, len(lines))):
            text, color = lines[i]
            draw.text((140, y_cursor), text, font=FONT_CODE_SM, fill=color)
            y_cursor += 28

    elif scene_type == "summary":
        draw_header(draw, "5. Project Specifications & Portability", "Judge Rebuild Checklist 8/8 fulfilled with dual execution architecture")
        
        # Left card: Checklist
        draw.rounded_rectangle([100, 240, 920, 960], radius=16, fill=TERM_BG, outline=CARD_BORDER, width=2)
        draw.text((140, 280), "📋 8/8 Judge Rebuild Checklist", font=FONT_CODE_TITLE, fill=ACCENT_CYAN)
        
        checks = [
            "✓ A git repository with commits",
            "✓ A dependency lockfile (requirements.txt)",
            "✓ The runtime version pinned (.python-version 3.11)",
            "✓ A Dockerfile that builds and runs offline",
            "✓ One single test command (make test / pytest)",
            "✓ A README with setup, run and test steps",
            "✓ Settings in .env.example, no secrets in files",
            "✓ No absolute paths from this machine"
        ]
        cy = 360
        for c in checks:
            draw.text((140, cy), c, font=FONT_CODE, fill=SUCCESS_GREEN)
            cy += 65

        # Right card: Key Highlights
        draw.rounded_rectangle([1000, 240, 1820, 960], radius=16, fill=TERM_BG, outline=CARD_BORDER, width=2)
        draw.text((1040, 280), "⚡ System Highlights", font=FONT_CODE_TITLE, fill=ACCENT_CYAN)
        
        highlights = [
            ("Dual Execution Engine", "Deterministic Heuristic for judges + LLM GPT-4o"),
            ("Bounded Sandbox", "Safe local process isolation and directory escape bounds"),
            ("Deterministic Convergence", "100% test pass rate in under 180 milliseconds"),
            ("Interactive Web Dashboard", "Live simulator on GitHub Pages with visual state machine"),
            ("Public GitHub Repository", "github.com/sundeep8967/sentinel-agent"),
            ("Live Demonstration Link", "sundeep8967.github.io/sentinel-agent")
        ]
        cy = 360
        for title, desc in highlights:
            draw.text((1040, cy), "• " + title, font=FONT_CODE, fill=TEXT_WHITE)
            draw.text((1070, cy + 32), desc, font=FONT_CODE_SM, fill=ACCENT_BLUE)
            cy += 90

    elif scene_type == "outro":
        draw_header(draw, None)
        cx, cy = WIDTH // 2, HEIGHT // 2
        draw.rounded_rectangle([cx - 550, cy - 250, cx + 550, cy + 250], radius=20, fill=TERM_BG, outline=SUCCESS_GREEN, width=2)
        
        draw.text((cx - 480, cy - 190), "SentinelAgent", font=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 80), fill=ACCENT_CYAN)
        draw.text((cx - 480, cy - 90), "Autonomous SRE Incident Remediation Complete", font=FONT_HERO, fill=TEXT_WHITE)
        
        draw.text((cx - 480, cy + 10), "GitHub Repo:   https://github.com/sundeep8967/sentinel-agent", font=FONT_CODE, fill=ACCENT_CYAN)
        draw.text((cx - 480, cy + 60), "Live Demo:     https://sundeep8967.github.io/sentinel-agent/", font=FONT_CODE, fill=SUCCESS_GREEN)
        draw.text((cx - 480, cy + 110), "Buildathon ID: OFB-BXREU9  •  Track: Agents & Automation", font=FONT_CODE, fill=TEXT_WHITE)
        draw.text((cx - 480, cy + 160), "Developer:     K J Sundeep Kumar (@sundeep8967)", font=FONT_CODE, fill=WARN_YELLOW)

    return img

def main():
    output_file = "sentinel_agent_demo.mp4"
    print("🎬 Rendering SentinelAgent 1080p demonstration video to:", output_file)
    
    # Launch ffmpeg pipe
    cmd = [
        "/usr/local/bin/ffmpeg", "-y",
        "-f", "image2pipe",
        "-vcodec", "png",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-movflags", "+faststart",
        output_file
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    # Timeline schedule (scene, duration in seconds)
    schedule = [
        ("intro", 3.5),
        ("incident", 5.0),
        ("test_fail", 6.0),
        ("agent_heal", 9.0),
        ("diff", 6.5),
        ("summary", 6.0),
        ("outro", 4.0),
    ]
    
    total_frames = sum(int(dur * FPS) for _, dur in schedule)
    current_frame = 0
    
    for scene, dur in schedule:
        num_frames = int(dur * FPS)
        for f in range(num_frames):
            prog = (f + 1) / (num_frames * 0.7) # reach 1.0 early so viewer can read
            if prog > 1.0:
                prog = 1.0
            frame = create_frame(scene, prog)
            frame.save(proc.stdin, "PNG")
            current_frame += 1
            if current_frame % 30 == 0:
                percent = (current_frame / total_frames) * 100
                print(f"  Rendering: {current_frame}/{total_frames} frames ({percent:.1f}%)")
                
    proc.stdin.close()
    proc.wait()
    print("✨ Video rendering complete! Video saved to:", output_file)

if __name__ == "__main__":
    main()
