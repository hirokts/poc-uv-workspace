# worker 側：SIGUSR1 を受けたら 1 回 job を走らせて結果をファイルに出す
#	•	worker プロセスは常駐
#	•	外から SIGUSR1 を送ると 1 回だけ job 実行
#	•	job の結果は /tmp/worker_result.txt に保存（読み取れる＝擬似的に「返す」）

from __future__ import annotations

import os
import signal
import time
from pathlib import Path

from libs import now_iso

_shutdown = False
_trigger = False

RESULT_PATH = Path(os.getenv("WORKER_RESULT_PATH", "/tmp/worker_result.txt"))


def _handle_shutdown(signum, _frame):
    global _shutdown
    _shutdown = True
    print(f"[worker] received shutdown signal {signum}")


def _handle_trigger(signum, _frame):
    global _trigger
    _trigger = True
    print(f"[worker] received trigger signal {signum} (will run one job)")


def run_once() -> str:
    # ダミー処理（後で Pub/Sub 1メッセージ処理に置き換え）
    start = now_iso()
    time.sleep(1)
    end = now_iso()
    return f"ok start={start} end={end}"


def main() -> None:
    # 停止
    signal.signal(signal.SIGTERM, _handle_shutdown)
    signal.signal(signal.SIGINT, _handle_shutdown)

    # トリガー（mac/linux なら SIGUSR1 が使える）
    signal.signal(signal.SIGUSR1, _handle_trigger)

    print("[worker] started (send SIGUSR1 to trigger one job)")

    # 起動時に結果ファイルを用意（任意）
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text("ready\n", encoding="utf-8")

    try:
        while not _shutdown:
            if _trigger:
                # フラグを先に落とす（連打に強くする）
                globals()["_trigger"] = False

                result = run_once()
                RESULT_PATH.write_text(result + "\n", encoding="utf-8")
                print(f"[worker] wrote result to {RESULT_PATH}: {result}")

            time.sleep(0.1)
    finally:
        print("[worker] stopped")


if __name__ == "__main__":
    main()
