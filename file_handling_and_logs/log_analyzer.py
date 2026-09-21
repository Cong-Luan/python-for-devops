#Import Path và json
import logging
import json
from pathlib import Path
import re
import argparse
#Khai báo level và đường dẫn
LEVELS = ('INFO','WARNING','ERROR','DEBUG','CRITICAL')
LEVELS_PATTERN = re.compile(r"\b(" + "|".join(LEVELS) + r")\b", re.IGNORECASE)
#Logging 
logging.basicConfig(
    level = logging.INFO,
    format = '%(levelname)s - %(asctime)s - %(name)s : %(message)s',
    handlers= [
        logging.FileHandler(f'script.py.log', encoding='utf-8'),    #tạo file .log ghi log
        logging.StreamHandler()                                     #hiển thị log ra màn hình console
    ]
)
logger = logging.getLogger(__name__)

#Tìm file .log trong thư mục 
def find_log_file(directory):
    log_file = list(directory.glob('*.log'))
    if not log_file:
        logger.warning(f"Không tìm thấy file log trong {directory.name}")
        return
    new_file = max(log_file, key = lambda p: p.stat().st_mtime)
    if len(log_file) > 1:
        logger.info(f"\n tim thấy nhiều file log, sử dụng file mới nhất: {new_file.name}")
    return new_file

#Đường dẫn
def parse_arg():
    parser = argparse.ArgumentParser(description="Phân tích lỗi trong file log")
    parser.add_argument("logfile", nargs="?", default=None, type=Path)
    parser.add_argument("--output", "--o", default="log_summary", help="Tên file báo cáo")
    args = parser.parse_args()

    if args.logfile is not None and args.logfile.suffix != ".log":
        parser.error(f"File {args.logfile.name} không phải .log")
    return args
    
#Hàm đọc từng dòng file .log
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        logger.error(f"Lỗi đọc file: {e}")
        return []

#Hàm Đếm số lần xuất hiện của mỗi level
def analyze_logs(lines):
    counts = {L : 0 for L in LEVELS}
    for line in lines:
        match = LEVELS_PATTERN.search(line)
        if match:
            counts[match.group(1).upper()] += 1
    return counts

#Ghi kết quả ra file
def write_summary(counts, stem):
    path = Path(__file__).parent
    with open(path / f"{stem}.txt", "w", encoding="utf-8") as f:
        for level in LEVELS:
            f.write(f"{level}: {counts[level]}\n")
    with open(path / f"{stem}.json", "w", encoding="utf-8") as f:
        json.dump(counts, f, indent=2)

#Main
def main():
    args = parse_arg()
    here = Path(__file__).parent
    
    log_file = args.logfile or find_log_file(here)
    
    if log_file is None:
        logger.error("Không tìm thấy file .log")
        return None
    
    lines = read_file(log_file)

    if not lines:
        logger.warning("Không có thông tin trong file")
        return
    counts = analyze_logs(lines)

    for level in LEVELS:
        logger.info(f"{level:7}: {counts[level]}")
    
    write_summary(counts, args.output)
    logger.info(f"\nKết quả được ghi vào {args.output}.txt và {args.output}.json")


if __name__ == "__main__":
    main()
    