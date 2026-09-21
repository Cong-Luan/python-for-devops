# IMPROVE LOG ANALYZER
- Học và thêm 2 module "re" và "argparse" để hoàn thiện script thực tế hơn
```bash
import re 
import argparse  
```

- Tìm hiểu về cách hoạt động của module Logging và sử dụng nó để thay thế cho việc sử dụng print()
```bash
import logging 
```

- Sử dụng thêm lambda
```bash
new_file = max(log_file, key = lambda p: p.stat().st_mtime)
```
- Với mỗi file trong log_file gọi qua lambda p và lấy time sửa đổi cuối cùng
- .st_mtime : càng lớn thì file càng mới

