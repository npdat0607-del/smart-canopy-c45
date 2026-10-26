"""Generate a clearly labeled, synthetic dataset for the classroom demo."""
from itertools import product
import csv
from pathlib import Path

OUT = Path(__file__).parent / "data" / "smart_canopy_demo.csv"

def target(rain: str, light: str, roof: str) -> str:
    if rain == "CO":
        return "DONG" if roof == "MO" else "GIU"
    if light == "CAO":
        return "MO" if roof == "DONG" else "GIU"
    return "GIU"

def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for rain, light, temperature, roof, _ in product(
        ("CO", "KHONG"), ("THAP", "VUA", "CAO"), ("MAT", "NONG"),
        ("MO", "DONG"), range(10),
    ):
        rows.append({"mua": rain, "anh_sang": light, "nhiet_do": temperature,
                     "mai_hien_tai": roof, "hanh_dong": target(rain, light, roof)})
    with OUT.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Đã tạo {len(rows)} dòng dữ liệu mô phỏng: {OUT}")

if __name__ == "__main__":
    main()
