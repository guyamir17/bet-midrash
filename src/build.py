"""Build the app from content/*.json + texts fetched from Sefaria.

Usage:  python3 build.py            -> writes build/data.json, build/app.html (claude.ai version) and ../index.html (standalone, data inlined)
"""
import json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fetch import text_of, clean, links_of, comm_piece, COMM, heb_num
from excerpt import excerpt

LABELS = [("Rashi on", "רש\"י"), ("Tosafot on", "תוספות"), ("Rashba on", "רשב\"א"), ("Rif ", "רי\"ף"),
          ("Rosh on", "רא\"ש"), ("Ran on", "ר\"ן"), ("Meiri on", "מאירי"), ("Ritva on", "ריטב\"א"),
          ("Ramban on", "רמב\"ן"), ("Rabbeinu Chananel on", "ר\"ח"), ("Mishneh Torah", "רמב\"ם")]
TRACT = {"Shabbat": "שבת", "Pesachim": "פסחים", "Bava Kamma": "בבא קמא", "Megillah": "מגילה", "Sukkah": "סוכה",
         "Berakhot": "ברכות", "Taanit": "תענית", "Rosh Hashanah": "ראש השנה", "Yoma": "יומא", "Menachot": "מנחות",
         "Eruvin": "עירובין", "Beitzah": "ביצה", "Bava Metzia": "בבא מציעא", "Sotah": "סוטה", "Avodah Zarah": "עבודה זרה"}
MT = {"Scroll of Esther and Hanukkah": "הל' מגילה וחנוכה", "Sabbath": "הל' שבת", "Blessings": "הל' ברכות",
      "Prayer and the Priestly Blessing": "הל' תפילה", "Mourning": "הל' אבל"}

def gim(s): return s[:-1] + "״" + s[-1] if len(s) > 1 else s + "׳"

def kind_label(ref):
    for p, l in LABELS:
        if ref.startswith(p):
            return ("rambam" if l == "רמב\"ם" else "rishon"), l
    return "talmud", "גמרא"

def place(ref):
    m = re.search(r"Rif (\w[\w ]*?) (\d+)([ab])", ref)
    if m and m.group(1) in TRACT:
        return f"{TRACT[m.group(1)]} {heb_num(int(m.group(2)))} {'ע\"א' if m.group(3)=='a' else 'ע\"ב'} בדפי הרי\"ף"
    m = re.search(r"Rosh on (\w[\w ]*?) (\d+):(\d+)", ref)
    if m and m.group(1) in TRACT:
        return f"{TRACT[m.group(1)]} פרק {heb_num(int(m.group(2)))} סימן {heb_num(int(m.group(3)))}"
    for en, he in TRACT.items():
        m = re.search(re.escape(en) + r" (\d+)([ab])", ref)
        if m:
            return f"{he} {heb_num(int(m.group(1)))} {'ע\"א' if m.group(2)=='a' else 'ע\"ב'}"
    m = re.search(r"Mishneh Torah, (.+?) (\d+):(\d+)", ref)
    if m:
        return f"{MT.get(m.group(1), m.group(1))} {heb_num(int(m.group(2)))}, {heb_num(int(m.group(3)))}"
    return ""

def url(ref): return "https://www.sefaria.org/" + ref.replace(" ", "_").replace(":", ".")

