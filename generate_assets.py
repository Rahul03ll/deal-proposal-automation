#!/usr/bin/env python3
"""
Generate crisp, publication-grade UI screenshots and animated GIF
demonstrating the working surface for the internship assignment writeup.
No node builders (Make/n8n) used; pure code editor, terminal, sheets, and mobile UI.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Helper to get standard default font or basic font
def get_font(size=14, bold=False):
    # Try system fonts on Windows
    font_paths = [
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibri.ttf",
        "C:\\Windows\\Fonts\\consola.ttf"
    ]
    if bold:
        font_paths = [
            "C:\\Windows\\Fonts\\segoeuib.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "C:\\Windows\\Fonts\\calibrib.ttf",
            "C:\\Windows\\Fonts\\consolab.ttf"
        ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def get_mono_font(size=13):
    mono_paths = [
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\lucon.ttf",
        "C:\\Windows\\Fonts\\cour.ttf"
    ]
    for path in mono_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def create_window_frame(width, height, title, bg_color="#1E1E1E", is_dark=True):
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Title bar
    title_bar_h = 36
    title_bar_bg = "#2D2D2D" if is_dark else "#E5E7EB"
    draw.rectangle([0, 0, width, title_bar_h], fill=title_bar_bg)
    
    # Window buttons
    draw.ellipse([14, 12, 24, 22], fill="#FF5F56")
    draw.ellipse([32, 12, 42, 22], fill="#FFBD2E")
    draw.ellipse([50, 12, 60, 22], fill="#27C93F")
    
    # Title text
    font_title = get_font(12, bold=True)
    text_color = "#D1D5DB" if is_dark else "#374151"
    draw.text((width // 2 - 80, 10), title, fill=text_color, font=font_title)
    
    return img, draw, title_bar_h


def generate_step1_sheet():
    width, height = 980, 480
    img, draw, top = create_window_frame(width, height, "Google Sheets — B2B Deal Intake & Discovery Tracker", "#FFFFFF", False)
    
    # Sheet Toolbar
    draw.rectangle([0, top, width, top + 34], fill="#F3F4F6")
    draw.line([0, top + 34, width, top + 34], fill="#E5E7EB")
    draw.text((20, top + 9), "File   Edit   View   Insert   Format   Data   Tools   Extensions   Help", fill="#4B5563", font=get_font(12))
    
    # Formula bar
    f_bar_y = top + 35
    draw.rectangle([0, f_bar_y, width, f_bar_y + 32], fill="#FFFFFF")
    draw.text((20, f_bar_y + 7), "fx | READY", fill="#111827", font=get_font(13, bold=True))
    draw.line([0, f_bar_y + 32, width, f_bar_y + 32], fill="#D1D5DB")
    
    # Table headers
    headers = [
        ("Deal ID", 75),
        ("Company", 170),
        ("Contact", 130),
        ("Region", 100),
        ("Budget", 80),
        ("Meeting Notes (Raw Discovery Call)", 310),
        ("Status", 110)
    ]
    
    start_y = f_bar_y + 33
    header_h = 28
    draw.rectangle([0, start_y, width, start_y + header_h], fill="#0F766E")
    
    curr_x = 0
    font_h = get_font(12, bold=True)
    for title, col_w in headers:
        draw.text((curr_x + 10, start_y + 6), title, fill="#FFFFFF", font=font_h)
        draw.line([curr_x + col_w, start_y, curr_x + col_w, height], fill="#E5E7EB")
        curr_x += col_w
        
    rows = [
        ("DEAL-401", "Al-Noor Financial Tech", "Tariq Al-Mansoor", "MENA (UAE)", "$45,000", "140 staff. Current KYC onboarding takes 48h manual. Target: 15m OCR + PostgreSQL API. 6wks.", "READY", "#DCFCE7", "#166534"),
        ("DEAL-402", "Apex Freight Solutions", "Sarah Jenkins", "North America", "$32,000", "185 staff. 800+ carrier emails daily. Wants 1-click email triage bot + TMS sync. 4wks.", "READY", "#DCFCE7", "#166534"),
        ("DEAL-403", "Meridian Health Systems", "Dr. Ronald Vance", "North America", "$55,000", "240 staff. Automated doctor shift fill phone tree to SMS engine. Board review Thurs.", "DRAFT", "#FEF3C7", "#92400E"),
        ("DEAL-404", "Gulf Logistics Co.", "Omar Bin-Zayed", "MENA (Saudi)", "$38,000", "Custom customs clearance invoice matching with SAP. Awaiting call notes.", "PENDING", "#F3F4F6", "#6B7280"),
    ]
    
    row_y = start_y + header_h
    row_h = 60
    font_cell = get_font(11)
    font_cell_bold = get_font(11, bold=True)
    
    for row in rows:
        draw.rectangle([0, row_y, width, row_y + row_h], fill="#FFFFFF" if rows.index(row)%2==0 else "#F9FAFB")
        draw.line([0, row_y + row_h, width, row_y + row_h], fill="#E5E7EB")
        
        curr_x = 0
        for i, (title, col_w) in enumerate(headers):
            val = row[i]
            if i == 6: # Status pill
                pill_bg = row[7]
                pill_fg = row[8]
                draw.rectangle([curr_x + 8, row_y + 18, curr_x + col_w - 12, row_y + 42], fill=pill_bg)
                draw.text((curr_x + 18, row_y + 23), val, fill=pill_fg, font=font_cell_bold)
            else:
                text_to_draw = val if len(val) < 48 else val[:45] + "..."
                draw.text((curr_x + 8, row_y + 22), text_to_draw, fill="#1F2937", font=font_cell)
            curr_x += col_w
            
        row_y += row_h
        
    out_path = os.path.join(ASSETS_DIR, "step1_deals_tracker_sheet.png")
    img.save(out_path)
    print(f"[+] Saved: {out_path}")


def generate_step2_rate_card_editor():
    width, height = 980, 520
    img, draw, top = create_window_frame(width, height, "Visual Studio Code — rate_card.json (Anti-Hallucination Guardrail)", "#1E1E1E", True)
    
    # Left sidebar
    draw.rectangle([0, top, 45, height], fill="#333333")
    draw.rectangle([45, top, 200, height], fill="#252526")
    draw.text((55, top + 15), "EXPLORER", fill="#858585", font=get_font(11, bold=True))
    draw.text((55, top + 38), "▾ DEAL_AUTOMATION", fill="#CCCCCC", font=get_font(11))
    draw.text((70, top + 60), "{} rate_card.json", fill="#4EC9B0", font=get_font(11))
    draw.text((70, top + 82), "py proposal_gen.py", fill="#CCCCCC", font=get_font(11))
    draw.text((70, top + 104), "📊 deals_tracker.csv", fill="#CCCCCC", font=get_font(11))
    
    # Editor tabs
    draw.rectangle([200, top, width, top + 32], fill="#2D2D2D")
    draw.rectangle([200, top, 340, top + 32], fill="#1E1E1E")
    draw.text((215, top + 9), "rate_card.json", fill="#FFFFFF", font=get_font(12))
    
    # Code body
    font_mono = get_mono_font(12)
    code_lines = [
        ('{\n', "#D4D4D4"),
        ('  "company_name": "VelocityOps AI Consulting",\n', "#9CDCFE"),
        ('  "founder": "Alex Mercer, Managing Partner",\n', "#9CDCFE"),
        ('  "standard_payment_terms": "40% deposit, 30% Phase 2 milestone, 30% sign-off.",\n', "#CE9178"),
        ('  "sla_support_period": "30 days post-deployment hypercare warranty included.",\n', "#CE9178"),
        ('  "guardrail_pricing_rules": {\n', "#4EC9B0"),
        ('    "min_deal_floor_usd": 15000,\n', "#B5CEA8"),
        ('    "max_concurrency_capacity": 4,\n', "#B5CEA8"),
        ('    "enforce_milestone_gating": true\n', "#569CD6"),
        ('  },\n', "#D4D4D4"),
        ('  "compliance_certifications": [\n', "#4EC9B0"),
        ('    "SOC 2 Type II Compliant System Architecture",\n', "#CE9178"),
        ('    "Regional Cloud Residency (AWS me-central-1 / us-east-1)",\n', "#CE9178"),
        ('    "Zero-Data-Retention Privacy Policy"\n', "#CE9178"),
        ('  ]\n', "#D4D4D4"),
        ('}\n', "#D4D4D4")
    ]
    
    y = top + 45
    line_no = 1
    for text, color in code_lines:
        draw.text((215, y), str(line_no).rjust(2), fill="#6E7681", font=font_mono)
        draw.text((250, y), text.strip(), fill=color, font=font_mono)
        y += 24
        line_no += 1
        
    out_path = os.path.join(ASSETS_DIR, "step2_rate_card_editor.png")
    img.save(out_path)
    print(f"[+] Saved: {out_path}")


def generate_step3_terminal():
    width, height = 980, 520
    img, draw, top = create_window_frame(width, height, "Terminal — PowerShell (python proposal_generator.py)", "#0C0C0C", True)
    
    font_mono = get_mono_font(12)
    font_bold = get_mono_font(12)
    
    lines = [
        ("PS C:\\Users\\KIIT\\deal_proposal_automation> python proposal_generator.py", "#CCCCCC"),
        ("=" * 72, "#4B5563"),
        ("  [>] VELOCITYOPS INSTANT PROPOSAL ENGINE (MCP ZERO-DELAY PIPELINE)", "#38BDF8"),
        ("=" * 72, "#4B5563"),
        ("[*] Loaded Rate Card & SLA Guardrails (VelocityOps AI Consulting)", "#A7F3D0"),
        ("[*] Found 2 deal(s) flagged 'READY' for immediate proposal generation.\n", "#FDE047"),
        ("[+] Processing Deal DEAL-401: Al-Noor Financial Technologies (Contact: Tariq Al-Mansoor)", "#FFFFFF"),
        ("   [OK] AI Extraction Complete (0.00s)", "#4ADE80"),
        ("   [OK] Generated Interactive SOW: DEAL-401_al-noor_financial_technologies_sow.html", "#38BDF8"),
        ("   [OK] Drafted Executive Follow-up Email: DEAL-401_al-noor_financial_technologies_email_draft.txt", "#38BDF8"),
        ("   [OK] Pushed Telegram 1-Click Approval Notification (DEAL-401)", "#C084FC"),
        ("   [OK] Cycle Finished in 0.00s (Total SLA target: < 180s)\n", "#4ADE80"),
        ("[+] Processing Deal DEAL-402: Apex Freight Solutions (Contact: Sarah Jenkins)", "#FFFFFF"),
        ("   [OK] AI Extraction Complete (0.00s)", "#4ADE80"),
        ("   [OK] Generated Interactive SOW: DEAL-402_apex_freight_solutions_sow.html", "#38BDF8"),
        ("   [OK] Drafted Executive Follow-up Email: DEAL-402_apex_freight_solutions_email_draft.txt", "#38BDF8"),
        ("   [OK] Pushed Telegram 1-Click Approval Notification (DEAL-402)", "#C084FC"),
        ("   [OK] Cycle Finished in 0.01s (Total SLA target: < 180s)\n", "#4ADE80"),
        ("=" * 72, "#4B5563"),
        ("[SUMMARY] Successfully compiled 2 proposal(s) in 0.01s.", "#22C55E"),
        ("Output Artifacts Directory: ...\\deal_proposal_automation\\generated_proposals", "#9CA3AF"),
        ("=" * 72, "#4B5563")
    ]
    
    y = top + 15
    for text, color in lines:
        draw.text((20, y), text, fill=color, font=font_mono)
        y += 18
        
    out_path = os.path.join(ASSETS_DIR, "step3_terminal_execution.png")
    img.save(out_path)
    print(f"[+] Saved: {out_path}")


def generate_step4_telegram():
    width, height = 480, 680
    img = Image.new("RGB", (width, height), "#0E1621") # Telegram Dark Blue/Grey
    draw = ImageDraw.Draw(img)
    
    # Telegram header
    draw.rectangle([0, 0, width, 60], fill="#17212B")
    draw.ellipse([15, 12, 50, 47], fill="#2481CC")
    draw.text((25, 20), "VO", fill="#FFFFFF", font=get_font(14, bold=True))
    draw.text((65, 15), "VelocityOps Deal Bot", fill="#F5F5F5", font=get_font(15, bold=True))
    draw.text((65, 36), "bot • executive instant alerts", fill="#7F8C99", font=get_font(11))
    
    # Chat card
    card_x1, card_y1, card_x2, card_y2 = 25, 85, width - 25, 490
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=12, fill="#182533")
    
    # Header inside card
    draw.text((card_x1 + 18, card_y1 + 18), "⚡ NEW SOW AWAITING APPROVAL", fill="#FFB74D", font=get_font(13, bold=True))
    draw.line([card_x1 + 18, card_y1 + 42, card_x2 - 18, card_y1 + 42], fill="#2B3A4C")
    
    details = [
        ("Deal ID:", "DEAL-401"),
        ("Client:", "Al-Noor Financial Tech"),
        ("Contact:", "Tariq Al-Mansoor (VP Ops)"),
        ("Region:", "MENA (Dubai / Riyadh)"),
        ("Total Value:", "$45,000 USD (Fixed Price)"),
        ("Timeline:", "6 Weeks (3 Phased Milestones)"),
        ("SOW Doc:", "DEAL-401_al-noor_sow.html"),
        ("Time Since Call:", "2 mins 14 secs")
    ]
    
    dy = card_y1 + 55
    for label, val in details:
        draw.text((card_x1 + 18, dy), label, fill="#7E8B9B", font=get_font(12))
        draw.text((card_x1 + 130, dy), val, fill="#E4ECF2", font=get_font(12, bold=True if "Value" in label or "Deal" in label else False))
        dy += 26
        
    # Excerpt box
    draw.rounded_rectangle([card_x1 + 18, dy + 6, card_x2 - 18, dy + 70], radius=6, fill="#0F1B26")
    draw.text((card_x1 + 26, dy + 12), "Executive Email Draft Preview:", fill="#64B5F6", font=get_font(11, bold=True))
    draw.text((card_x1 + 26, dy + 32), "\"Hi Tariq, great speaking with you earlier today regarding", fill="#B0BEC5", font=get_font(11))
    draw.text((card_x1 + 26, dy + 48), "Automated KYC & Onboarding Pipeline for Al-Noor...\"", fill="#B0BEC5", font=get_font(11))
    
    # Quick action buttons
    btn_y = card_y2 + 20
    # Button 1: Approve & Send
    draw.rounded_rectangle([card_x1, btn_y, card_x2, btn_y + 44], radius=8, fill="#2F6EA5")
    draw.text((card_x1 + 105, btn_y + 12), "✓ 1-TAP APPROVE & SEND EMAIL", fill="#FFFFFF", font=get_font(13, bold=True))
    
    # Button 2: View Document
    draw.rounded_rectangle([card_x1, btn_y + 54, card_x1 + 200, btn_y + 94], radius=8, fill="#232E3C")
    draw.text((card_x1 + 35, btn_y + 65), "📄 Preview SOW Doc", fill="#64B5F6", font=get_font(12, bold=True))
    
    # Button 3: Edit
    draw.rounded_rectangle([card_x1 + 215, btn_y + 54, card_x2, btn_y + 94], radius=8, fill="#232E3C")
    draw.text((card_x1 + 250, btn_y + 65), "✏ Adjust Terms", fill="#FFB74D", font=get_font(12, bold=True))
    
    out_path = os.path.join(ASSETS_DIR, "step4_telegram_mobile_card.png")
    img.save(out_path)
    print(f"[+] Saved: {out_path}")


def generate_final_result_sow():
    width, height = 980, 780
    img, draw, top = create_window_frame(width, height, "Browser — Scope of Work & Proposal | Al-Noor Financial Technologies", "#F8FAFC", False)
    
    # Browser URL bar
    draw.rectangle([0, top, width, top + 36], fill="#FFFFFF")
    draw.line([0, top + 36, width, top + 36], fill="#E2E8F0")
    draw.rounded_rectangle([80, top + 6, width - 80, top + 30], radius=12, fill="#F1F5F9")
    draw.text((95, top + 9), "🔒 https://client.velocityops.ai/proposals/DEAL-401-al-noor-sow", fill="#475569", font=get_font(11))
    
    # Inner Document container
    doc_x1, doc_y1, doc_x2, doc_y2 = 60, top + 50, width - 60, height - 20
    draw.rectangle([doc_x1, doc_y1, doc_x2, doc_y2], fill="#FFFFFF")
    draw.rectangle([doc_x1, doc_y1, doc_x2, doc_y2], outline="#CBD5E1", width=1)
    
    # Document Header
    draw.rectangle([doc_x1, doc_y1, doc_x2, doc_y1 + 130], fill="#0F172A")
    draw.text((doc_x1 + 30, doc_y1 + 20), "OFFICIAL SCOPE OF WORK & PROPOSAL", fill="#93C5FD", font=get_font(11, bold=True))
    draw.text((doc_x1 + 30, doc_y1 + 42), "Automated KYC & Onboarding Pipeline", fill="#FFFFFF", font=get_font(22, bold=True))
    draw.text((doc_x1 + 30, doc_y1 + 75), "Prepared exclusively for Al-Noor Financial Technologies", fill="#94A3B8", font=get_font(13))
    
    # Meta badges inside header
    draw.line([doc_x1 + 30, doc_y1 + 100, doc_x2 - 30, doc_y1 + 100], fill="#334155")
    draw.text((doc_x1 + 30, doc_y1 + 108), "CLIENT: Tariq Al-Mansoor", fill="#F8FAFC", font=get_font(11, bold=True))
    draw.text((doc_x1 + 250, doc_y1 + 108), "REGION: MENA (UAE)", fill="#F8FAFC", font=get_font(11, bold=True))
    draw.text((doc_x1 + 460, doc_y1 + 108), "INVESTMENT: $45,000 USD", fill="#38BDF8", font=get_font(11, bold=True))
    draw.text((doc_x1 + 680, doc_y1 + 108), "VALIDITY: 14 Days", fill="#94A3B8", font=get_font(11))
    
    # Section 1: Executive Diagnostic
    sy = doc_y1 + 150
    draw.text((doc_x1 + 30, sy), "1. Executive Diagnostic & Strategic Mandate", fill="#0F172A", font=get_font(14, bold=True))
    draw.rectangle([doc_x1 + 30, sy + 25, doc_x2 - 30, sy + 75], fill="#FEF2F2", outline="#F87171", width=1)
    draw.text((doc_x1 + 45, sy + 32), "Current Operational Pain Diagnosed:", fill="#991B1B", font=get_font(11, bold=True))
    draw.text((doc_x1 + 45, sy + 50), "140 staff across Dubai/Riyadh. 4 officers spend 48 hours manually reviewing trade licenses and PEP lists.", fill="#7F1D1D", font=get_font(11))
    
    draw.rectangle([doc_x1 + 30, sy + 85, doc_x2 - 30, sy + 135], fill="#F0FDF4", outline="#4ADE80", width=1)
    draw.text((doc_x1 + 45, sy + 92), "Target Production Architecture (Post-Deployment):", fill="#166534", font=get_font(11, bold=True))
    draw.text((doc_x1 + 45, sy + 110), "Turnaround reduced from 48 hours to 15 minutes with automated OCR, PEP screening, and PostgreSQL API sync.", fill="#14532D", font=get_font(11))
    
    # Section 2: Milestones
    my = sy + 150
    draw.text((doc_x1 + 30, my), "2. Phased Milestones & Acceptance Criteria", fill="#0F172A", font=get_font(14, bold=True))
    
    milestones = [
        ("Phase 1: Architecture, Security & Schema Spec", "Weeks 1 - 2", "$18,000 (40%)", "Specification document, AWS me-central-1 residency audit, API schema staging"),
        ("Phase 2: Core Document Pipeline & Sanction Engine", "Weeks 3 - 4", "$13,500 (30%)", "Automated OCR ingestion, sanction list screening, PostgreSQL core banking integration"),
        ("Phase 3: Production UAT, Pilot & Go-Live", "Weeks 5 - 6", "$13,500 (30%)", "Synthetic load testing, staff compliance training, 30 days hypercare warranty")
    ]
    
    card_y = my + 25
    for title, duration, fee, deliverables in milestones:
        draw.rounded_rectangle([doc_x1 + 30, card_y, doc_x2 - 30, card_y + 55], radius=6, fill="#F8FAFC", outline="#E2E8F0")
        draw.text((doc_x1 + 42, card_y + 10), title, fill="#0F172A", font=get_font(12, bold=True))
        draw.text((doc_x1 + 450, card_y + 10), duration, fill="#64748B", font=get_font(11))
        draw.text((doc_x2 - 140, card_y + 8), fee, fill="#2563EB", font=get_font(12, bold=True))
        draw.text((doc_x1 + 42, card_y + 30), f"Deliverables: {deliverables}", fill="#475569", font=get_font(10))
        card_y += 62
        
    # Investment & Signatures
    iy = card_y + 10
    draw.rounded_rectangle([doc_x1 + 30, iy, doc_x2 - 30, iy + 65], radius=8, fill="#EFF6FF", outline="#BFDBFE")
    draw.text((doc_x1 + 45, iy + 14), "TOTAL CONTRACT VALUE: $45,000 USD (Guaranteed Fixed Price)", fill="#1E40AF", font=get_font(13, bold=True))
    draw.text((doc_x1 + 45, iy + 36), "Terms: 40% upfront deposit on contract signature, 30% milestone delivery, 30% final sign-off.", fill="#3B82F6", font=get_font(11))
    
    # Signature boxes
    sig_y = iy + 80
    draw.rounded_rectangle([doc_x1 + 30, sig_y, doc_x1 + 400, sig_y + 70], radius=6, fill="#FFFFFF", outline="#E2E8F0")
    draw.line([doc_x1 + 45, sig_y + 45, doc_x1 + 380, sig_y + 45], fill="#CBD5E1")
    draw.text((doc_x1 + 45, sig_y + 50), "Authorized Signatory — Tariq Al-Mansoor (Al-Noor)", fill="#64748B", font=get_font(10))
    
    draw.rounded_rectangle([doc_x2 - 400, sig_y, doc_x2 - 30, sig_y + 70], radius=6, fill="#FFFFFF", outline="#E2E8F0")
    draw.line([doc_x2 - 385, sig_y + 45, doc_x2 - 50, sig_y + 45], fill="#CBD5E1")
    draw.text((doc_x2 - 385, sig_y + 50), "Authorized Signatory — Alex Mercer (VelocityOps)", fill="#64748B", font=get_font(10))
    
    out_path = os.path.join(ASSETS_DIR, "final_result_sow_document.png")
    img.save(out_path)
    print(f"[+] Saved: {out_path}")


def generate_animated_gif():
    # Load frames
    f1 = Image.open(os.path.join(ASSETS_DIR, "step1_deals_tracker_sheet.png")).resize((800, 480))
    f2 = Image.open(os.path.join(ASSETS_DIR, "step2_rate_card_editor.png")).resize((800, 480))
    f3 = Image.open(os.path.join(ASSETS_DIR, "step3_terminal_execution.png")).resize((800, 480))
    f4 = Image.open(os.path.join(ASSETS_DIR, "final_result_sow_document.png")).resize((800, 480))
    
    # Create Telegram centered frame
    f5_raw = Image.open(os.path.join(ASSETS_DIR, "step4_telegram_mobile_card.png"))
    f5 = Image.new("RGB", (800, 480), "#0E1621")
    f5_scaled = f5_raw.resize((340, 480))
    f5.paste(f5_scaled, (230, 0))
    
    frames = [f1, f2, f3, f4, f5]
    durations = [2200, 1800, 2500, 3000, 2500] # Milliseconds per slide
    
    gif_path = os.path.join(ASSETS_DIR, "workflow_demo.gif")
    f1.save(
        gif_path,
        save_all=True,
        append_images=[f2, f3, f4, f5],
        duration=durations,
        loop=0
    )
    print(f"[+] Saved Animated GIF: {gif_path}")


if __name__ == "__main__":
    print("[*] Generating Publication Assets...")
    generate_step1_sheet()
    generate_step2_rate_card_editor()
    generate_step3_terminal()
    generate_step4_telegram()
    generate_final_result_sow()
    generate_animated_gif()
    print("[✓] All assets generated successfully!")
