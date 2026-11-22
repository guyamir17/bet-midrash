# Simple explanatory diagrams (SVG), placed after the source they explain.
FONT = "font-family='Assistant, sans-serif'"
INK, MUTED, BLUE, GOLD, GREEN, RED = "#24221e", "#6f685c", "#1f4e79", "#a8741a", "#2f6b4f", "#a33a1f"

def svg(w, h, body, y0=0):
    return (f"<svg viewBox='0 {y0} {w} {h-y0}' xmlns='http://www.w3.org/2000/svg' {FONT} role='img' "
            f"style='width:100%;height:auto;display:block'><style>text{{direction:rtl;unicode-bidi:plaintext}}</style>{body}</svg>")

def candle(x, y, s=1.0, color=GOLD):
    return (f"<g transform='translate({x},{y}) scale({s})'>"
            f"<rect x='-3' y='0' width='6' height='12' rx='1.5' fill='#efe3c6' stroke='{color}' stroke-width='1'/>"
            f"<path d='M0,-11 C4,-6 4,-2 0,0 C-4,-2 -4,-6 0,-11 Z' fill='#f2a33a' stroke='#d9822b' stroke-width='0.8'/></g>")

def t(x, y, s, size=12, color=INK, weight=400, anchor="middle"):
    return f"<text x='{x}' y='{y}' font-size='{size}' fill='{color}' font-weight='{weight}' text-anchor='{anchor}'>{s}</text>"

def person(x, y, c=BLUE):
    return f"<g fill='{c}'><circle cx='{x}' cy='{y}' r='5'/><path d='M{x-7},{y+18} Q{x},{y+3} {x+7},{y+18} Z'/></g>"

# 1. Where to place the candle: Rashi / Tosafot / Rashba
placement = svg(340, 270, "".join([
    f"<rect x='0' y='212' width='340' height='58' fill='#e7e2d7'/>",
    t(170, 258, "רשות הרבים (הרחוב)", 12, MUTED),
    f"<path d='M150,212 L40,212 L40,62 L300,62 L300,212 L190,212' fill='#f6efdc' stroke='{GOLD}' stroke-width='2'/>",
    t(68, 84, "חצר", 13, GOLD, 700),
    t(232, 226, "פתח החצר", 10, MUTED),
    f"<path d='M155,104 L110,104 L110,22 L230,22 L230,104 L185,104' fill='#dfe8f2' stroke='{BLUE}' stroke-width='2'/>",
    t(170, 62, "בית", 14, BLUE, 700),
    t(170, 98, "פתח הבית", 10, MUTED),
    candle(170, 112), t(118, 122, "רש״י", 13, BLUE, 700),
    candle(170, 196), t(118, 205, "תוספות", 13, GREEN, 700),
    candle(170, 236), t(112, 244, "רשב״א", 13, RED, 700),
]))
placement_cap = "רש\"י: בתוך החצר, על פתח הבית. תוספות (וכך פוסק השולחן ערוך): על פתח החצר שפונה לרחוב. הרשב\"א: \"מבחוץ ממש\", ברחוב."

# 2. Upper storey opening into the house
aliya = svg(360, 240, "".join([
    f"<rect x='0' y='206' width='360' height='34' fill='#e7e2d7'/>", t(250, 228, "רשות הרבים", 11, MUTED),
    f"<rect x='70' y='40' width='170' height='166' fill='#dfe8f2' stroke='{BLUE}' stroke-width='2'/>",
    f"<line x1='70' y1='123' x2='240' y2='123' stroke='{BLUE}' stroke-width='2'/>",
    t(130, 88, "עלייה", 14, BLUE, 700), t(160, 190, "בית", 14, BLUE, 700),
    f"<path d='M95,200 L95,186 L110,186 L110,172 L125,172 L125,158 L140,158 L140,144 L155,144 L155,130' fill='none' stroke='{MUTED}' stroke-width='1.5' stroke-dasharray='3 2'/>",
    t(112, 140, "מדרגות פנימיות", 9, MUTED),
    f"<rect x='185' y='160' width='30' height='46' fill='#fffdf8' stroke='{BLUE}' stroke-width='1.5'/>",
    t(200, 154, "פתח הבית", 10, MUTED),
    f"<rect x='180' y='62' width='40' height='36' fill='#fffdf8' stroke='{GOLD}' stroke-width='2'/>",
    candle(200, 84),
    t(300, 74, "חלון העלייה", 11, GOLD, 700), t(300, 89, "הסמוך לרה״ר", 11, GOLD, 700),
]))
aliya_cap = "כך הבית יוסף מסביר את הטור: העלייה פתוחה לבית, ואין לה פתח משלה לרחוב או לחצר. נר בפתח הבית ייראה כנר של הבית. רק נר בחלון העלייה מראה שהוא שייך לה."

