"""Readable script layout for a cut.json (shared by build_cut.py)."""
import re
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

INK = RGBColor(0x11, 0x11, 0x11)
CUE_INK = RGBColor(0x44, 0x44, 0x44)
TAG_INK = RGBColor(0x6B, 0x3F, 0xA0)
SOUND_INK = RGBColor(0xC2, 0x41, 0x0C)
GRAY = RGBColor(0x77, 0x77, 0x77)
SOUND_RE = re.compile(r"(SOUND[^:]*:[^'\]]*'[^']*'(?:[^'\].)]*'[^']*')*)")


def shade(p, fill):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
    pPr.append(shd)


def left_bar(p, color):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single"); left.set(qn("w:sz"), "18"); left.set(qn("w:space"), "6"); left.set(qn("w:color"), color)
    bdr.append(left)
    pPr.append(bdr)


def keep_next(p):
    p.paragraph_format.keep_with_next = True


def spacing(p, before=0, after=0, indent=0.0):
    f = p.paragraph_format
    f.space_before = Pt(before); f.space_after = Pt(after); f.line_spacing = 1.0
    if indent:
        f.left_indent = Inches(indent)


def strip(t):
    t = t.strip()
    return t[1:-1].strip() if t.startswith("[") and t.endswith("]") else t


def runs_with_sounds(p, text, size, color, italic=False):
    pos = 0
    for m in SOUND_RE.finditer(text):
        if m.start() > pos:
            r = p.add_run(text[pos:m.start()]); r.font.size = Pt(size); r.font.color.rgb = color; r.italic = italic
        r = p.add_run(m.group(1)); r.font.size = Pt(size); r.font.color.rgb = SOUND_INK; r.bold = True; r.italic = italic
        pos = m.end()
    if pos < len(text):
        r = p.add_run(text[pos:]); r.font.size = Pt(size); r.font.color.rgb = color; r.italic = italic


def page_number_footer(section, title):
    p = section.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title + "   ·   page "); r.font.size = Pt(8); r.font.color.rgb = GRAY
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        run = p.add_run(); run.font.size = Pt(8); run.font.color.rgb = GRAY
        if kind:
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), kind); run._r.append(fc)
        else:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt; run._r.append(it)


def render(cut, out, stats_line):
    d = Document()
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Inches(0.7)
    sec.top_margin = sec.bottom_margin = Inches(0.6)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    page_number_footer(sec, cut.get("title", "Cutting"))

    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; spacing(p, 0, 0)
    r = p.add_run(cut.get("title", "Cutting")); r.bold = True; r.font.size = Pt(18)
    if cut.get("author"):
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; spacing(p, 0, 2)
        r = p.add_run(cut["author"]); r.italic = True; r.font.size = Pt(10); r.font.color.rgb = GRAY
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; spacing(p, 0, 6)
    r = p.add_run(cut.get("subtitle") or stats_line); r.font.size = Pt(8.5); r.font.color.rgb = GRAY

    # legend
    p = d.add_paragraph(); spacing(p, 0, 8); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for txt, color, bold, italic, fill in (("▶ DO THIS", CUE_INK, True, False, True), ("   how to say it", TAG_INK, False, True, False),
                                           ("   SAY THIS", INK, True, False, False), ("   SOUND", SOUND_INK, True, False, False)):
        r = p.add_run(txt); r.font.size = Pt(9); r.font.color.rgb = color; r.bold = bold; r.italic = italic
        if fill:
            r.font.highlight_color = 16  # light gray

    scene_no = 0
    for s in cut["segments"]:
        k, t, tag = s["kind"], s["text"], s.get("tag", "")
        if k in ("scene", "head"):
            p = d.add_paragraph(); spacing(p, 10, 4); keep_next(p)
            if k == "scene":
                scene_no += 1
                label = f"{scene_no}.  {t.upper()}"
                shade(p, "1F2937")
            else:
                label = f"— {t.upper()} —"
                shade(p, "6B3FA0")
            r = p.add_run(label); r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        elif k == "cue":
            p = d.add_paragraph(); spacing(p, 2, 4); keep_next(p); shade(p, "F1F1F1"); left_bar(p, "9CA3AF")
            r = p.add_run("▶ "); r.font.size = Pt(9); r.font.color.rgb = CUE_INK; r.bold = True
            runs_with_sounds(p, strip(t), 9, CUE_INK)
        else:  # src / intro
            if tag:
                p = d.add_paragraph(); spacing(p, 2, 0, 0.25); keep_next(p)
                runs_with_sounds(p, strip(tag), 8.5, TAG_INK, italic=True)
            p = d.add_paragraph(); spacing(p, 0, 7, 0.25)
            if k == "intro":
                left_bar(p, "6B3FA0")
            r = p.add_run(t); r.font.size = Pt(11.5); r.font.color.rgb = INK

    if cut.get("backup_cuts"):
        p = d.add_paragraph(); spacing(p, 12, 3); shade(p, "FEF3C7")
        r = p.add_run("IF UR OVER TIME (cut these first, in order)"); r.bold = True; r.font.size = Pt(9.5)
        for t in cut["backup_cuts"]:
            p = d.add_paragraph(); spacing(p, 0, 1, 0.2); r = p.add_run(t); r.font.size = Pt(9)
        if cut.get("never_cut"):
            p = d.add_paragraph(); spacing(p, 4, 0, 0.2)
            r = p.add_run("Do NOT cut: "); r.bold = True; r.font.size = Pt(9)
            r = p.add_run(cut["never_cut"]); r.font.size = Pt(9)
    d.save(out)
