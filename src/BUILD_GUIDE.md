# מדריך בנייה – בית מדרש (לכל סשן של Claude שבונה סימן חדש)

המשתמש: רב קהילה (גיא). המטרה: **שליטה בהלכה למעשה**, מן המקורות. כל הכתוב לו – בעברית בלבד.
האפליקציה פרטית, לשימוש אישי, ומשמשת גם להכנת שיעורים של רבע שעה בקהילה.

## איפה הכול נמצא
- `src/content/<siman>.json` – התוכן שכתב Claude לכל סימן (ראה סכמה למטה). **סימן חדש = קובץ חדש.** העתק את המבנה של `671.json`.
- `src/content/schedule.json` – לוח הלימוד היומי. הוסף ימים לסימנים חדשים.
- `src/build.py` – שולף טקסטים מספריא (sefaria.org, מותר בהגדרות), מרכיב `build/data.json`, `build/app.html`, ו־`../index.html` (האתר העצמאי ב־GitHub Pages).
- `src/app.html` – קוד האפליקציה. אל תשנה אותו בלי צורך.
- `src/deploy.sh "הודעה"` – בונה, עושה commit ו־push ל־`main`. האתר: https://guyamir17.github.io/bet-midrash
- גרסת Claude של האפליקציה: artifact slug `5d65efbe-610f-49b3-a882-750b4555e85e`. לפרסם עם `publish_files` (מצב patch), את `build/app.html` בתור `index.html` ואת `build/data.json` בתור `data.json`. קרא קודם `get_artifact` כדי לקבל base_version.
- התקדמות המשתמש: ב־artifact db, מסמך `progress/main` (`seifim: {"671-2": {learned, stage, due}}`). קרא עם `db_get`.