# 3. Heights: 3 tefachim, 10 tefachim, 20 amot
def ycm(cm): return 236 - cm * 1.7
heights = svg(340, 260, "".join([
    t(85, 16, "ליד הקרקע", 12, INK, 700),
    f"<line x1='10' y1='236' x2='160' y2='236' stroke='{INK}' stroke-width='2'/>",
    f"<rect x='40' y='{ycm(96)}' width='110' height='{ycm(80)-ycm(96)}' fill='#f8e9df'/>",
    f"<rect x='40' y='{ycm(80)}' width='110' height='{ycm(29)-ycm(80)}' fill='#e9f3ec'/>",
    f"<rect x='40' y='{ycm(29)}' width='110' height='{ycm(24)-ycm(29)}' fill='#f8e9df'/>",
    f"<line x1='30' y1='{ycm(29)}' x2='150' y2='{ycm(29)}' stroke='{GOLD}' stroke-dasharray='4 3'/>",
    f"<line x1='30' y1='{ycm(80)}' x2='150' y2='{ycm(80)}' stroke='{GOLD}' stroke-dasharray='4 3'/>",
    t(95, ycm(24) + 14, "3 טפחים: 24 עד 29 ס״מ", 10, INK, 600),
    t(95, ycm(96) - 6, "10 טפחים: 80 עד 96 ס״מ", 10, INK, 600),
    candle(95, ycm(55), 1.3, GREEN),
    t(95, ycm(55) + 34, "לכתחילה כאן", 11, GREEN, 700),
    t(280, 16, "בניין", 12, INK, 700),
    f"<line x1='175' y1='236' x2='340' y2='236' stroke='{INK}' stroke-width='2'/>",
    f"<rect x='235' y='30' width='90' height='206' fill='#dfe8f2' stroke='{BLUE}' stroke-width='1.5'/>",
    *[f"<line x1='235' y1='{236-18*3*k}' x2='325' y2='{236-18*3*k}' stroke='{BLUE}' stroke-width='1'/>" for k in (1, 2, 3)],
    t(280, 216, "קרקע", 10, MUTED), t(280, 162, "קומה א׳", 10, MUTED), t(280, 108, "קומה ב׳", 10, MUTED), t(280, 54, "קומה ג׳", 10, MUTED),
    f"<rect x='225' y='{236-18*11.5}' width='110' height='{18*(11.5-9.6)}' fill='#a33a1f' opacity='0.18'/>",
    f"<line x1='180' y1='{236-18*9.6}' x2='335' y2='{236-18*9.6}' stroke='{RED}' stroke-width='2'/>",
    t(200, 236 - 18 * 9.6 - 6, "20 אמה", 11, RED, 700),
    t(200, 236 - 18 * 9.6 + 12, "9.6 עד 11.5 מ׳", 9, RED),
]))
heights_cap = "משמאל: מצווה להניח את הנר למעלה משלושה טפחים ולמטה מעשרה. בדיעבד, גם אם הניח למעלה מעשרה, יצא. מימין: נר שמונח מעל עשרים אמה מהקרקע פסול. בבניין רגיל זה בערך הגובה של קומה ג׳. השרטוטים לא באותו קנה מידה."

