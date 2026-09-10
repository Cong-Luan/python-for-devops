#Import thư viện psutil
import psutil

# Tạo giá trị max
THRESHOLDS = {
    "CPU": 80.0,
    "RAM": 80.0,
    "DISK": 80.0,
}

# Hàm lấy thông tin CPU, Ram, Disk
def check_CPU():
    return {
        "CPU": psutil.cpu_percent(interval=1),
        "RAM": psutil.virtual_memory().percent,
        "DISK": psutil.disk_usage("/").percent
    }

# Hàm so sánh với giá trị max
def check_metrics(name, value, threshold):
    if value > threshold:
        return f"Cảnh báo {name} {threshold:.0f}%", False
    return "Ổn định", True
    
# Main
def main():
    try:
        metrics = check_CPU()
    except Exception as exc:
        print(f"Loại lỗi: {type(exc)}")
        print(f"Lỗi: {exc}")
        return

    print("==== Kết quả kiểm tra hệ thống ====")
    all_healthy = True
    for name, value in metrics.items():
        status, healthy = check_metrics(name, value, THRESHOLDS[name])
        all_healthy = all_healthy and healthy
        print(f"{name}: {value:.1f}% -> {status}")
        
    print("Báo cáo", "Báo động" if not all_healthy else "Ổn định")

if __name__ == "__main__":
    main()

