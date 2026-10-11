import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding for a cell in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                       f'<w:top w:w="{top}" w:type="dxa"/>'
                       f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                       f'<w:left w:w="{left}" w:type="dxa"/>'
                       f'<w:right w:w="{right}" w:type="dxa"/>'
                       f'</w:tcMar>')
    tc_pr.append(tc_mar)

def set_table_borders(table, color="D0D5DD", sz="4", val="single"):
    """Sets thin subtle borders on a table."""
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:left w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideV w:val="none"/>'
                        f'</w:tblBorders>')
    tbl_pr.append(borders)

def add_callout(doc, text, title="KEY PRINCIPLE", fill_hex="F1F1FE", border_hex="5F5FE1"):
    """Adds a stylish callout box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=160, bottom=160, left=240, right=200)
    
    # Left border only
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = parse_xml(f'<w:tcBorders {nsdecls("w")}>'
                           f'<w:top w:val="none"/>'
                           f'<w:bottom w:val="none"/>'
                           f'<w:left w:val="single" w:sz="24" w:color="{border_hex}"/>'
                           f'<w:right w:val="none"/>'
                           f'</w:tcBorders>')
    tc_pr.append(tc_borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"📌 {title}: ")
    run_t.font.bold = True
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(95, 95, 225)
    
    run_b = p.add_run(text)
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(29, 41, 57)
    
    # Add small spacing after callout
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def build_proposal():
    doc = docx.Document()
    
    # Page Margins: 0.8 in
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        section.header_distance = Inches(0.4)
        section.footer_distance = Inches(0.4)
        
        # Header & Footer setup
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("Zedu Design Proposal • Channel Details Files Tab • Team Vader")
        f_run.font.name = "Plus Jakarta Sans"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(152, 162, 179)
    
    # Set base font
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Plus Jakarta Sans'
    font.size = Pt(10)
    font.color.rgb = RGBColor(52, 64, 84) # #344054
    
    # --- COVER / HEADER BANNER TABLE ---
    banner_tbl = doc.add_table(rows=1, cols=1)
    banner_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    banner_cell = banner_tbl.cell(0, 0)
    banner_cell.width = Inches(6.8)
    set_cell_background(banner_cell, "1A1836") # Deep Indigo
    set_cell_margins(banner_cell, top=360, bottom=360, left=360, right=360)
    
    b_p1 = banner_cell.paragraphs[0]
    b_p1.paragraph_format.space_before = Pt(0)
    b_p1.paragraph_format.space_after = Pt(4)
    r_tag = b_p1.add_run("ZEDU CORE PLATFORM • DESIGN SPECIFICATION & RFC")
    r_tag.font.size = Pt(9)
    r_tag.font.bold = True
    r_tag.font.color.rgb = RGBColor(165, 165, 255)
    
    b_p2 = banner_cell.add_paragraph()
    b_p2.paragraph_format.space_before = Pt(4)
    b_p2.paragraph_format.space_after = Pt(6)
    r_title = b_p2.add_run("Channel Details Dialog:\nFiles Tab Redesign & Document Workflow")
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(255, 255, 255)
    
    b_p3 = banner_cell.add_paragraph()
    b_p3.paragraph_format.space_before = Pt(2)
    b_p3.paragraph_format.space_after = Pt(0)
    r_sub = b_p3.add_run("A Slack-Grade Architecture Featuring Dual View Modes (Hybrid vs. Pure List), Direct Actions, Non-Intrusive File Cues, and Desktop-Scale Document Inspection.")
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(228, 231, 236)
    
    # Metadata Info Block
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(12)
    p_space.paragraph_format.space_after = Pt(4)
    
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_tbl, color="E4E7EC", sz="4")
    
    metadata = [
        ("Author / Designer", "Fabian Muoghalu (@Fabbenco)"),
        ("Engineering Team", "Team Vader (Frontend Core)"),
        ("Target Surface", "Zedu Channel Details Dialog (`#channel-details-modal` → `Files Tab`)"),
        ("Status & Version", "Approved Design Proposal • Version 2.2 • October 2026")
    ]
    
    for row_idx, (k, v) in enumerate(metadata):
        c0 = meta_tbl.cell(row_idx, 0)
        c1 = meta_tbl.cell(row_idx, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.6)
        set_cell_background(c0, "F8F9FA" if row_idx % 2 == 0 else "FFFFFF")
        set_cell_background(c1, "F8F9FA" if row_idx % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, top=100, bottom=100, left=140, right=140)
        set_cell_margins(c1, top=100, bottom=100, left=140, right=140)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(71, 84, 103)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(29, 41, 57)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    # ==========================================
    # 1. EXECUTIVE SUMMARY
    # ==========================================
    h1 = doc.add_heading(level=1)
    r = h1.add_run("1. Executive Summary")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(26, 24, 54)
    
    p = doc.add_paragraph()
    p.add_run(
        "Files shared across high-velocity communication channels represent critical project artifacts: design guides, "
        "specifications, meeting recordings, code walk-throughs, sprint assets, and audio summaries. In large teams "
        "(such as Zedu channels exceeding 2,000 members), finding, previewing, and acting on files is a foundational "
        "daily routine."
    )
    p = doc.add_paragraph()
    p.add_run(
        "The current production implementation of the Files tab suffers from severe usability and visual limitations: "
        "files are dumped into an undemarcated single stream, hovering over items triggers cramped popups that obstruct "
        "the screen, primary actions like downloading or sharing require circuitous clicks, and inspecting multi-page "
        "documents opens a tiny, cramped modal dialog where text is illegible."
    )
    p = doc.add_paragraph()
    p.add_run(
        "This design proposal establishes a comprehensive, Slack-grade redesign of the Files tab within the existing "
        "channel details bounds (600px × 600px), paired with a wide desktop-grade document preview experience. "
        "Key architectural achievements include:\n"
    )
    
    points = [
        ("Sub-Category Demarcation:", " Immediate filtering via All, Documents (first right after All), Images, Videos, and Audio pills."),
        ("Dual View Mode System:", " Providing users with a Hybrid view (square media gallery on top + documents below) and a Pure List view (every item presented as a uniform list row)."),
        ("Subtle Micro-Interaction Cues:", " Replacing invasive hover previews with clean, contextual 'Open file ↗' and 'Play video ↗' cues."),
        ("Direct Action Suite:", " Exposing immediate Download, Share, and Open in Browser action buttons directly on document cards."),
        ("Wide Multi-Page Document Preview:", " Expanding the document modal to 1024px with thumbnail page navigation, zoom, fit, print, and instant sharing controls.")
    ]
    for bold_txt, norm_txt in points:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        rb = bp.add_run(bold_txt)
        rb.font.bold = True
        rb.font.color.rgb = RGBColor(95, 95, 225)
        rn = bp.add_run(norm_txt)
        rn.font.color.rgb = RGBColor(52, 64, 84)
        
    add_callout(
        doc,
        "The redesign preserves the established channel details modal dimension (600px × 600px) and navigation tabs "
        "(About, People 303, Agents, Files 24), elevating information density, aesthetics, and user productivity "
        "without disrupting user muscle memory.",
        title="ZERO-REGRESSION DESIGN OBJECTIVE"
    )

    # ==========================================
    # 2. PROBLEM STATEMENT & AUDIT
    # ==========================================
    h1 = doc.add_heading(level=1)
    r = h1.add_run("2. Problem Statement & Production UX Audit")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(26, 24, 54)
    
    p = doc.add_paragraph()
    p.add_run(
        "A rigorous heuristic evaluation of the current production channel details dialog revealed five critical "
        "UX defects that hinder team collaboration and asset discovery:"
    )
    
    defects = [
        ("Defect 1: Undemarcated Clutter & Media Pollution",
         "In the current Files tab, all file types are grouped together without category isolation. When members upload "
         "numerous screenshots or video clips, important text specifications, PDF guidelines, and contracts are pushed far "
         "down the list, forcing users into tedious continuous scrolling."),
        ("Defect 2: Invasive & Broken Hover Preview Popups",
         "Attempting to preview a file in the existing interface renders a 350px-400px floating tooltip directly over the "
         "list cursor. This popup obscures adjacent files, triggers accidental dismissed clicks, and cannot render documents "
         "legibly, causing friction and frustration."),
        ("Defect 3: Missing Direct Actions on Document Cards",
         "Users cannot perform essential document tasks—such as downloading a PDF, sharing an internal asset link, or opening "
         "a document in a dedicated browser tab—directly from the card row. Users are forced to open the file first, perform "
         "extra clicks, and navigate away from context."),
        ("Defect 4: Cramped, Narrow Document Preview Modal",
         "When a document (e.g., Ticket_Guide_Stage1.pdf) is opened, the current preview dialog renders in a constrained "
         "vertical box (~450px wide). Margins are crushed, headings are truncated, multi-page thumbnails are absent, and "
         "interns or contributors cannot read stage guides without extreme zooming and awkward horizontal panning."),
        ("Defect 5: Rigid Layout Without User Customization",
         "Power users reviewing legal documents or audit logs prefer high-density list scanning, whereas creative teams "
         "prefer visual image thumbnails. The current interface forces a single rigid layout without a clean toggle mechanism.")
    ]
    
    for d_title, d_desc in defects:
        dp = doc.add_paragraph()
        dp.paragraph_format.space_before = Pt(4)
        dp.paragraph_format.space_after = Pt(2)
        r_dt = dp.add_run(f"❌ {d_title}: ")
        r_dt.font.bold = True
        r_dt.font.color.rgb = RGBColor(180, 35, 24)
        r_dd = dp.add_run(d_desc)
        r_dd.font.color.rgb = RGBColor(71, 84, 103)

    # Embed Before Screenshots
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    p_img_title = doc.add_paragraph()
    r_it = p_img_title.add_run("Figure 1: Production State Analysis (Before Redesign)")
    r_it.font.bold = True
    r_it.font.size = Pt(10)
    r_it.font.color.rgb = RGBColor(52, 64, 84)

    img_tbl = doc.add_table(rows=1, cols=2)
    img_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_img0 = img_tbl.cell(0, 0)
    c_img1 = img_tbl.cell(0, 1)
    c_img0.width = Inches(3.2)
    c_img1.width = Inches(3.2)
    
    # Try inserting before screenshots if present
    before_p1 = "before_files_tab_current.png"
    before_p2 = "before_cramped_preview_modal.png"
    
    if os.path.exists(before_p1):
        p_c0 = c_img0.paragraphs[0]
        p_c0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c0.add_run().add_picture(before_p1, width=Inches(3.0))
        p_cap0 = c_img0.add_paragraph()
        p_cap0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap0 = p_cap0.add_run("A: Current Files Tab (Undemarcated, mixed stream)")
        r_cap0.font.size = Pt(8.5)
        r_cap0.font.italic = True
        
    if os.path.exists(before_p2):
        p_c1 = c_img1.paragraphs[0]
        p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c1.add_run().add_picture(before_p2, width=Inches(3.0))
        p_cap1 = c_img1.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap1 = p_cap1.add_run("B: Current Document Modal (Cramped ~450px width)")
        r_cap1.font.size = Pt(8.5)
        r_cap1.font.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==========================================
    # 3. PROPOSED ARCHITECTURE & FIVE CORE PILLARS
    # ==========================================
    h1 = doc.add_heading(level=1)
    r = h1.add_run("3. Proposed Design Architecture & Core Pillars")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(26, 24, 54)
    
    p = doc.add_paragraph()
    p.add_run(
        "To solve the identified defects while maintaining high performance and elegance, the redesign is structured "
        "around five foundational pillars:"
    )
    
    # Pillar 1
    h2 = doc.add_heading(level=2)
    r = h2.add_run("Pillar 1: Sub-Toolbar Hierarchy & Category Demarcation")
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(95, 95, 225)
    
    p = doc.add_paragraph()
    p.add_run(
        "Directly below the channel details navigation tabs, a dedicated sub-toolbar provides immediate search and "
        "type demarcation:\n"
        "• Instant Search: Real-time debounced query input with live count feedback.\n"
        "• Demarcated Category Pills: All (24) → Documents (10) [ordered first after All] → Images (8) → Videos (4) → Audio (2).\n"
        "• Strict Content Separation: Clicking 'Videos' isolates video files exclusively; clicking 'Images' displays images only; "
        "clicking 'Documents' shows docs only. The 'All' tab provides the unified overview."
    )
    
    # Pillar 2
    h2 = doc.add_heading(level=2)
    r = h2.add_run("Pillar 2: Dual View Mode System (Hybrid vs. Pure List)")
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(95, 95, 225)
    
    p = doc.add_paragraph()
    p.add_run(
        "Users can toggle between two purpose-built visualization modes using a segmented toggle button placed in the toolbar:\n"
    )
    
    v_modes = [
        ("Mode 1 (Hybrid Layout — Default):",
         "Employs an aspect-square (1:1) 4-column media grid at the top of each date section for rich visual assets "
         "(PNG, JPG, MP4 previews with timestamp pills), while documents (PDF, DOCX), Figma files, and audio notes are "
         "stacked in structured rows below. This achieves the optimal balance between visual browsing and textual detail."),
        ("Mode 2 (Pure List Layout):",
         "Converts all items—including images and video clips—into uniform row-by-row cards. Each row features a 36px icon "
         "with format badge (PNG, JPG, MP4, PDF), file name, inline open cue, file size pill, uploader avatar, upload timestamp, "
         "and action buttons. Perfect for audit logs, administrative reviews, and high-density scanning.")
    ]
    for vm_title, vm_desc in v_modes:
        vp = doc.add_paragraph(style='List Bullet')
        vp.paragraph_format.space_after = Pt(4)
        rvt = vp.add_run(vm_title)
        rvt.font.bold = True
        rvt.font.color.rgb = RGBColor(26, 24, 54)
        rvd = vp.add_run(f" {vm_desc}")
        rvd.font.color.rgb = RGBColor(71, 84, 103)
        
    # Pillar 3
    h2 = doc.add_heading(level=2)
    r = h2.add_run("Pillar 3: Non-Intrusive Micro-Interaction: Inline 'Open file ↗' Cue")
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(95, 95, 225)
    
    p = doc.add_paragraph()
    p.add_run(
        "The annoying floating hover thumbnail popup is permanently eliminated. In its place, card rows display a tiny, "
        "tasteful text cue: 'Open file ↗' (or 'Play video ↗' / 'Play audio ↗') rendered in primary brand indigo (#5F5FE1). "
        "On row hover, the cue subtly illuminates and underlines, giving users clear affordance that clicking opens the "
        "file without triggering visual obstruction."
    )
    
    # Pillar 4
    h2 = doc.add_heading(level=2)
    r = h2.add_run("Pillar 4: Direct Primary Document Action Buttons")
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(95, 95, 225)
    
    p = doc.add_paragraph()
    p.add_run(
        "Each document row features an integrated action cluster that appears on hover and remains fully keyboard-accessible:\n"
        "• Download: Instant file download with progress feedback.\n"
        "• Share: Copies channel file permalink to clipboard with toast notification.\n"
        "• Open in Browser: Opens document directly in a new browser tab for native viewing."
    )
    
    # Pillar 5
    h2 = doc.add_heading(level=2)
    r = h2.add_run("Pillar 5: Wide Multi-Page Document Preview Modal (Desktop-Scale)")
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(95, 95, 225)
    
    p = doc.add_paragraph()
    p.add_run(
        "To address the cramped document modal defect, clicking any document launches a high-fidelity, desktop-grade "
        "preview modal designed to professional standards:\n"
        "• Expansive Canvas: 1024px maximum width (up to 90vw) and 88vh height, centered over a frosted glass backdrop.\n"
        "• Interactive Page Rail (140px): Interactive vertical thumbnail sidebar displaying page previews (Page 1, 2, 3, 4) "
        "with active page highlights.\n"
        "• Dedicated PDF Control Toolbar: Displays current page counter ('Page 1 / 4'), Zoom Out (−), 100% scale indicator, "
        "Zoom In (+), Fit to Width (⛶), Rotate Clockwise (↻), and Print (🖶).\n"
        "• Full Top Header Suite: Displays document title, file size, uploader metadata tag, and quick Download, Share, "
        "Open in Browser, and Close (✕) action pills."
    )
    
    # Embed Redesign Screenshots
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    p_img_title2 = doc.add_paragraph()
    r_it2 = p_img_title2.add_run("Figure 2: Redesigned Interface & High-Fidelity Prototypes")
    r_it2.font.bold = True
    r_it2.font.size = Pt(10)
    r_it2.font.color.rgb = RGBColor(52, 64, 84)

    img_tbl2 = doc.add_table(rows=1, cols=2)
    img_tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
    c2_0 = img_tbl2.cell(0, 0)
    c2_1 = img_tbl2.cell(0, 1)
    c2_0.width = Inches(3.2)
    c2_1.width = Inches(3.2)
    
    after_p1 = "04_full_modal_redesign_screenshot.png"
    after_p2 = "04_full_modal_list_view.png"
    
    if os.path.exists(after_p1):
        p_c20 = c2_0.paragraphs[0]
        p_c20.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c20.add_run().add_picture(after_p1, width=Inches(3.0))
        p_cap20 = c2_0.add_paragraph()
        p_cap20.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap20 = p_cap20.add_run("A: Hybrid View Mode (Square media grid + Doc rows)")
        r_cap20.font.size = Pt(8.5)
        r_cap20.font.italic = True
        
    if os.path.exists(after_p2):
        p_c21 = c2_1.paragraphs[0]
        p_c21.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c21.add_run().add_picture(after_p2, width=Inches(3.0))
        p_cap21 = c2_1.add_paragraph()
        p_cap21.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap21 = p_cap21.add_run("B: Pure List View Mode (Every file listed row-by-row)")
        r_cap21.font.size = Pt(8.5)
        r_cap21.font.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==========================================
    # 4. BEFORE VS. AFTER COMPARISON MATRIX
    # ==========================================
    h1 = doc.add_heading(level=1)
    r = h1.add_run("4. Before vs. After Detailed Comparison Matrix")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(26, 24, 54)
    
    matrix_data = [
        ("UX Dimension", "Current Production State (Before)", "Redesigned Implementation (After)"),
        ("Category Organization", "All files dumped into a single unsorted feed. No sub-tabs.", "Demarcated pills: All (24), Documents (10) first, Images (8), Videos (4), Audio (2)."),
        ("Layout Modes", "Single fixed layout; no user toggle or personalization.", "Segmented Dual Toggle: Hybrid Mode (Media grid + Doc list) and Pure List Mode."),
        ("File Interaction / Preview", "Intrusive 400px hover popup that obstructs the screen.", "Subtle, non-blocking inline 'Open file ↗' cue. Zero screen clutter."),
        ("Document Actions", "No actions on file row. Requires opening the file first.", "Direct Download, Share link, and Open in Browser buttons directly on row hover."),
        ("Document Preview Width", "Cramped vertical dialog (~450px wide). Margins clipped.", "Expansive 1024px multi-page modal with thumbnail page sidebar and PDF tools."),
        ("Multi-Page PDF Support", "Single unpaged vertical scroll without thumbnails.", "Dedicated 140px interactive thumbnail sidebar with active page indicators."),
        ("Video & Media Treatment", "Small inline thumbnails mixed with text files.", "Rich 1:1 aspect ratio square media grid with play buttons and timestamp tags in Hybrid mode."),
        ("State Handling", "Basic loading indicator. Missing empty/error states.", "Fully styled Loading Skeletons, Empty Channel State, Zero-Match Search, and Retry State.")
    ]
    
    comp_tbl = doc.add_table(rows=len(matrix_data), cols=3)
    comp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(comp_tbl, color="D0D5DD", sz="4")
    
    col_widths = [Inches(1.8), Inches(2.5), Inches(2.5)]
    
    for row_idx, row in enumerate(matrix_data):
        for col_idx, val in enumerate(row):
            cell = comp_tbl.cell(row_idx, col_idx)
            cell.width = col_widths[col_idx]
            set_cell_margins(cell, top=110, bottom=110, left=130, right=130)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            
            if row_idx == 0:
                set_cell_background(cell, "1A1836")
                r = p.add_run(val)
                r.font.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                set_cell_background(cell, "F9FAFB" if row_idx % 2 == 1 else "FFFFFF")
                r = p.add_run(val)
                r.font.size = Pt(9)
                if col_idx == 0:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(52, 64, 84)
                elif col_idx == 1:
                    r.font.color.rgb = RGBColor(180, 35, 24) # Negative red tint
                else:
                    r.font.color.rgb = RGBColor(2, 122, 72) # Positive green tint

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # ==========================================
    # 5. STATE MANAGEMENT & EDGE CASES
    # ==========================================
    h1 = doc.add_heading(level=1)
    r = h1.add_run("5. State Management & Comprehensive Edge Cases")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(26, 24, 54)
    
    p = doc.add_paragraph()
    p.add_run(
        "To deliver a robust, production-ready implementation, all application states have been designed and validated:"
    )
    
    states = [
        ("1. Populated State (Default):", "Displays date-grouped file collections with full counters, media grid thumbnails, and metadata rows. Supports both Hybrid and List rendering."),
        ("2. Filtered States (Docs, Images, Videos, Audio):", "Instantly filters file list to single content type. Category counters reflect accurate item counts without layout shift."),
        ("3. Active Search State:", "Filters file results in real-time as user types into `#file-search-box`. Highlights matching file name strings."),
        ("4. Zero Search Results State:", "Renders an illustrative 'No files found' state with a friendly search icon and a 'Clear Search' button that restores default view in 1 click."),
        ("5. Channel Empty State:", "When a newly created channel has no uploaded files, displays an inspiring empty state icon with 'Share the first file' call-to-action button."),
        ("6. Skeleton Loading State:", "When fetching files over high-latency connections, presents pulsing shimmer cards matching the exact dimensions of file cards and media squares to prevent Cumulative Layout Shift (CLS = 0.0)."),
        ("7. Error & Offline State:", "If network request fails, displays a non-blocking error badge with a 'Retry Sync' button.")
    ]
    
    for s_title, s_desc in states:
        sp = doc.add_paragraph(style='List Bullet')
        sp.paragraph_format.space_after = Pt(3)
        rst = sp.add_run(s_title)
        rst.font.bold = True
        rst.font.color.rgb = RGBColor(26, 24, 54)
        rsd = sp.add_run(f" {s_desc}")
        rsd.font.color.rgb = RGBColor(71, 84, 103)

    # ==========================================
    # 6. TECHNICAL IMPLEMENTATION ARCHITECTURE
    # ==========================================
    h1 = doc.add_heading(level=1)
    r = h1.add_run("6. Technical Implementation Blueprint (Zedu Frontend)")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(26, 24, 54)
    
    p = doc.add_paragraph()
    p.add_run(
        "The redesign directly integrates into the Zedu Next.js/React frontend codebase (`zedu-fe`). "
        "The component hierarchy and TypeScript data structures are specified below:"
    )
    
    add_callout(
        doc,
        "Components adhere strictly to existing Zedu patterns: Tailwind CSS utility tokens, Lucide-React icons, "
        "Radix UI dialog accessibility primitives, and zero external viewer bloat.",
        title="FRONTEND ARCHITECTURE PRINCIPLE"
    )
    
    p_code_header = doc.add_paragraph()
    p_code_header.paragraph_format.space_before = Pt(4)
    p_code_header.paragraph_format.space_after = Pt(2)
    r_ch = p_code_header.add_run("TypeScript Component Hierarchy & Data Model:")
    r_ch.font.bold = True
    r_ch.font.size = Pt(10)
    
    ts_code = (
        "// 1. Data Model Interface\n"
        "export type FileCategory = 'all' | 'documents' | 'images' | 'videos' | 'audio';\n"
        "export type LayoutMode = 'hybrid' | 'list';\n\n"
        "export interface ChannelFile {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  url: string;\n"
        "  sizeBytes: number;\n"
        "  formattedSize: string;\n"
        "  extension: 'pdf' | 'docx' | 'png' | 'jpg' | 'webp' | 'mp4' | 'm4a' | 'fig';\n"
        "  category: 'document' | 'image' | 'video' | 'audio';\n"
        "  uploadedAt: string; // ISO date\n"
        "  uploader: {\n"
        "    id: string;\n"
        "    username: string;\n"
        "    displayName: string;\n"
        "    avatarUrl?: string;\n"
        "  };\n"
        "  duration?: string; // For audio & video\n"
        "  pageCount?: number; // For PDF/DOC documents\n"
        "}\n\n"
        "// 2. Component File Organization\n"
        "components/channel-details/\n"
        "├── channel-details-modal.tsx          // Root modal (maintains 600px x 600px)\n"
        "└── files-tab/\n"
        "    ├── files-sub-toolbar.tsx         // Search bar, category pills, layout mode toggle\n"
        "    ├── files-tab-container.tsx       // Main date-grouped container & mode switcher\n"
        "    ├── file-card-row.tsx             // Document / list row card with direct actions\n"
        "    ├── media-grid-tile.tsx           // 1:1 square media thumbnail for Hybrid mode\n"
        "    └── wide-doc-preview-modal.tsx    // 1024px desktop-grade multi-page viewer\n"
    )
    
    tbl_code = doc.add_table(rows=1, cols=1)
    tbl_code.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_code = tbl_code.cell(0, 0)
    c_code.width = Inches(6.8)
    set_cell_background(c_code, "F8F9FA")
    set_cell_margins(c_code, top=140, bottom=140, left=180, right=180)
    
    p_c = c_code.paragraphs[0]
    p_c.paragraph_format.space_after = Pt(0)
    r_c = p_c.add_run(ts_code)
    r_c.font.name = "Consolas"
    r_c.font.size = Pt(8.5)
    r_c.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==========================================
    # 7. USER ACCEPTANCE CRITERIA (UAC)
    # ==========================================
    h1 = doc.add_heading(level=1)
    r = h1.add_run("7. User Acceptance Criteria (UAC)")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(26, 24, 54)
    
    uac_items = [
        ("UAC-1: Category Pill Demarcation", 
         "Sub-filter pills display in exact order: All, Documents (first right after All), Images, Videos, Audio. Clicking 'Videos' displays only videos; clicking 'Images' displays only images; clicking 'Documents' displays only documents; clicking 'All' shows all items."),
        ("UAC-2: Dual View Toggle", 
         "A segmented toggle allows switching between 'Hybrid' and 'List'. In Hybrid mode, images and videos render in square 1:1 grids at the top of each date section. In List mode, all items render row-by-row with individual format tags, metadata, and action buttons."),
        ("UAC-3: Elimination of Hover Popups", 
         "Hovering over file items displays a clean inline text cue ('Open file ↗' or 'Play video ↗'). No floating hover cards obstruct the screen."),
        ("UAC-4: Direct Document Action Buttons", 
         "Document rows render Download, Share, and Open in Browser action buttons on hover/focus. Clicking Download initiates instant download without extra dialogs. Clicking Share copies file permalink."),
        ("UAC-5: Wide Desktop-Grade Document Preview Modal", 
         "Clicking a document opens a 1024px wide modal (88vh max height) with a 140px thumbnail sidebar showing multi-page cards (Page 1, 2, 3, 4). Includes page counter, zoom controls, fit, rotate, print, download, and close (✕) actions."),
        ("UAC-6: Zero Layout Shift & Keyboard Accessibility", 
         "Modal supports full ESC key dismiss, Tab navigation, and WCAG AA contrast compliance (minimum 4.5:1 text contrast).")
    ]
    
    for uac_id, uac_desc in uac_items:
        up = doc.add_paragraph()
        up.paragraph_format.space_before = Pt(4)
        up.paragraph_format.space_after = Pt(2)
        r_ut = up.add_run(f"✅ {uac_id}: ")
        r_ut.font.bold = True
        r_ut.font.color.rgb = RGBColor(2, 122, 72)
        r_ud = up.add_run(uac_desc)
        r_ud.font.color.rgb = RGBColor(52, 64, 84)

    # ==========================================
    # 8. IMPLEMENTATION ROADMAP & SIGN-OFF
    # ==========================================
    h1 = doc.add_heading(level=1)
    r = h1.add_run("8. Implementation Roadmap & Sign-Off")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(26, 24, 54)
    
    roadmap_tbl = doc.add_table(rows=5, cols=4)
    roadmap_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(roadmap_tbl, color="D0D5DD", sz="4")
    
    rm_headers = ["Phase", "Milestone / Deliverable", "Target Owner", "Timeline"]
    rm_rows = [
        ("Phase 1", "Interactive Design Prototype & Spec Approval", "Fabian Muoghalu (@Fabbenco)", "Completed"),
        ("Phase 2", "Sub-Toolbar, Category Demarcation & Direct Actions", "Team Vader Frontend", "Sprint 2, Days 1-2"),
        ("Phase 3", "Dual View Toggle (Hybrid & Pure List modes)", "Team Vader Frontend", "Sprint 2, Days 3-4"),
        ("Phase 4", "Wide Multi-Page Document Preview Modal & QA Testing", "Team Vader & QA", "Sprint 2, Day 5")
    ]
    
    for col_idx, h in enumerate(rm_headers):
        cell = roadmap_tbl.cell(0, col_idx)
        set_cell_background(cell, "1A1836")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for row_idx, r_data in enumerate(rm_rows, start=1):
        for col_idx, val in enumerate(r_data):
            cell = roadmap_tbl.cell(row_idx, col_idx)
            set_cell_background(cell, "F9FAFB" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if col_idx == 0 or col_idx == 3:
                r.font.bold = True
            r.font.color.rgb = RGBColor(52, 64, 84)

    doc.add_paragraph().paragraph_format.space_after = Pt(20)
    
    # Sign-off footer block
    so_p = doc.add_paragraph()
    so_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    so_r = so_p.add_run("— End of Design Proposal Document —\nReady for Review & Frontend Implementation in Zedu Core")
    so_r.font.italic = True
    so_r.font.size = Pt(9.5)
    so_r.font.color.rgb = RGBColor(102, 112, 133)

    output_filename = "DESIGN_PROPOSAL_FILES_TAB.docx"
    doc.save(output_filename)
    print(f"Successfully generated {output_filename} ({os.path.getsize(output_filename)} bytes)")

if __name__ == "__main__":
    build_proposal()