# 4. Doorway: mezuzah right, candle left within a tefach
doorway = svg(340, 250, "".join([
    f"<rect x='95' y='30' width='150' height='16' fill='#c9b48a'/>",
    f"<rect x='95' y='30' width='16' height='200' fill='#c9b48a'/>", f"<rect x='229' y='30' width='16' height='200' fill='#c9b48a'/>",
    f"<rect x='111' y='46' width='118' height='184' fill='#fbf6ea'/>",
    t(170, 140, "הפתח", 13, MUTED),
    f"<line x1='0' y1='230' x2='340' y2='230' stroke='{INK}' stroke-width='2'/>",
    f"<rect x='233' y='70' width='8' height='34' rx='3' fill='{BLUE}'/>",
    t(285, 82, "מזוזה", 12, BLUE, 700), t(285, 97, "ימין הנכנס", 10, BLUE),
    candle(80, 150, 1.4),
    f"<line x1='80' y1='190' x2='95' y2='190' stroke='{GOLD}' stroke-width='1.5'/>",
    f"<line x1='80' y1='185' x2='80' y2='195' stroke='{GOLD}'/>", f"<line x1='95' y1='185' x2='95' y2='195' stroke='{GOLD}'/>",
    t(55, 130, "נר חנוכה", 12, GOLD, 700), t(55, 208, "בתוך טפח מהפתח", 10, GOLD),
    t(55, 145, "שמאל הנכנס", 10, GOLD),
    t(170, 22, "מבט מבחוץ, לעבר הפתח", 11, MUTED),
]))
doorway_cap = "מי שנכנס עובר בין שתי מצוות: המזוזה מימינו ונר החנוכה משמאלו. הנר מונח בתוך טפח (כ־8–10 ס״מ) מהפתח, כדי שיהיה ניכר שבעל הבית הניח אותו."

# 5. Tosafot: four lights are ambiguous
def row_of_candles(cx, y, n, gap=16):
    x0 = cx - gap * (n - 1) / 2
    return "".join(candle(x0 + k * gap, y) for k in range(n))
hekker = svg(340, 250, "".join([
    t(170, 20, "מי שרואה ארבעה נרות דולקים:", 13, INK, 700),
    row_of_candles(170, 48, 4, 20),
    f"<rect x='12' y='86' width='150' height='120' rx='12' fill='#f6ecd8'/>",
    f"<rect x='178' y='86' width='150' height='120' rx='12' fill='#e6eef6'/>",
    t(253, 108, "אדם אחד", 13, BLUE, 700), person(253, 122),
    t(253, 166, "היום הרביעי", 13, BLUE, 700),
    t(87, 108, "ארבעה אנשים", 13, GOLD, 700), *[person(51 + 24 * k, 122, GOLD) for k in range(4)],
    t(87, 166, "היום הראשון", 13, GOLD, 700),
    t(170, 152, "או", 14, MUTED, 700),
    t(170, 232, "אין היכר כמה ימים עברו", 13, RED, 700),
]))
hekker_cap = "זו קושיית תוספות: אם כל אחד מבני הבית מדליק ומוסיף נר בכל לילה, מספר הנרות כבר לא מראה איזה יום היום. לכן, לפי תוספות, ההוספה נעשית על נר אחד לכל הבית. הרמ\"א פותר את הבעיה אחרת: כל אחד מבני הבית מניח את נרותיו במקום נפרד."

# 6a. Bowl of wicks: uncovered vs covered
bowl = svg(340, 200, "".join([
    f"<path d='M20,120 Q85,170 150,120 Z' fill='#d9c7a0' stroke='{GOLD}' stroke-width='1.5'/>",
    "<path d='M50,118 C60,70 110,70 120,118 Z' fill='#f2a33a' opacity='0.9'/>",
    "<path d='M65,118 C75,85 95,85 105,118 Z' fill='#f7c35a'/>",
    t(85, 160, "לא כפה עליה כלי", 12, RED, 700), t(85, 177, "הלהבות מתחברות – מדורה", 11, RED),
    f"<path d='M190,120 Q255,170 320,120 Z' fill='#d9c7a0' stroke='{GOLD}' stroke-width='1.5'/>",
    f"<path d='M192,120 Q255,68 318,120 Z' fill='#cfd8e3' stroke='{BLUE}' stroke-width='1.5'/>",
    *[f"<path d='M{x},{y} C{x+4},{y-6} {x+4},{y-10} {x},{y-15} C{x-4},{y-10} {x-4},{y-6} {x},{y} Z' fill='#f2a33a'/>" for x, y in ((208, 112), (232, 96), (255, 90), (278, 96), (302, 112))],
    t(255, 160, "כפה עליה כלי", 12, GREEN, 700), t(255, 177, "כל פתילה – נר בפני עצמו", 11, GREEN),
]), y0=55)
bowl_cap = "קערה מלאה שמן, ופתילות סביב השפה. אם לא כיסו אותה, הלהבות מתחברות לאש אחת, וזו מדורה ולא נר. כשכופים עליה כלי, כל פתילה יוצאת דרך נקב משלה, והלהבות נשארות נפרדות."