## שרשרת הלימוד בכל סעיף (לפי הסדר)
1. **"מה לחפש"** (`before`) – משפט או שניים שמכוונים לקריאה.
2. **מקורות** (`sources`) – גמרא ← רש"י/תוספות/ראשונים על אותו קטע ← רמב"ם. **בסדר לימוד**, כל קטע גמרא ואחריו מפרשיו.
   - בחר ידנית את ה־refs (הקישורים האוטומטיים של ספריא מבולבלים – אל תסמוך עליהם). בדוק את הטקסט של כל ref לפני שאתה כותב עליו.
   - מקור ארוך – רק הקטעים המשמעותיים, עם `excerpt: [[מילות פתיחה, מילות סיום], ...]` (בלי ניקוד). הכפתור "המקור המלא" מציג את השאר.
   - `pre` / `post` לכל מקור – **רק איפה שיש מה להדגיש**. כל הערה **מזכירה במפורש את שם המקור** ("רש"י מסביר כאן…", "תוספות מקשים…"), כי היא מוצגת בתוך הכרטיס של אותו מקור. **בלי** המילים "לפני"/"אחרי".
   - **להסביר מושגים קשים** (למשל מהלכות טומאה) ו**את מהלך הקושיה והתירוץ** בשפה פשוטה. להיזהר מדיוק (טעות שהמשתמש תפס: "היסט = מזיז בלי לגעת" – צריך: הזזה, גם בלי מגע ישיר, ומטמאת גם כלי חרס).
   - חלקים שהם רקע ולא דין (למשל סיפור הנס) – לסמן ב־`bg` כדי שיוצגו בתיבה מתקפלת.
3. **"בקצרה"** (`after_sources`).
4. **טור ובית יוסף** – `by` = אינדקסים של קטעי הב"י הרלוונטיים; `by_note`; `by_excerpts` לקטעים ארוכים; **`by_summary` – סיכום תמציתי בנקודות** (חובה).
5. **שולחן ערוך ורמ"א** + `after_sa` (הדגשה).
6. **נושאי כלים** – נשלפים אוטומטית לפי הסעיף. כתוב `after_comm` ו־`comm_notes` (pre/post לס"ק חשובים, עם שם המפרש).
7. **פוסקי זמננו** – `yy`: פסקי ילקוט יוסף **בסיכום ובלשון שלך** (לא ציטוט; הספר אינו בספריא). חפש ברשת מקורות לפסקים ומסור מאיפה. אם אין מקור – אל תמציא. `yy_note` להבדלים ספרדי/אשכנזי.
8. **הלכה למעשה** (`practice.rules`, `practice.cases`) – **הדגש העיקרי**. כללים קצרים עם מקור, הבחנה ספרדים/אשכנזים, ו־2–3 "שאלות מצויות" מהקהילה עם תשובה. אם אין פוסק מפורש – כתוב שזה שיקול שלך.
9. **שאלות שליפה** (`questions`) – 2–4 לכל סעיף.
10. **מושגים** (`concepts`) – הסבר מעשי (מה זה אומר בפועל, במידות של היום), כל מושג עם `after` = ה־ref של המקור שעוסק בו (או `"sa"` / `"by"`). **לא** רשימה בתחילת הסעיף.
11. **שרטוטים** (`figures`) – SVG פשוט כשיש מיקום/גובה/סידור. טקסט מספרי בתוך SVG: לא טווחים עם מקף (נהפכים ב־RTL) – כתוב "80 עד 96". בדוק את הרינדור בצילום מסך.
12. **`summary`** לכל סעיף (לדף "סיכומים לחזרה ולשיעור"): `title, gemara, rishonim, tur_by, sa, rema, ach, lemaase` – שורה או שתיים לכל אחד. ובראש הקובץ `summary.hook` (שאלת פתיחה לשיעור) ו־`summary.closing`.

## פתיחה לסימן
`intro` – **כללית**: על מה הסימן, רקע קצר, מבנה הסעיפים, למה זה חשוב לרב קהילה. **בלי** ירידה למחלוקות.

## דיוק
- כל טענה על מקור – רק אחרי שקראת את הטקסט שלו (ספריא). מה שלא בדקת – לא לכתוב, או לסמן "לבדוק".
- ציטוטים – רק מהטקסט שנשלף. ילקוט יוסף ופוסקים אחרונים שאינם בספריא – רק בסיכום, עם ציון המקור המשני.
- אחרי הבנייה: לפתוח את האפליקציה בדפדפן headless (playwright + /usr/bin/google-chrome), לצלם מסך של סעיף ושל שרטוט, ולוודא שאין שגיאות.

## פסקי הרב יעקב אריאל – "אוהלי הלכה" (שדה `ariel`)
Guy supplied the book "אוהלי הלכה – הלכות חנוכה" (rulings of Rav Yaakov Ariel; for Ashkenazim and Sephardim). It is a key practical source.
- `src/content/ariel_digest.json` holds a paraphrased digest of the book's rulings, by siman (673–683), each with a chapter/section ref; `own: true` marks rulings the book explicitly labels "הכרעת הגר"י אריאל".
- For each seif, add `ariel: [{t, ref, own?}]` with the relevant rulings (move each digest item to the seif it belongs to; reword if needed, never quote at length). The app shows them in "פוסקי זמננו" under the label "הרב אריאל", with a badge for `own`.
- Each digest item may carry `ach`: the Acharonim the book cites in its footnotes (שמש ומגן, הרב קנייבסקי, חזון איש, חזון עובדיה, הגרש"ז, הגרי"ש וכו'), in summary. Copy it into the seif's `ariel` item as `ach`; the app shows it under the ruling as "בהערות". Guy values these footnote opinions – keep them.
- Use the book's rulings to strengthen the practice section (rules + cases), naming him as the source. Where he differs from Yalkut Yosef / MB, say so explicitly in `yy_note` or the practice rules.
- The book text itself is NOT in the repo (copyright; the repo is public). Do not add it.

## סיכום הסוגיה – mandatory for every seif (Guy's rule: "לא כותבים דבר בלי מקור")
The seif `summary` chain is shown on each seif page as "סיכום הסוגיה" (and on the summaries page). Rules:
- Start from the Gemara: the `gemara` row names the speaker and the exact place (e.g. "רבה (שבת כב ע\"א): ..."). If the seif has no Gemara source, cite the earliest source (ברייתא, מסכת סופרים פרק/הלכה, a Rishon) with its place.
- Every row, and every sentence inside `lemaase`, names its source in parentheses: (שו"ע), (רמ"א), (משנה ברורה ס"ק X), (ילקוט יוסף, בסיכום), (הרב אריאל), etc. Where poskim disagree, say who holds what.
- No statement without a source you actually read. If you cannot source a practical point, leave it out.
- The summary should put a tangled sugya in order: the question, each Rishon's reason, what the Tur/BY add and why (e.g. the BY's reinterpretation of a Gemara case), and the practical outcome.

## תרשים זרימה – `flow` (mandatory for every seif; Guy asked for it at the end of each sugya)
`flow: [{s: stage, n: [{w: who, t: short text (≤12 words), k: bool, tr: ""|"r"}]}]`
- Stages in order, skip empty ones: גמרא → ראשונים → טור ובית יוסף → שולחן ערוך → רמ"א → אחרונים → למעשה.
- Several nodes in one stage = the different opinions side by side (e.g. רש"י | תוספות | רשב"א).
- `k: true` marks the line the Shulchan Aruch follows (gold); `tr: "r"` marks the Rema/Ashkenazi line where it splits off (blue). In למעשה, split ספרדים / אשכנזים when they differ.
- Every node names its source; nothing that is not already in the seif's summary chain. The app renders it as "תרשים זרימה" after "סיכום הסוגיה".

## מחלוקות ראשונים – מתי מותר לכתוב "חולק" (Guy's rule, Nov 2026)
Never infer a dispute between Rishonim from the fact that they say different things. Mark or describe a dispute ONLY when one of these says so explicitly:
1. the Beit Yosef (or the Tur) presents it as a dispute (e.g. "אבל התוספות כתבו", "ודלא כהרמב"ם", "ולא נהירא");
2. a Rishon explicitly rejects another in his own words (e.g. the Rashba on Rashi: "ואינו מחוור בעיני");
3. a reliable website (yeshiva.org.il, etzion.org.il, toraland.org.il, Peninei Halakha, din.org.il etc.) states it – cite the page.
Otherwise present the views as complementary, without "חולק".
In `flow`, a stage with a documented dispute gets `"rel": "מחלוקת"` and `"src": "<where the dispute is stated>"`; the app shows "⇄ מחלוקת · מקור: …". Stages without it are read as complementary views.
Only name a Rishon in a stage if you read his words (in the BY, on Sefaria, or on a cited site).

## Seif page length
The seif page no longer shows "סיכום הסוגיה"; the `summary` chain is still required (it feeds the summaries page for shiurim). The flow chart is the end-of-seif overview, so make it carry the structure: who says what, where it splits, what the SA follows.
