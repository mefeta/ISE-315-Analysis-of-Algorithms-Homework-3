from __future__ import annotations
import argparse
import time
from typing import List, Tuple


INF = 10**18


def dp_change(coins: List[int], V: int) -> Tuple[int, List[int]]:
    if V < 0:
        raise ValueError("V must be non-negative.")
    if not coins:
        raise ValueError("Coin list cannot be empty.")
    if any(c <= 0 for c in coins):
        raise ValueError("All coin denominations must be positive integers.")

    coins = sorted(set(coins))

    opt = [INF] * (V + 1)
    parent = [-1] * (V + 1)

    opt[0] = 0
    parent[0] = 0

    for v in range(1, V + 1):
        best_count = INF
        best_coin = -1
        for c in coins:
            if c <= v and opt[v - c] + 1 < best_count:
                best_count = opt[v - c] + 1
                best_coin = c
        opt[v] = best_count
        parent[v] = best_coin

    if opt[V] >= INF or parent[V] == -1:
        raise ValueError(f"No solution found for V={V} with coins={coins}")

    used = []
    cur = V
    while cur > 0:
        c = parent[cur]
        if c == -1:
            raise RuntimeError("Reconstruction failed (parent pointer missing).")
        used.append(c)
        cur -= c

    return opt[V], used


def greedy_largest_first(coins: List[int], V: int) -> Tuple[int, List[int]]:
    """Greedy Strategy 1: always take largest coin <= remaining."""
    coins = sorted(coins, reverse=True)
    rem = V
    used = []
    for c in coins:
        while c <= rem:
            used.append(c)
            rem -= c
    return len(used), used


def run_single_case(coins: List[int], V: int) -> None:
    g_cnt, g_used = greedy_largest_first(coins, V)
    d_cnt, d_used = dp_change(coins, V)

    print(f"Coins: {sorted(coins)}")
    print(f"Target V: {V}")
    print("-" * 48)
    print(f"Greedy (Largest First): count={g_cnt}, coins={g_used}")
    print(f"DP Optimal:             count={d_cnt}, coins={d_used}")
    print()


def benchmark_dp(coins: List[int], V: int, reps: int = 7) -> None:
    times = []
    for _ in range(reps):
        t0 = time.perf_counter()
        dp_change(coins, V)
        times.append(time.perf_counter() - t0)

    avg = sum(times) / len(times)
    print(f"DP benchmark for V={V} (reps={reps})")
    print(f"avg={avg:.6f}s  min={min(times):.6f}s  max={max(times):.6f}s")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="HW3 DP Change-Making")
    parser.add_argument("--coins", type=str, default="25,10,1",
                        help="Comma-separated coin denominations, e.g. 25,10,1")
    parser.add_argument("--V", type=int, default=30, help="Target value V")
    parser.add_argument("--bench", action="store_true",
                        help="Also benchmark DP for V=10000")
    args = parser.parse_args()

    coins = [int(x.strip()) for x in args.coins.split(",") if x.strip()]

    run_single_case(coins, args.V)

    if args.bench:
        benchmark_dp(coins, 10_000)


if __name__ == "__main__":
    main()
