"""Train and run the smart canopy C4.5 classroom demonstration."""
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from c45 import fit, predict, print_tree

DATA = ROOT / "data" / "smart_canopy_demo.csv"
FEATURES = ["mua", "anh_sang", "nhiet_do", "mai_hien_tai"]
LABELS = {"MO": "MỞ", "DONG": "ĐÓNG", "GIU": "GIỮ NGUYÊN"}

def load_rows():
    with DATA.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main():
    rows = load_rows()
    train = [row for i, row in enumerate(rows) if i % 10 != 0]
    test = [row for i, row in enumerate(rows) if i % 10 == 0]
    tree = fit(train, FEATURES)
    correct = sum(predict(tree, row) == row["hanh_dong"] for row in test)
    print("=" * 58)
    print("DEMO MAI CHE THONG MINH - CAY QUYET DINH C4.5")
    print("Dữ liệu là mô phỏng; không phải kết quả đo ngoài thực tế.")
    print(f"Số dòng: {len(rows)} | Huấn luyện: {len(train)} | Kiểm tra: {len(test)}")
    print(f"Độ chính xác trên tập kiểm tra: {correct}/{len(test)} = {correct/len(test):.1%}")
    print("\nCây quyết định đã học:")
    print_tree(tree)
    examples = [
        {"mua": "CO", "anh_sang": "CAO", "nhiet_do": "NONG", "mai_hien_tai": "MO"},
        {"mua": "KHONG", "anh_sang": "CAO", "nhiet_do": "NONG", "mai_hien_tai": "DONG"},
        {"mua": "KHONG", "anh_sang": "THAP", "nhiet_do": "MAT", "mai_hien_tai": "MO"},
        {"mua": "KHONG", "anh_sang": "VUA", "nhiet_do": "NONG", "mai_hien_tai": "DONG"},
    ]
    print("\nTình huống demo:")
    for i, sample in enumerate(examples, 1):
        print(f"{i}. mưa={sample['mua']}, sáng={sample['anh_sang']}, "
              f"nhiệt={sample['nhiet_do']}, mái={sample['mai_hien_tai']} "
              f"=> {LABELS[predict(tree, sample)]}")
    print("\nNhập tình huống của bạn (Enter để bỏ qua).")
    try:
        rain = input("Mưa [CO/KHONG]: ").strip().upper()
    except EOFError:
        return
    if not rain:
        return
    light = input("Ánh sáng [THAP/VUA/CAO]: ").strip().upper()
    temperature = input("Nhiệt độ [MAT/NONG]: ").strip().upper()
    roof = input("Mái hiện tại [MO/DONG]: ").strip().upper()
    sample = {"mua": rain, "anh_sang": light, "nhiet_do": temperature,
              "mai_hien_tai": roof}
    valid = (rain in {"CO", "KHONG"} and light in {"THAP", "VUA", "CAO"}
             and temperature in {"MAT", "NONG"} and roof in {"MO", "DONG"})
    if not valid:
        print("Giá trị chưa hợp lệ. Hãy nhập đúng các lựa chọn trong ngoặc vuông.")
        return
    print("Dự đoán:", LABELS[predict(tree, sample)])

if __name__ == "__main__":
    main()