# 6b. Row vs circle
def circle_candles(cx, cy, r, n):
    import math
    return "".join(candle(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n))
rowcircle = svg(340, 150, "".join([
    row_of_candles(85, 60, 8, 17),
    t(85, 105, "בשורה, בשווה", 12, GREEN, 700), t(85, 122, "✓", 16, GREEN, 700),
    circle_candles(255, 55, 26, 8),
    t(255, 105, "בעיגול", 12, RED, 700), t(255, 122, "✗ נראה כמדורה", 12, RED, 700),
]))
rowcircle_cap = "הרמ\"א: מעמידים את הנרות בשורה ישרה ולא בעיגול, כדי שלא ייראו כמדורה. המשנה ברורה מוסיף: גם לא \"אחד נכנס ואחד יוצא\", כלומר לא בשורה עקומה."

# 7. Two doorways on two sides
twodoors = svg(340, 260, "".join([
    f"<rect x='0' y='0' width='340' height='46' fill='#e7e2d7'/>", t(170, 28, "רחוב בצד צפון", 11, MUTED),
    f"<rect x='294' y='46' width='46' height='214' fill='#e7e2d7'/>",
    t(317, 160, "רחוב", 11, MUTED), t(317, 175, "במזרח", 11, MUTED),
    f"<rect x='90' y='70' width='160' height='150' fill='#dfe8f2' stroke='{BLUE}' stroke-width='2'/>",
    t(170, 150, "בית אחד", 14, BLUE, 700),
    f"<rect x='155' y='66' width='30' height='8' fill='#fffdf8' stroke='{BLUE}'/>",
    f"<rect x='246' y='130' width='8' height='30' fill='#fffdf8' stroke='{BLUE}'/>",
    candle(170, 82), candle(236, 145),
    t(170, 104, "פתח בצפון", 10, MUTED), t(205, 180, "פתח במזרח", 10, MUTED),
    person(60, 16), person(317, 205),
    t(60, 60, "רואה רק את", 10, INK, 600), t(60, 73, "הפתח הצפוני", 10, INK, 600),
    t(270, 248, "רואה רק את הפתח המזרחי", 10, INK, 600),
]))
twodoors_cap = "מי שעובר ברחוב אחד רואה רק פתח אחד. אם בעל הבית ידליק רק בפתח השני, העובר יחשוב שלא הדליק בכלל. לכן, כשהפתחים בשני צדדים, צריך להדליק בשניהם. כשהשניים באותו צד, רואים אותם יחד, ומספיק אחד. בזמננו, שמדליקים בפנים, מדליקים פעם אחת (רמ\"א)."

FIGURES = {
 (671, 2): [{"after": "Tosafot on Shabbat 21b:5:1", "svg": hekker, "cap": hekker_cap}],
 (671, 4): [{"after": "Shabbat 23b:2", "svg": bowl, "cap": bowl_cap}, {"after": "sa", "svg": rowcircle, "cap": rowcircle_cap}],
 (671, 5): [{"after": "Rashba on Shabbat 21b:6", "svg": placement, "cap": placement_cap}, {"after": "by", "svg": aliya, "cap": aliya_cap}],
 (671, 6): [{"after": "Shabbat 22a:1", "svg": heights, "cap": heights_cap}],
 (671, 7): [{"after": "Shabbat 22a:2", "svg": doorway, "cap": doorway_cap}],
 (671, 8): [{"after": "Shabbat 23a:10", "svg": twodoors, "cap": twodoors_cap}],
}
