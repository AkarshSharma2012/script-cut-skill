#!/usr/bin/env python3
"""Build and verify an interp cutting.

Usage:
  python build_cut.py extract SOURCE.pdf OUT.txt
  python build_cut.py check  SOURCE(.pdf|.txt) CUT.json [--wpm 149]
  python build_cut.py build  SOURCE(.pdf|.txt) CUT.json OUT.docx [--wpm 149]

CUT.json:
{
  "title": "Hamlet",
  "author": "William Shakespeare",
  "subtitle": "Around 9:30 mins",           (optional)
  "segments": [
    {"kind": "cue",   "text": "[stand center...]"},
    {"kind": "src",   "text": "exact line from the script", "tag": "[how to say it]"},
    {"kind": "head",  "text": "INTRO"},
    {"kind": "intro", "text": "student-written intro", "tag": "[how to say it]"}
  ],
  "backup_cuts": ["1. 'line' (~3 sec)", "..."],   (optional)
  "never_cut":   "the soliloquy, the final scene"   (optional)
}

kinds: src = exact words from the script (verified, spoken)
       intro = new words the student wrote (spoken, not verified)
       cue = blocking line (not spoken)
       head = section header (not spoken)
"""
import difflib, json, re, sys


def load_source(path):
    if path.lower().endswith(".pdf"):
        import pypdf
        r = pypdf.PdfReader(path)
        return "\n".join(p.extract_text() or "" for p in r.pages)
    return open(path, encoding="utf-8", errors="ignore").read()


def norm(t):
    t = t.lower()
    t = re.sub(r"\bpm\b", "im", t)   # common PDF glyph errors for I'm / I'd / I've
    t = re.sub(r"\bpd\b", "id", t)
    t = re.sub(r"\bpve\b", "ive", t)
    return re.sub(r"[^a-z]", "", t)


def coverage(excerpt, S):
    e = norm(excerpt)
    if not e:
        return 1.0, -1
    i = S.find(e)
    if i >= 0:
        return 1.0, i
    sm = difflib.SequenceMatcher(None, e, S, autojunk=False)
    m = sm.find_longest_match(0, len(e), 0, len(S))
    start = max(0, m.b - m.a - 20)
    win = S[start:start + len(e) + 40]
    cov = sum(b.size for b in difflib.SequenceMatcher(None, e, win, autojunk=False).get_matching_blocks()) / len(e)
    return cov, start


def words(t):
    return len(re.findall(r"[A-Za-z0-9']+", t))


def check(src_path, cut, wpm):
    S = norm(load_source(src_path))
    segs = cut["segments"]
    unverified, out_of_order, last = [], [], -1
    slack = min(200, len(S) // 50)   # tolerate small PDF jitter, scaled to source size
    for s in segs:
        if s["kind"] != "src":
            continue
        cov, pos = coverage(s["text"], S)
        if cov < 0.95:
            unverified.append({"coverage": round(cov, 3), "text": s["text"][:80]})
        elif len(norm(s["text"])) >= 40:          # short lines (numbers, "Why?") repeat too often to order-check
            if pos < last - slack:
                out_of_order.append(s["text"][:80])
            last = max(last, pos)
    spoken = sum(words(s["text"]) for s in segs if s["kind"] in ("src", "intro"))
    intro = sum(words(s["text"]) for s in segs if s["kind"] == "intro")
    res = {
        "spoken_words": spoken,
        "intro_words": intro,
        "script_words": spoken - intro,
        "wpm_used": wpm,
        "talking_minutes": round(spoken / wpm, 2),
        "est_with_pauses": f"{spoken / wpm + 0.75:.1f}-{spoken / wpm + 1.25:.1f} min (estimate, time a real run)",
        "unverified_lines": unverified,
        "possibly_out_of_order": out_of_order,
        "spoken_lines_missing_tag": [s["text"][:60] for s in segs if s["kind"] in ("src", "intro") and not s.get("tag")],
    }
    return res


def build(src_path, cut, out, wpm):
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    res = check(src_path, cut, wpm)
    d = Document()
    st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(cut.get("title", "Cutting")); r.bold = True; r.font.size = Pt(18)
    if cut.get("author"):
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(cut["author"]).italic = True
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(cut.get("subtitle") or f"{res['spoken_words']} spoken words. [brackets] = do this, dont say it.").font.size = Pt(10)
    for s in cut["segments"]:
        k, t, tag = s["kind"], s["text"], s.get("tag", "")
        p = d.add_paragraph()
        if k == "head":
            p.add_run(t).bold = True
        elif k == "cue":
            r = p.add_run(t); r.italic = True; r.font.size = Pt(10.5)
        else:
            if tag:
                r = p.add_run(tag + " "); r.italic = True; r.bold = True; r.font.size = Pt(10.5)
            p.add_run(t)
    if cut.get("backup_cuts"):
        d.add_paragraph().add_run("IF UR OVER TIME (cut these first, in this order)").bold = True
        for t in cut["backup_cuts"]:
            d.add_paragraph(t)
        if cut.get("never_cut"):
            d.add_paragraph("Do NOT cut: " + cut["never_cut"])
    d.save(out)
    res["wrote"] = out
    return res


def main(a):
    wpm = 149
    if "--wpm" in a:
        i = a.index("--wpm"); wpm = float(a[i + 1]); del a[i:i + 2]
    if not a:
        print(__doc__); return 1
    cmd = a[0]
    if cmd == "extract" and len(a) == 3:
        open(a[2], "w", encoding="utf-8").write(load_source(a[1])); print("wrote", a[2]); return 0
    if cmd in ("check", "build") and len(a) >= 3:
        cut = json.load(open(a[2], encoding="utf-8"))
        res = check(a[1], cut, wpm) if cmd == "check" else build(a[1], cut, a[3], wpm)
        print(json.dumps(res, indent=1))
        return 0 if not res["unverified_lines"] else 2
    print(__doc__); return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
