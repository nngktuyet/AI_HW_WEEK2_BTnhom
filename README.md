# FoodMood

FoodMood là ứng dụng gợi ý món ăn và nhà hàng được xây dựng bằng *Flask*. Hệ thống sử dụng dữ liệu từ hai file CSV gồm thông tin nhà hàng và món ăn, kết hợp với logic mờ để đưa ra gợi ý phù hợp với ngân sách, mức độ đói, thời gian chờ, thời tiết và mục tiêu sức khỏe của người dùng.

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

## Dataset

Project sử dụng 2 tập dữ liệu chính:

| File | Nội dung |
|---|---|
| restaurants.csv | Thông tin nhà hàng |
| menu.csv | Thông tin món ăn/thức uống |

Bộ dữ liệu hiện có:

- 68 nhà hàng
- 344 món ăn/thức uống

## Tính năng chính

- Gợi ý món ăn và nhà hàng theo ngữ cảnh người dùng
- Sử dụng fuzzy logic để xử lý các input như ngân sách, mức độ đói, thời gian chờ, thời tiết và mục tiêu sức khỏe
- Tự động lấy vị trí và thời tiết hiện tại nếu người dùng cho phép
- Hiển thị chi tiết nhà hàng
- Thêm món vào giỏ hàng
- Checkout đơn hàng
- Mô phỏng trạng thái đơn hàng
- Ước lượng phí giao hàng và thời gian giao hàng

## Cấu trúc project

```text
foodmood/
│
├── app.py
├── data/
│   ├── restaurants.csv
│   └── menu.csv
│
├── templates/
├── static/
├── requirements.txt
└── README.md
