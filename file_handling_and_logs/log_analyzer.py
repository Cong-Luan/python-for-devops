#Import Path và json
import json
from pathlib import Path

#Khai báo level và đường dẫn
LEVELS = ("INFO", "WARNING", "ERROR")
LOG_FILE = Path(__file__).parent / "webserver.log"

#Hàm đọc từng dòng file .log
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readline()
    except FileNotFoundError:
        print(f"Không tìm thấy file: {path}")
        return []

#Hàm Đếm số lần xuất hiện của mỗi level
def analyze_logs(lines):
    counts = {L : 0 for L in LEVELS}
    for line in lines:
        tokens = set(line.split())
        for L in LEVELS:
            if L in tokens:
                counts[L] += 1
    return counts

#Ghi kết quả ra file
def write_summary(counts, stem='report'):
    path = Path(__file__).parent
    with open(path / f"{stem}.txt", "w", encoding="utf-8") as f:
        for level in LEVELS:
            f.write(f"{level}: {counts[level]}\n")
    with open(path / f"{stem}.json", "w", encoding="utf-8") as f:
        json.dump(counts, f, indent=2)

#Main
def main():
    lines = read_file(LOG_FILE)
    if not lines:
        print("Không có thông tin")
        return 
    
    counts = analyze_logs(lines)
    print("=== Thống kê log ===")
    for level in LEVELS:
        print(f"{level:7s}: {counts[level]}")
    write_summary(counts)
    print("Đã ghi báo cáo vào file.")

if __name__ == "__main__":
    main()
    