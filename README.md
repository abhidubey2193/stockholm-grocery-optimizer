# Stockholm Grocery Basket Optimizer

Offline Python demo to optimize a shopping basket across a shortlist of seven Stockholm-area grocery stores using **user-supplied prices**.

## Run
```bash
python app.py
# Open http://127.0.0.1:8085
python -m unittest discover -s tests -v
```

Enter a comma-separated shopping list and JSON price records; the app chooses a basket that minimizes product cost plus a configurable extra-store penalty. The optimizer enumerates store combinations deterministically.

**Important:** Example prices are illustrative, not live retail prices. This is a limited rebuild, not the previously planned feature-complete grocery platform. No scraping, purchase history, stock availability, loyalty-price eligibility, unit normalization, translations, or route optimization. Compare prices only for equivalent products and units.
