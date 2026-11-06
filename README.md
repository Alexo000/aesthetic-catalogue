# Aesthetic Catalogue

Things noted while travelling, over the years, with small black and white moving pictures made by script.

- Live: https://catalogue.ramos-saavedra.com
- GitHub Pages publishes the `site/` folder on every push to main.
- Words and links: `src/entries.json`. Pictures: `src/plates.py`, `src/plates2.py`, `src/plates3.py`, `src/plates4.py` and `src/plates5.py` (the colour plates), on one 64 by 64 grid. Black and white first: colour appears only where the entry is about colour, as a small soft accent.
- Rebuild from the repo root: `PYTHONPATH=src python3 src/plates.py`, then `PYTHONPATH=src python3 src/plates2.py`, then `PYTHONPATH=src python3 src/plates3.py`, then `PYTHONPATH=src python3 src/plates4.py`, then `PYTHONPATH=src python3 src/plates5.py`, then `python3 src/build_site.py`.

© Alejandro Ramos Saavedra. All rights reserved.
