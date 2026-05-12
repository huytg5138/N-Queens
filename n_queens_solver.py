import random
import math
import time

class NQueensSolver:
    def __init__(self, n):
        self.n = n

    def initial_board(self): 
        """Khởi tạo bàn cờ ngẫu nhiên.
        Mảng 1 chiều: index là cột, giá trị là hàng của quân hậu."""
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    def calculate_conflicts(self, board):
        """Hàm Heuristic: Đếm số cặp hậu tấn công nhau (ngang, chéo)."""
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_best_neighbor(self, board):
        """Tìm láng giềng tốt nhất cho Hill Climbing.
        Shuffle cột để tránh bias, dừng sớm nếu tìm thấy nghiệm."""
        current_conflicts = self.calculate_conflicts(board)
        best_board = None
        best_conflicts = current_conflicts

        cols = list(range(self.n))
        random.shuffle(cols)  # Tránh bias về cột đầu

        for col in cols:
            for row in range(self.n):
                if board[col] == row:
                    continue
                neighbor = list(board)
                neighbor[col] = row
                c = self.calculate_conflicts(neighbor)
                if c < best_conflicts:
                    best_conflicts = c
                    best_board = list(neighbor)
                    if c == 0:
                        return best_board, best_conflicts  # Dừng sớm khi tìm thấy nghiệm

        return best_board, best_conflicts

    # ================= 1. THUẬT TOÁN HILL CLIMBING =================

    def hill_climbing(self, start_board):
        """Thuật toán Leo núi cơ bản (Dễ bị kẹt ở Local Minimum).
        Trả về: (board, conflicts, steps)"""
        current_board = list(start_board)
        current_conflicts = self.calculate_conflicts(current_board)
        steps = 0

        while True:
            # Tìm láng giềng tốt nhất
            best_neighbor, best_conflicts = self.get_best_neighbor(current_board)

            # Bị kẹt: không có láng giềng nào tốt hơn
            if best_neighbor is None:
                return current_board, current_conflicts, steps

            # Di chuyển sang láng giềng tốt hơn
            current_board = best_neighbor
            current_conflicts = best_conflicts
            steps += 1

            # Tìm thấy nghiệm
            if current_conflicts == 0:
                return current_board, current_conflicts, steps

    def random_restart_hill_climbing(self):
        """Hill Climbing có khởi động lại ngẫu nhiên khi bị kẹt.
        Trả về: (board, conflicts, total_steps, restarts)"""
        total_steps = 0
        restarts = 0

        while True:
            start_board = self.initial_board()
            final_board, conflicts, steps = self.hill_climbing(start_board)
            total_steps += steps

            if conflicts == 0:
                return final_board, conflicts, total_steps, restarts

            restarts += 1

   # ================= 2. THUẬT TOÁN SIMULATED ANNEALING =================

    def simulated_annealing(self, start_board=None, initial_temp=None, cooling_rate=None):
        """Thuật toán Tôi luyện giả lập.
        Tự động điều chỉnh nhiệt độ ban đầu theo kích thước N.
        Trả về: (board, conflicts, steps)"""
        current_board = list(start_board) if start_board else self.initial_board()
        current_conflicts = self.calculate_conflicts(current_board)

        # Tự động chỉnh nhiệt độ theo N nếu không truyền vào
        if initial_temp is None:
            initial_temp = self.n * self.n * 2.0

        temperature = initial_temp
        max_steps = int(initial_temp * self.n * 20)

        # Tự động tính cooling_rate sao cho nhiệt độ nguội vừa đủ trong max_steps bước
        if cooling_rate is None:
            cooling_rate = (0.01 / initial_temp) ** (1.0 / max_steps)

        steps = 0

        while temperature > 0.01 and current_conflicts > 0 and steps < max_steps:
            # Chọn ngẫu nhiên 1 láng giềng (nhanh hơn sinh tất cả)
            col = random.randint(0, self.n - 1)
            row = random.randint(0, self.n - 1)
            while row == current_board[col]:
                row = random.randint(0, self.n - 1)

            neighbor = list(current_board)
            neighbor[col] = row
            neighbor_conflicts = self.calculate_conflicts(neighbor)

            delta_e = neighbor_conflicts - current_conflicts

            # Chấp nhận nếu tốt hơn, hoặc tệ hơn nhưng vượt qua xác suất SA
            if delta_e < 0 or random.random() < math.exp(-delta_e / temperature):
                current_board = neighbor
                current_conflicts = neighbor_conflicts

            temperature *= cooling_rate
            steps += 1

        return current_board, current_conflicts, steps
    # ================= 3. BENCHMARK SO SÁNH =================

    def benchmark(self, runs=30):
        """Chạy nhiều lần để so sánh thống kê giữa HC và SA.
        Chỉ dùng HC đơn (không restart) để thấy rõ sự khác biệt."""
        print(f"\n{'='*50}")
        print(f"  BENCHMARK: {runs} lần chạy cho {self.n}-Queens")
        print(f"{'='*50}")

        hc_success = 0
        sa_success = 0
        hc_steps_list = []
        sa_steps_list = []

        for _ in range(runs):
            board = self.initial_board()

            # Hill Climbing đơn (không restart) — để thấy tỉ lệ thất bại
            _, conflicts, steps = self.hill_climbing(list(board))
            hc_steps_list.append(steps)
            if conflicts == 0:
                hc_success += 1

            # Simulated Annealing
            _, conflicts, steps = self.simulated_annealing(list(board))
            sa_steps_list.append(steps)
            if conflicts == 0:
                sa_success += 1

        hc_rate = hc_success / runs * 100
        sa_rate = sa_success / runs * 100
        hc_avg_steps = sum(hc_steps_list) / runs
        sa_avg_steps = sum(sa_steps_list) / runs

        print(f"\n  {'Thuật toán':<30} {'HC':>8} {'SA':>8}")
        print(f"  {'-'*46}")
        print(f"  {'Tỉ lệ thành công (%):':<30} {hc_rate:>7.1f}% {sa_rate:>7.1f}%")
        print(f"  {'Số bước TB:':<30} {hc_avg_steps:>8.1f} {sa_avg_steps:>8.1f}")
        print(f"  {'Số lần thành công:':<30} {hc_success:>7}/{runs} {sa_success:>5}/{runs}")
        print(f"\n  => SA vượt trội hơn HC thuần túy ở tỉ lệ thành công.")

    # ================= TIỆN ÍCH =================

    def print_board(self, board):
        """In bàn cờ ra màn hình một cách trực quan."""
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if board[col] == row:
                    line += "Q "
                else:
                    line += ". "
            print(line)
        print("-" * (self.n * 2))


