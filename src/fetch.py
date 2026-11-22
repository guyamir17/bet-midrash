import json, os, re, sys, time, urllib.parse, subprocess, hashlib

CACHE = "/home/claude/sefaria_cache"
os.makedirs(CACHE, exist_ok=True)

def get(path):
    """GET a Sefaria API path with disk cache + retries."""
    key = hashlib.md5(path.encode()).hexdigest()
    fp = os.path.join(CACHE, key + ".json")
    if os.path.exists(fp):
        with open(fp) as f:
            return json.load(f)
    url = "https://www.sefaria.org" + path
    for attempt in range(6):
        try:
            out = subprocess.run(["curl", "-sSL", "--max-time", "40", url],
                                 capture_output=True, text=True).stdout
            d = json.loads(out)
            with open(fp, "w") as f:
                json.dump(d, f, ensure_ascii=False)
            time.sleep(0.25)
            return d
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    print("FAILED", path, file=sys.stderr)
    return None

def q(ref):
    return urllib.parse.quote(ref.replace(" ", "_"), safe=",_.:'-")

def text_of(ref):
    """Hebrew text (nested lists) for a ref, or None."""
    d = get("/api/v3/texts/" + q(ref) + "?version=hebrew")
    if not d or "versions" not in d or not d["versions"]:
        d = get("/api/v3/texts/" + q(ref))
    if not d or "versions" not in d:
        return None
    vs = [v for v in d["versions"] if v.get("language") == "he"] or d["versions"]
    return vs[0].get("text")

def links_of(ref):
    return get("/api/links/" + q(ref) + "?with_text=0") or []

ALLOWED = re.compile(r"</?(b|i|small|big|strong|em|br)\s*/?>", re.I)
def clean(s):
    if s is None:
        return ""
    if isinstance(s, list):
        return "\n".join(clean(x) for x in s if x)
    s = str(s)
    s = re.sub(r"<sup[^>]*>.*?</sup>", "", s, flags=re.S)
    s = re.sub(r"<i class=\"footnote\">.*?</i>", "", s, flags=re.S)
    s = re.sub(r"<(?!/?(b|i|small|big|strong|em|br)\b)[^>]+>", "", s)
    s = re.sub(r"<(\w+)[^>]*>", r"<\1>", s)
    s = re.sub(r"<(i|b|small)>\s*</\1>", "", s)
    s = re.sub(r"<(i|b|small)>\s*</\1>", "", s)
    return s.strip()

# commentary books to pull, by Sefaria title prefix -> (key, Hebrew label)
COMM = [
    ("Magen Avraham", "ma", "מגן אברהם"),
    ("Turei Zahav on Shulchan Arukh, Orach Chayim", "taz", "ט\"ז"),
    ("Mishnah Berurah", "mb", "משנה ברורה"),
    ("Biur Halacha", "bh", "ביאור הלכה"),
    ("Sha'arei Teshuvah on Shulchan Arukh, Orach Chayim", "st", "שערי תשובה"),
    ("Kaf HaChayim on Shulchan Arukh, Orach Chayim", "kh", "כף החיים"),
    ("Beur HaGra on Shulchan Arukh, Orach Chayim", "gra", "ביאור הגר\"א"),
]

siman_cache = {}
def comm_piece(book, ref):
    """ref like 'Mishnah Berurah 671:4' or 'Biur Halacha 671:2:1'."""
    m = re.match(re.escape(book) + r" (\d+):(\d+)(?::(\d+))?(?:-(\d+))?$", ref)
    if not m:
        return None
    sim, a, b = int(m.group(1)), int(m.group(2)), m.group(3)
    k = (book, sim)
    if k not in siman_cache:
        siman_cache[k] = text_of(f"{book} {sim}")
    t = siman_cache[k]
    try:
        x = t[a - 1]
        if b is not None and isinstance(x, list):
            x = x[int(b) - 1]
        return clean(x)
    except Exception:
        return None

RISH = ["Rashi on ", "Tosafot on ", "Rif ", "Rosh on ", "Ran on Rif", "Rashba on ", "Ritva on ", "Meiri on ", "Rabbeinu Chananel on ", "Ramban on "]
def hetitle(l):
    ct = l.get("collectiveTitle")
    return ct.get("he") if isinstance(ct, dict) else None
def sortkey2(ref):
    return (ref.split(" ")[0], [int(n) if n.isdigit() else 0 for n in re.findall(r"\d+", ref)])

def sortkey(ref):
    return [int(n) for n in re.findall(r"\d+", ref.split(" ")[-1])]

