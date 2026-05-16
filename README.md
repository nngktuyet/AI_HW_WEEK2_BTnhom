
Mobile-style Flask demo for food ordering recommendations using the uploaded `rules-1.ipynb` and `AI_dataset_HW_week2 (2).xlsx`.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## What changed in V12

- Rebuilt `restaurants.csv` and `menu.csv` again directly from the new Excel file.
- Verified exact core data transfer: 68 restaurants and 344 menu items, with 0 mismatches for IDs, names, and menu prices.
- Health goal only includes: Giảm cân, Cân bằng, Tăng cơ.
- Removed cuisine selection from the app flow.
- Removed spicy-level logic/input from the app flow.
- Changed suggestion mode to only 2 options: Bình thường and Ăn chay.
- Bình thường includes all menu items, including vegetarian food.
- Ăn chay filters vegetarian restaurants/items only.
- Centered the suggestion-mode title/card area and the location/weather header.
- Home label remains: Đa dạng quán.
- Recommendation scoring follows the rule notebook weights: price 0.3, meal 0.5, distance 0.2.


## V15 Patch

This version fixes meal recommendation scoring by matching menu categories directly with fuzzy rule strengths instead of using a numeric meal centroid. It also adds budget guardrails, softer balanced-health logic, and lower rating weight in restaurant ranking.


## V21 UI cleanup

- Removed restaurant rating display from recommendation cards and restaurant detail header.
- Removed food thumbnails from the restaurant menu list to make the menu cleaner.
