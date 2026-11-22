# Build pipeline

- fetch.py: pulls texts from Sefaria (cached).
- content.py / figures.py / summaries.py: guided content written with Claude.
- build_data.py: builds data.json (expects raw.json from `python3 fetch.py 670 671 raw.json`).
- app.html: the app (claude.ai version loads data.json; deploy.sh inlines it into ../index.html).

To add a siman: fetch it, add its content entries, rebuild, deploy.
