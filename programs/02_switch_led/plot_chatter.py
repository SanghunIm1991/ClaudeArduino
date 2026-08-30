"""capture_chatter_log.pyで取得したCSVから、生信号(R)とデバウンス後信号(D)を比較するSVGグラフを生成する。

生データ全体の概観と、実際にチャタリング（複数回の反転）が観測された区間の拡大図の2枚を出力する。

使い方: py -3.11 plot_chatter.py [入力CSV] [出力先ディレクトリ]
例:     py -3.11 plot_chatter.py chatter_log.csv .
"""

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "MS Gothic"


def load_events(path):
    raw = []
    deb = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) != 3:
                continue
            typ, us, val = row
            try:
                us = int(us)
                val = int(val)
            except ValueError:
                continue
            (raw if typ == "R" else deb).append((us, val))
    raw.sort()
    deb.sort()
    return raw, deb


def find_bounciest_run(raw, deb):
    """直近のD確定からD確定までの間にRが2回以上変化した区間のうち、最も反転回数が多いものを返す。"""
    events = sorted([(t, "R", v) for t, v in raw] + [(t, "D", v) for t, v in deb])
    runs = []
    run_r_times = []
    for t, typ, _v in events:
        if typ == "R":
            run_r_times.append(t)
        else:
            if len(run_r_times) >= 2:
                runs.append((run_r_times[0], t, len(run_r_times)))
            run_r_times = []
    if not runs:
        return None
    # 反転回数が多く、かつ短時間で収束している区間ほど典型的な接点バウンスとみなす
    return max(runs, key=lambda r: (r[2], -(r[1] - r[0])))


def value_before(events, t, default=0):
    v = default
    for et, ev in events:
        if et < t:
            v = ev
        else:
            break
    return v


def to_step_xy(events, t0, t1, initial):
    xs = [t0]
    ys = [initial]
    for t, v in events:
        if t0 <= t <= t1:
            xs.append(t)
            ys.append(v)
    return xs, ys


def plot_window(raw, deb, t0, t1, unit_div, xlabel, title, out_path):
    r_init = value_before(raw, t0)
    d_init = value_before(deb, t0)
    rx, ry = to_step_xy(raw, t0, t1, r_init)
    dx, dy = to_step_xy(deb, t0, t1, d_init)
    rx = [(x - t0) / unit_div for x in rx]
    dx = [(x - t0) / unit_div for x in dx]

    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.step(rx, ry, where="post", color="#d94f4f", linewidth=1.5, label="生信号 (digitalRead)")
    ax.step(dx, [v + 1.5 for v in dy], where="post", color="#2f6fb0", linewidth=1.5, label="デバウンス後信号")
    ax.set_xlim(0, (t1 - t0) / unit_div)
    ax.set_yticks([0, 1, 1.5, 2.5])
    ax.set_yticklabels(["LOW", "HIGH", "LOW", "HIGH"])
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, axis="x", linestyle=":", linewidth=0.5, alpha=0.6)
    fig.tight_layout()
    fig.savefig(out_path, format="svg")
    plt.close(fig)


def main():
    in_path = sys.argv[1] if len(sys.argv) > 1 else "chatter_log.csv"
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")

    raw, deb = load_events(in_path)
    if not raw and not deb:
        print("イベントが記録されていません。")
        return

    t0 = min(raw[0][0] if raw else deb[0][0], deb[0][0] if deb else raw[0][0])
    t1 = max(raw[-1][0] if raw else 0, deb[-1][0] if deb else 0)
    plot_window(
        raw, deb, t0, t1, 1_000_000, "経過時間 [s]",
        "スイッチ入力の生信号とデバウンス後信号（全体）",
        out_dir / "chatter_overview.svg",
    )
    print(f"raw events: {len(raw)}, debounced events: {len(deb)}")

    run = find_bounciest_run(raw, deb)
    if run is None:
        print("チャタリング（複数回反転）が観測された区間が見つかりませんでした。")
        return
    run_start, run_end, bounce_count = run
    pad = 15_000  # 15ms
    zt0 = run_start - pad
    zt1 = run_end + pad
    plot_window(
        raw, deb, zt0, zt1, 1_000, "経過時間 [ms]（区間先頭を0とする）",
        f"チャタリング拡大区間（生信号が{bounce_count}回反転→デバウンス後は1回に収束）",
        out_dir / "chatter_bounce_zoom.svg",
    )
    print(f"bounciest run: {bounce_count} raw transitions between {run_start}us and {run_end}us")


if __name__ == "__main__":
    main()
