import json, re, sys
from fetch import text_of, clean, hebref, heb_num
from content import SIMANIM, YY_SRC, SRC_NOTES, COMM_NOTES, CONCEPTS, EXCERPTS, BY_EXCERPTS, CONCEPT_AFTER, BY_SUMMARY, BG, PRACTICE, SCHEDULE
from excerpt import excerpt
from figures import FIGURES
from summaries import SUMMARIES

raw = json.load(open("/home/claude/raw.json"))
rawmap = {S["n"]: S for S in raw["simanim"]}

LABELS = [("Rashi on", "רש\"י"), ("Tosafot on", "תוספות"), ("Rashba on", "רשב\"א"), ("Rif ", "רי\"ף"),
          ("Rosh on", "רא\"ש"), ("Ran on", "ר\"ן"), ("Meiri on", "מאירי"), ("Mishneh Torah", "רמב\"ם")]
TRACT = {"Shabbat": "שבת", "Pesachim": "פסחים", "Bava Kamma": "בבא קמא"}

def kind_label(ref):
    for p, l in LABELS:
        if ref.startswith(p):
            return ("rambam" if l == "רמב\"ם" else "rishon"), l
    return "talmud", "גמרא"

def place(ref):
    m = re.search(r"Rif Shabbat (\d+)([ab])", ref)
    if m:
        return f"שבת {heb_num(int(m.group(1)))} {'ע\"א' if m.group(2)=='a' else 'ע\"ב'} בדפי הרי\"ף"
    m = re.search(r"(Shabbat|Pesachim|Bava Kamma) (\d+)([ab])", ref)
    if m:
        return f"{TRACT[m.group(1)]} {heb_num(int(m.group(2)))} {'ע\"א' if m.group(3)=='a' else 'ע\"ב'}"
    m = re.search(r"Hanukkah (\d+):(\d+)", ref)
    if m:
        return f"הל' מגילה וחנוכה {heb_num(int(m.group(1)))}, {heb_num(int(m.group(2)))}"
    m = re.search(r"Rosh on Shabbat (\d+):(\d+)", ref)
    if m:
        return f"שבת פרק {heb_num(int(m.group(1)))} סימן {heb_num(int(m.group(2)))}"
    return ""

def sefaria_url(ref):
    return "https://www.sefaria.org/" + ref.replace(" ", "_").replace(":", ".")

def gim(s):
    return s[:-1] + "״" + s[-1] if len(s) > 1 else s + "׳"

def comm_with_notes(n, i, comm):
    notes = COMM_NOTES.get((n, i), {})
    used = set()
    res = []
    for c in comm:
        ps = []
        for p in c["pieces"]:
            m = re.search(r" (\d+):", p["ref"])
            if m and int(m.group(1)) != n:
                continue
            nt = notes.get(p["ref"], {})
            if nt: used.add(p["ref"])
            ps.append({**p, "pre": nt.get("pre", ""), "post": nt.get("post", "")})
        if ps:
            res.append({**c, "pieces": ps, "noted": sum(1 for p in ps if p["pre"] or p["post"])})
    for r in notes:
        if r not in used: print("UNUSED NOTE", n, i, r, file=sys.stderr)
    return res

out = {"built": "2026-11-22", "yy_src": YY_SRC, "simanim": []}
for n, C in SIMANIM.items():
    R = rawmap[n]
    S = {"n": n, "he": gim(heb_num(n)), "title": C["title"], "intro": C["intro"], "tur": R["tur"], "tur_note": C["tur_note"],
         "by_all": R["by"], "seifim": []}
    for i, sc in C["seifim"].items():
        rs = R["seifim"][i - 1]
        text = rs["text"]
        if i == 1:
            text = re.sub(r"^<b>.*?</b>(<br>)?", "", text)
        srcs = []
        for ref in sc["sources"]:
            t = clean(text_of(ref))
            if not t:
                print("MISSING", ref, file=sys.stderr); continue
            k, l = kind_label(ref)
            nt = SRC_NOTES.get((n, i), {}).get(ref, {})
            srcs.append({"kind": k, "label": l, "place": place(ref), "ref": ref, "url": sefaria_url(ref), "text": t, "ex": excerpt(t, EXCERPTS[ref]) if ref in EXCERPTS else "",
                         "pre": nt.get("pre", ""), "post": nt.get("post", "")})
        cont = [c for c in rs["contemporary"] if c["ref"].startswith("Peninei Halakhah, Zemanim")]
        for c in cont:
            c["url"] = sefaria_url(c["ref"])
            m = re.search(r"Zemanim (\d+):(\d+):(\d+)", c["ref"])
            c["place"] = f"זמנים {heb_num(int(m.group(1)))}, {heb_num(int(m.group(2)))}" if m else ""
        S["seifim"].append({
            "n": i, "he": heb_num(i), "title": sc["title"], "before": sc["before"], "sources": srcs,
            "after_sources": sc["after_sources"],
            "by": [{"i": b, "text": R["by"][b], "ex": excerpt(R["by"][b], BY_EXCERPTS[(n, b)]) if (n, b) in BY_EXCERPTS else ""} for b in sc["by"]],
            "concepts": [{"t": a, "d": d, "after": CONCEPT_AFTER.get((n, i), {}).get(a) or CONCEPT_AFTER.get((n, i), {}).get("*") or "sa"} for a, d in CONCEPTS.get((n, i), [])], "by_note": sc["by_note"], "by_summary": BY_SUMMARY.get((n, i), []),
            "sa": text, "after_sa": sc["after_sa"],
            "comm": comm_with_notes(n, i, rs["comm"]), "after_comm": sc["after_comm"],
            "yy": sc["yy"], "yy_note": sc.get("yy_note", ""), "ph": cont,
            "questions": sc["questions"],
        })
    out["simanim"].append(S)

for S in out["simanim"]:
    for x in S["seifim"]:
        x["figures"] = FIGURES.get((S["n"], x["n"]), [])
        pr = PRACTICE.get((S["n"], x["n"]), {"rules": [], "cases": []})
        x["practice"] = pr
for S in out["simanim"]:
    for x in S["seifim"]:
        bg = BG.get((S["n"], x["n"]))
        if not bg:
            continue
        x["bg"] = {"title": bg["title"], "intro": bg["intro"]}
        for z in x["sources"]:
            z["bg"] = z["ref"] in bg["sources"]
        for b2 in x["by"]:
            b2["bg"] = b2["i"] in bg["by"]
        x["by_summary_bg"] = [t for j, t in enumerate(x["by_summary"]) if j in bg["by_summary"]]
        x["by_summary"] = [t for j, t in enumerate(x["by_summary"]) if j not in bg["by_summary"]]
        for c in x["comm"]:
            for p in c["pieces"]:
                p["bg"] = p["ref"] in bg["comm"]
out["schedule"] = SCHEDULE
out["summaries"] = {str(k): {"hook": v["hook"], "closing": v["closing"], "seifim": {str(i): s for i, s in v["seifim"].items()}} for k, v in SUMMARIES.items()}
json.dump(out, open("/home/claude/app/data.json", "w"), ensure_ascii=False)
print("ok", sum(len(s["seifim"]) for s in out["simanim"]))
