"""Simple, readable script layout for a cut.json (shared by build_cut.py).
Plain text, no boxes or bars:
  [blocking]            gray italic, own line
  [how to say it] line  gray italic tag, then the script line in black
  SOUND: 'click'        bold
  scene names           bold caps
"""
import re
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

BLACK = RGBColor(0x00, 0x00, 0x00)
GRAY = RGBColor(0x59, 0x59, 0x59)
SOUND_RE = re.compile(r"(SOUND[^:]*:[^'\]]*'[^']*'(?:[^'\].)]*'[^']*')*)")


def spacing(p, before=0, after=0):
    f = p.paragraph_format
    f.space_before = Pt(before); f.space_after = Pt(after); f.line_spacing = 1.05


def gray_text(p, text, size, bold_sounds=True):
    pos = 0
    for m in (SOUND_RE.finditer(text) if bold_sounds else []):
        if m.start() > pos:
            r = p.add_run(text[pos:m.start()]); r.italic = True; r.font.size = Pt(size); r.font.color.rgb = GRAY
        r = p.add_run(m.group(1)); r.italic = True; r.bold = True; r.font.size = Pt(size); r.font.color.rgb = BLACK
        pos = m.end()
    if pos < len(text):
        r = p.add_run(text[pos:]); r.italic = True; r.font.size = Pt(size); r.font.color.rgb = GRAY


def render(cut, out, stats_line):
    d = Document()
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Inches(0.8)
    sec.top_margin = sec.bottom_margin = Inches(0.7)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; spacing(p)
    r = p.add_run(cut.get("title", "Cutting")); r.bold = True; r.font.size = Pt(17)
    if cut.get("author"):
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; spacing(p)
        r = p.add_run(cut["author"]); r.italic = True; r.font.size = Pt(10)
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; spacing(p, 0, 10)
    r = p.add_run((cut.get("subtitle") or stats_line) + "   ·   [gray] = do it, dont say it   ·   black = say it")
    r.font.size = Pt(9); r.font.color.rgb = GRAY

    scene_no = 0
    for s in cut["segments"]:
        k, t, tag = s["kind"], s["text"], s.get("tag", "")
        if k == "scene":
            scene_no += 1
            p = d.add_paragraph(); spacing(p, 12, 4); p.paragraph_format.keep_with_next = True
            r = p.add_run(f"{scene_no}. {t.upper()}"); r.bold = True; r.font.size = Pt(11)
        elif k == "head":
            p = d.add_paragraph(); spacing(p, 12, 4); p.paragraph_format.keep_with_next = True
            r = p.add_run(t.upper()); r.bold = True; r.font.size = Pt(11)
        elif k == "cue":
            p = d.add_paragraph(); spacing(p, 2, 4); p.paragraph_format.keep_with_next = True
            gray_text(p, t, 10)
        else:
            p = d.add_paragraph(); spacing(p, 0, 6)
            if tag:
                gray_text(p, tag + " ", 10)
            r = p.add_run(t); r.font.size = Pt(12); r.font.color.rgb = BLACK

    if cut.get("backup_cuts"):
        p = d.add_paragraph(); spacing(p, 14, 3)
        r = p.add_run("IF UR OVER TIME (cut these first, in order)"); r.bold = True; r.font.size = Pt(10)
        for t in cut["backup_cuts"]:
            p = d.add_paragraph(); spacing(p, 0, 1); r = p.add_run(t); r.font.size = Pt(9.5)
        if cut.get("never_cut"):
            p = d.add_paragraph(); spacing(p, 4, 0)
            r = p.add_run("Do NOT cut: "); r.bold = True; r.font.size = Pt(9.5)
            r = p.add_run(cut["never_cut"]); r.font.size = Pt(9.5)
    d.save(out)
