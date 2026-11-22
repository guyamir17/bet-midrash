import re
NQ = re.compile(r"[֑-ׇ]")
def norm_map(s):
    out, idx = [], []
    for i, ch in enumerate(s):
        if NQ.match(ch):
            continue
        ch = {"״": '"', "׳": "'", "—": "-"}.get(ch, ch)
        out.append(ch); idx.append(i)
    return "".join(out), idx

def excerpt(html, ranges):
    plain = re.sub(r"<br\s*/?>", " ", html)
    plain = re.sub(r"<[^>]+>", "", plain)
    n, idx = norm_map(plain)
    parts, pos = [], 0
    for a, b in ranges:
        i = n.find(a, pos)
        if i < 0:
            raise ValueError("start not found: " + a)
        j = n.find(b, i)
        if j < 0:
            raise ValueError("end not found: " + b)
        j += len(b)
        # extend to end of word / punctuation
        while j < len(n) and n[j] in ".:,;)]?!":
            j += 1
        parts.append(plain[idx[i]: idx[j - 1] + 1].strip())
        pos = j
    return " … ".join(parts)
