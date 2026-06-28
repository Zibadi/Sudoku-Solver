import time
import cv2
import numpy as np

start = time.time_ns()
grid = [
    [0, 0, 0, 0, 1, 0, 7, 2, 0],
    [0, 0, 3, 2, 7, 8, 0, 9, 0],
    [0, 5, 7, 0, 0, 0, 3, 0, 8],
    [0, 0, 0, 9, 6, 0, 0, 7, 1],
    [0, 0, 0, 0, 8, 2, 0, 6, 3],
    [1, 9, 6, 0, 0, 0, 0, 4, 2],
    [3, 0, 8, 0, 2, 9, 0, 0, 4],
    [0, 0, 9, 0, 5, 1, 0, 0, 0],
    [0, 6, 0, 7, 0, 3, 0, 8, 9],
]

solve_calls_count = 0
video = cv2.VideoWriter(
    "backtracking.mkv", cv2.VideoWriter_fourcc(*"X264"), 10, (540, 540)
)
current_y = current_x = 0


def print_grid():
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=" ")
        print()


def write_grid_frame_to_video():
    global grid
    global video

    frame = np.full((540, 540, 3), 255, np.uint8)

    cv2.rectangle(
        frame,
        (current_x * 60, current_y * 60),
        ((current_x + 1) * 60, (current_y + 1) * 60),
        (75, 255, 75),
        -1,
    )

    for i in range(10):
        if i % 3 == 0:
            thickness = 2
            color = (0, 0, 0)
        else:
            thickness = 1
            color = (200, 200, 200)
        cv2.line(frame, (i * 60, 0), (i * 60, 540), color, thickness)
        cv2.line(frame, (0, i * 60), (540, i * 60), color, thickness)

    for y in range(9):
        for x in range(9):
            if grid[y][x] != 0:
                cv2.putText(
                    frame,
                    str(grid[y][x]),
                    (x * 60 + 20, y * 60 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 0),
                    2,
                    cv2.LINE_AA,
                )
    video.write(frame)


def is_possible(y, x, n):
    global grid
    for i in range(9):
        if grid[y][i] == n:
            return False
    for i in range(9):
        if grid[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[y0 + i][x0 + j] == n:
                return False
    return True


def solve():
    global grid
    global solve_calls_count
    global current_y, current_x
    solve_calls_count += 1
    print(solve_calls_count)
    write_grid_frame_to_video()
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if is_possible(y, x, n):
                        current_y, current_x = y, x
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    print_grid()
    print(solve_calls_count)
    global start
    elapsed = (time.time_ns() - start) / 10**9
    print(elapsed, "s")
    video.release()
    exit()


solve()
