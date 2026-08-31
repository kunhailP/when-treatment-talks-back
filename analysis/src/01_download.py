"""
DebateGPT 데이터 다운로드.

주의: Anthropic 클라우드 샌드박스에서는 huggingface.co가 차단됨(403).
이 스크립트는 로컬(네트워크 되는 곳)에서 실행하거나, 아래 수동 방법 사용:

  수동 다운로드: https://huggingface.co/datasets/frasalvi/debategpt
  -> Files 탭에서 csv/parquet 파일들을 받아 analysis/data/raw/ 에 저장

Usage: python 01_download.py [--out ../data/raw]
"""

import argparse
import os

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "data", "raw"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    from huggingface_hub import snapshot_download

    path = snapshot_download("frasalvi/debategpt", repo_type="dataset", local_dir=args.out)
    print("downloaded to", path)
    for root, _, files in os.walk(args.out):
        for f in files:
            print(os.path.join(root, f))