# ================= MAIN =================
def main():
    N = 8  # Thay đổi N tại đây: 8, 16, 32...
    solver = NQueensSolver(N)

    print(f"{'='*50}")
    print(f"  BÀI TOÁN {N}-QUEENS")
    print(f"{'='*50}")

    # ---------------------------------------------------------
    # 1. Random-Restart Hill Climbing (luôn tìm ra nghiệm)
    # ---------------------------------------------------------
    print(f"\n[1] Random-Restart Hill Climbing")
    print(f"    (Leo núi + tự khởi động lại khi bị kẹt)")
    start_time = time.time()

    hc_board, hc_conflicts, hc_steps, hc_restarts = solver.random_restart_hill_climbing()

    hc_time = time.time() - start_time
    print(f"    -> Kết quả       : {'THÀNH CÔNG ✓' if hc_conflicts == 0 else 'THẤT BẠI ✗'}")
    print(f"    -> Số lỗi còn lại: {hc_conflicts}")
    print(f"    -> Tổng bước đi  : {hc_steps}")
    print(f"    -> Số lần restart: {hc_restarts}")
    print(f"    -> Thời gian     : {hc_time:.4f} giây")
    solver.print_board(hc_board)

    # ---------------------------------------------------------
    # 2. Simulated Annealing
    # ---------------------------------------------------------
    print(f"\n[2] Simulated Annealing")
    print(f"    (Tôi luyện giả lập)")
    sa_init_board = solver.initial_board()
    start_time = time.time()

    sa_board, sa_conflicts, sa_steps = solver.simulated_annealing(sa_init_board)

    sa_time = time.time() - start_time
    print(f"    -> Kết quả       : {'THÀNH CÔNG ✓' if sa_conflicts == 0 else 'THẤT BẠI ✗'}")
    print(f"    -> Số lỗi còn lại: {sa_conflicts}")
    print(f"    -> Số vòng lặp   : {sa_steps}")
    print(f"    -> Thời gian     : {sa_time:.4f} giây")

    if sa_conflicts > 0:
        print(f"    !! Chưa tìm thấy nghiệm. Thử tăng initial_temp hoặc giảm cooling_rate.")

    solver.print_board(sa_board)

    # ---------------------------------------------------------
    # 3. Benchmark so sánh HC vs SA
    # ---------------------------------------------------------
    solver.benchmark(runs=30)


if __name__ == "__main__":
    main()