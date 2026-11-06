# Aesthetic Catalogue

Things noted while travelling, over the years, with small black and white moving pictures made by script.

- Live: https://catalogue.ramos-saavedra.com
- GitHub Pages publishes the `site/` folder on every push to main.
- Words and links: `src/entries.json`. Pictures: `src/plates.py`, `src/plates2.py`, `src/plates3.py`, `src/plates4.py`, `src/plates5.py` (the colour plates) and `src/plates6.py` (worked back from Actionary operations), on one 64 by 64 grid. Black and white first: colour appears only where the entry is about colour, as a small soft accent.
- Rebuild from the repo root: `PYTHONPATH=src python3 src/plates.py`, then `PYTHONPATH=src python3 src/plates2.py`, then `PYTHONPATH=src python3 src/plates3.py`, then `PYTHONPATH=src python3 src/plates4.py`, then `PYTHONPATH=src python3 src/plates5.py`, then `PYTHONPATH=src python3 src/plates6.py`, then `python3 src/build_site.py`, then `python3 src/home_set.py`.
- `src/plates7.py` and `src/moves_meta.py` draw the move plates in `site/moves/`: operations with no catalogue entry, shown as the move itself. Only Actionary's Find one by eye uses them; they are not on this page.
- `src/home_set.py` turns a chosen set of plates into black on white for the Home page and writes `site/home.js`, which picks one on each load. It does nothing until its script tag is added to Home.

© Alejandro Ramos Saavedra. All rights reserved.
