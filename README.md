# 👑 N-Queens Solver

Giải bài toán **N-Queens (N Quân Hậu)** bằng hai thuật toán tìm kiếm cục bộ:  
**Hill Climbing** và **Simulated Annealing**

> 📚 Môn học: Trí Tuệ Nhân Tạo
> Đề tài 21: Giải câu đố N-Queens bằng thuật toán leo núi (Hill Climbing) và Tôi luyện giả lập (Simulated Annealing)
> Danh sách thành viên:
 Trịnh Gia Huy - 232661
 Dương Phước Duy - 232831
 Phạm Thành Luân - 232897
 Nguyễn Vĩnh Phước - 232913
 Phạm Quốc Huy - 232848
 Nguyễn Chí Công - 232685
## 🧩 Bài toán N-Queens

Đặt **N quân hậu** trên bàn cờ **N×N** sao cho **không có 2 quân nào tấn công nhau** (không cùng hàng, cột, hoặc đường chéo).

```
. Q . . . . . .
. . . . Q . . .
. . . . . . . Q
. . . . . Q . .
. . Q . . . . .
. . . . . . Q .
Q . . . . . . .
. . . Q . . . .
```
*Ví dụ: Một nghiệm hợp lệ cho bài toán 8-Queens*

---

## ⚙️ Thuật toán sử dụng

### 1. Hill Climbing (Leo núi)
- Từ trạng thái ngẫu nhiên, liên tục di chuyển sang trạng thái **ít xung đột hơn**
- Dừng khi không còn láng giềng nào tốt hơn (bị kẹt ở local optimum)
- Kết hợp **Random Restart** để thoát khỏi local optimum

### 2. Simulated Annealing (Tôi luyện giả lập)
- Tương tự Hill Climbing nhưng **đôi khi chấp nhận trạng thái tệ hơn** với xác suất `P = e^(-ΔE/T)`
- Nhiệt độ T giảm dần theo thời gian → xác suất chấp nhận trạng thái tệ giảm dần
- Giúp **thoát khỏi local optimum** hiệu quả hơn HC thuần túy

---

## 🚀 Cách chạy

### Yêu cầu
- Python 3.x (không cần cài thêm thư viện)

### Chạy chương trình
```bash
python n_queens_solver.py
```

### Thay đổi kích thước N
Mở file `n_queens_solver.py`, tìm dòng:
```python
N = 8  # Thay đổi N tại đây: 8, 16, 32...
```
Đổi thành N bất kỳ và chạy lại.

---

## 📊 Kết quả mẫu (N = 8)

```
==================================================
  BÀI TOÁN 8-QUEENS
==================================================

[1] Random-Restart Hill Climbing
    -> Kết quả       : THÀNH CÔNG ✓
    -> Số lỗi còn lại: 0
    -> Tổng bước đi  : 12
    -> Số lần restart: 3
    -> Thời gian     : 0.0021 giây

[2] Simulated Annealing
    -> Kết quả       : THÀNH CÔNG ✓
    -> Số lỗi còn lại: 0
    -> Số vòng lặp   : 1847
    -> Thời gian     : 0.0134 giây

==================================================
  BENCHMARK: 30 lần chạy cho 8-Queens
==================================================
  Thuật toán                        HC       SA
  ----------------------------------------------
  Tỉ lệ thành công (%):          43.3%    86.7%
  Số bước TB:                      8.2    523.1
  Số lần thành công:             13/30    26/30
```

---

## 🗂️ Cấu trúc chương trình

```
n_queens_solver.py
│
├── class NQueensSolver
│   ├── initial_board()            # Khởi tạo bàn cờ ngẫu nhiên
│   ├── calculate_conflicts()      # Hàm heuristic đếm số xung đột
│   ├── get_best_neighbor()        # Tìm láng giềng tốt nhất
│   │
│   ├── hill_climbing()            # HC cơ bản
│   ├── random_restart_hill_climbing()  # HC + Random Restart
│   │
│   ├── simulated_annealing()      # Thuật toán SA
│   │
│   ├── benchmark()                # So sánh thống kê HC vs SA
│   └── print_board()              # In bàn cờ trực quan
│
└── main()                         # Chạy thử nghiệm và so sánh
```

---

## 📈 Nhận xét so sánh

| Tiêu chí | Hill Climbing | Simulated Annealing |
|---|---|---|
| Tốc độ mỗi bước | Nhanh | Chậm hơn |
| Dễ bị local optimum | Có | Ít hơn |
| Tỉ lệ thành công (N=8) | ~40% | ~85% |
| Cần Random Restart | Có | Không bắt buộc |

> **Kết luận:** SA vượt trội hơn HC thuần túy về tỉ lệ thành công nhờ khả năng thoát khỏi local optimum. HC cần kết hợp Random Restart mới đảm bảo tìm ra nghiệm.