def build(simanim):
    out = {"simanim": []}
    for sim in simanim:
        sa = text_of(f"Shulchan Arukh, Orach Chayim {sim}") or []
        tur = text_of(f"Tur, Orach Chayim {sim}") or []
        by = text_of(f"Beit Yosef, Orach Chayim {sim}") or []
        ahs = text_of(f"Arukh HaShulchan, Orach Chaim {sim}") or []
        S = {"n": sim, "tur": [clean(x) for x in tur], "by": [clean(x) for x in by], "ahs": [clean(x) for x in ahs], "seifim": []}
        for i, seif in enumerate(sa, 1):
            ref = f"Shulchan Arukh, Orach Chayim {sim}:{i}"
            links = links_of(ref)
            sources, comms, contemporary = [], {k: [] for _, k, _ in COMM}, []
            seen = set()
            for l in links:
                r = l.get("ref", "")
                if r in seen:
                    continue
                seen.add(r)
                cat = l.get("category")
                if cat == "Talmud":
                    sources.append({"label": "גמרא", "ref": r, "kind": "a_talmud"})
                elif cat == "Halakhah" and r.startswith("Mishneh Torah"):
                    sources.append({"label": hetitle(l) or "רמב\"ם", "ref": r, "kind": "c_rambam"})
                elif cat == "Halakhah" and r.startswith("Peninei Halakhah"):
                    contemporary.append({"label": "פניני הלכה", "ref": r})
                else:
                    for book, k, _ in COMM:
                        if r.startswith(book + " "):
                            comms[k].append(r)
            # fetch source texts
            # rishonim on the gemara
            for s0 in [x for x in sources if x["kind"] == "a_talmud"]:
                for l2 in links_of(s0["ref"]):
                    ct = hetitle(l2)
                    r2 = l2.get("ref", "")
                    if l2.get("category") == "Commentary" and any(r2.startswith(p) for p in RISH) and r2 not in seen:
                        seen.add(r2)
                        sources.append({"label": ct, "ref": r2, "kind": "b_rishon", "on": s0["ref"]})
            srcs = []
            for s in sorted(sources, key=lambda s: (s["kind"], sortkey2(s["ref"]))):
                t = clean(text_of(s["ref"]))
                if t:
                    srcs.append({"label": s["label"], "ref": s["ref"], "kind": s["kind"][2:], "he": hebref(s["ref"]), "text": t})
            cm = []
            for book, k, label in COMM:
                pieces = []
                for r in sorted(comms[k], key=sortkey):
                    t = comm_piece(book, r)
                    if t:
                        pieces.append({"ref": r, "text": t})
                if pieces:
                    cm.append({"key": k, "label": label, "pieces": pieces})
            cont = []
            for c in contemporary:
                t = clean(text_of(c["ref"]))
                if t:
                    cont.append({"label": c["label"], "ref": c["ref"], "text": t})
            S["seifim"].append({"n": i, "text": clean(seif), "sources": srcs, "comm": cm, "contemporary": cont})
            print(sim, i, "src", len(srcs), "comm", [(c["key"], len(c["pieces"])) for c in cm], "cont", len(cont), flush=True)
        out["simanim"].append(S)
    return out

TRACT = {"Shabbat": "שבת", "Pesachim": "פסחים", "Sukkah": "סוכה", "Megillah": "מגילה",
         "Berakhot": "ברכות", "Taanit": "תענית", "Rosh Hashanah": "ראש השנה", "Yoma": "יומא",
         "Sotah": "סוטה", "Menachot": "מנחות", "Bava Kamma": "בבא קמא", "Bava Metzia": "בבא מציעא",
         "Avodah Zarah": "עבודה זרה", "Eruvin": "עירובין", "Beitzah": "ביצה", "Ketubot": "כתובות"}
def hebref(r):
    m = re.match(r"(.+?) (\d+)([ab])(?::[\d\-]+)?$", r)
    if m and m.group(1) in TRACT:
        return f"{TRACT[m.group(1)]} {heb_num(int(m.group(2)))} {'ע\"א' if m.group(3)=='a' else 'ע\"ב'}"
    m = re.match(r"Mishneh Torah, (.+?) (\d+):(\d+)", r)
    if m:
        return f"רמב\"ם, {m.group(1)} {m.group(2)}:{m.group(3)}"
    return r

def heb_num(n):
    ones = "אבגדהוזחט"; tens = "יכלמנסעפצ"; hund = "קרשת"
    s = ""
    while n >= 400: s += "ת"; n -= 400
    if n >= 100: s += hund[n // 100 - 1]; n %= 100
    if n == 15: s += "טו"; n = 0
    if n == 16: s += "טז"; n = 0
    if n >= 10: s += tens[n // 10 - 1]; n %= 10
    if n: s += ones[n - 1]
    return s

if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    data = build(range(a, b + 1))
    with open(sys.argv[3], "w") as f:
        json.dump(data, f, ensure_ascii=False)
