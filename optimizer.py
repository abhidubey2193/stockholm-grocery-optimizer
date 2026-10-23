"""Transparent, offline basket optimizer using user-provided prices."""
from dataclasses import dataclass
from itertools import combinations

@dataclass(frozen=True)
class Price:
    store: str
    item: str
    sek: float
    unit: str = "each"

def best_basket(items, prices, extra_store_penalty=15.0):
    items = list(dict.fromkeys(x.strip() for x in items if x.strip()))
    if extra_store_penalty < 0:
        raise ValueError("Extra-store penalty must be nonnegative")
    if not items:
        return {"stores": [], "basket": [], "subtotal_sek": 0, "penalty_sek": 0, "total_sek": 0}
    prices = [p for p in prices if p.sek >= 0]
    stores = sorted(set(p.store for p in prices))
    best = None
    for count in range(1, len(stores) + 1):
        for group in combinations(stores, count):
            basket = []
            for item in items:
                options = [p for p in prices if p.item == item and p.store in group]
                if not options:
                    break
                p = min(options, key=lambda row: (row.sek, row.store))
                basket.append({"item": item, "store": p.store, "price_sek": p.sek, "unit": p.unit})
            if len(basket) != len(items):
                continue
            used = sorted({p["store"] for p in basket})
            subtotal = round(sum(p["price_sek"] for p in basket), 2)
            penalty = round((len(used) - 1) * extra_store_penalty, 2)
            row = {"stores": used, "basket": basket, "subtotal_sek": subtotal,
                   "penalty_sek": penalty, "total_sek": round(subtotal + penalty, 2)}
            if best is None or (row["total_sek"], len(used)) < (best["total_sek"], len(best["stores"])):
                best = row
    if best is None:
        raise ValueError("Some requested items have no supplied prices")
    return best