def build_siman(C):
    n = C["n"]
    sa = text_of(f"Shulchan Arukh, Orach Chayim {n}") or []
    tur = text_of(f"Tur, Orach Chayim {n}") or []
    by = [clean(x) for x in (text_of(f"Beit Yosef, Orach Chayim {n}") or [])]
    S = {"n": n, "he": gim(heb_num(n)), "title": C["title"], "intro": C["intro"], "tur": [clean(x) for x in tur],
         "tur_note": C["tur_note"], "by_all": by, "seifim": []}
    for sc in C["seifim"]:
        i = sc["n"]
        text = clean(sa[i - 1])
        if i == 1:
            text = re.sub(r"^<b>.*?</b>(<br>)?", "", text)
        bgc = sc.get("bg") or {}
        srcs = []
        for s in sc["sources"]:
            t = clean(text_of(s["ref"]))
            if not t:
                print("MISSING SOURCE", s["ref"], file=sys.stderr); continue
            k, l = kind_label(s["ref"])
            srcs.append({"kind": k, "label": l, "place": place(s["ref"]), "ref": s["ref"], "url": url(s["ref"]), "text": t,
                         "ex": excerpt(t, s["excerpt"]) if s.get("excerpt") else "", "pre": s.get("pre", ""), "post": s.get("post", ""),
                         "bg": s["ref"] in bgc.get("sources", [])})
        # commentaries linked to this seif
        links = links_of(f"Shulchan Arukh, Orach Chayim {n}:{i}")
        comms, ph, seen = {k: [] for _, k, _ in COMM}, [], set()
        for l in links:
            r = l.get("ref", "")
            if r in seen: continue
            seen.add(r)
            if r.startswith("Peninei Halakhah, Zemanim"):
                ph.append(r)
            for book, k, _ in COMM:
                if r.startswith(book + " "):
                    m = re.search(r" (\d+):", r)
                    if m and int(m.group(1)) == n:
                        comms[k].append(r)
        notes = sc.get("comm_notes", {})
        cm = []
        for book, k, label in COMM:
            ps = []
            for r in sorted(comms[k], key=lambda r: [int(x) for x in re.findall(r"\d+", r.split(" ")[-1])]):
                t = comm_piece(book, r)
                if t:
                    nt = notes.get(r, {})
                    ps.append({"ref": r, "text": t, "pre": nt.get("pre", ""), "post": nt.get("post", ""), "bg": r in bgc.get("comm", [])})
            if ps:
                cm.append({"key": k, "label": label, "pieces": ps, "noted": sum(1 for p in ps if p["pre"] or p["post"])})
        for r in notes:
            if not any(p["ref"] == r for c in cm for p in c["pieces"]):
                print("UNUSED COMM NOTE", n, i, r, file=sys.stderr)
        phs = []
        for r in ph:
            t = clean(text_of(r))
            m = re.search(r"Zemanim (\d+):(\d+)", r)
            if t: phs.append({"label": "פניני הלכה", "ref": r, "url": url(r), "text": t,
                              "place": f"זמנים {heb_num(int(m.group(1)))}, {heb_num(int(m.group(2)))}" if m else ""})
        bex = C.get("by_excerpts", {})
        bylist = [{"i": b, "text": by[b], "ex": excerpt(by[b], bex[str(b)]) if str(b) in bex else "", "bg": b in bgc.get("by", [])} for b in sc["by"]]
        bsum = sc.get("by_summary", [])
        bsum_bg_idx = bgc.get("by_summary", [])
        S["seifim"].append({
            "n": i, "he": heb_num(i), "title": sc["title"], "before": sc["before"], "sources": srcs,
            "after_sources": sc["after_sources"], "by": bylist, "by_note": sc["by_note"],
            "by_summary": [t for j, t in enumerate(bsum) if j not in bsum_bg_idx],
            "by_summary_bg": [t for j, t in enumerate(bsum) if j in bsum_bg_idx],
            "sa": text, "after_sa": sc["after_sa"], "comm": cm, "after_comm": sc["after_comm"],
            "concepts": sc.get("concepts", []), "yy": sc.get("yy", []), "yy_note": sc.get("yy_note", ""), "ph": phs,
            "practice": sc.get("practice") or {"rules": [], "cases": []}, "questions": sc.get("questions", []),
            "figures": sc.get("figures", []),
            **({"bg": {"title": bgc["title"], "intro": bgc["intro"]}} if bgc else {}),
        })
    return S

def main():
    files = sorted(glob.glob(os.path.join(HERE, "content", "[0-9]*.json")), key=lambda p: int(os.path.basename(p)[:-5]))
    out = {"yy_src": json.load(open(os.path.join(HERE, "content", "yy_src.json"))), "simanim": [], "summaries": {},
           "schedule": json.load(open(os.path.join(HERE, "content", "schedule.json")))}
    for f in files:
        C = json.load(open(f))
        out["simanim"].append(build_siman(C))
        out["summaries"][str(C["n"])] = {"hook": C["summary"]["hook"], "closing": C["summary"]["closing"],
                                         "seifim": {str(s["n"]): s["summary"] for s in C["seifim"] if s.get("summary")}}
        print("built", C["n"], len(C["seifim"]), "seifim")
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    data = json.dumps(out, ensure_ascii=False)
    open(os.path.join(HERE, "build", "data.json"), "w").write(data)
    app = open(os.path.join(HERE, "app.html")).read()
    open(os.path.join(HERE, "build", "app.html"), "w").write(app)
    old = 'fetch("data.json").then(r => r.json()).then(d => { DATA = d; render(); })'
    assert old in app
    st = app.replace(old, 'Promise.resolve(JSON.parse(document.getElementById("bm-data").textContent)).then(d => { DATA = d; render(); })')
    st = st.replace('<script>\n"use strict";', '<script type="application/json" id="bm-data">' + data.replace('</', '<\\/') + '</script>\n<script>\n"use strict";')
    open(os.path.join(HERE, "..", "index.html"), "w").write(st)
    print("wrote build/data.json, build/app.html, ../index.html")

if __name__ == "__main__":
    main()
