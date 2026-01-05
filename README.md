# poc-uv-workspace

FastAPI API と Worker を **uv workspace** で管理するサンプル構成です。

- `api` : FastAPI サービス
- `worker` : 常駐 Worker（将来 Google Cloud Pub/Sub subscriber 想定）
- `libs` : API / Worker で共有する共通ライブラリ

uv / src レイアウト / Docker / docker compose を前提にしています。

---

## ディレクトリ構成

```
ws-test/
├─ pyproject.toml        # workspace root
├─ uv.lock
├─ docker-compose.yml
└─ packages/
├─ api/
│  ├─ Dockerfile
│  ├─ pyproject.toml
│  └─ src/api/
│     └─ main.py
├─ worker/
│  ├─ Dockerfile
│  ├─ pyproject.toml
│  └─ src/worker/
│     └─ main.py
└─ libs/
├─ pyproject.toml
└─ src/libs/
└─ init.py
```

---

## 設計方針

- **uv workspace**
  - `packages/*` を workspace メンバーとして管理
  - 依存解決・lock を 1 つに集約
- **src レイアウト**
- **役割分離**
  - `libs`：純粋な共通ロジック（FastAPI 依存なし）
  - `api`：FastAPI + uvicorn
  - `worker`：常駐処理（将来 Pub/Sub subscriber）

---

## ローカル実行（Docker）
Docker / docker compose

```bash
# ビルド & 起動
docker compose up --build

#	•	API: http://localhost:8000
#	•	Worker: バックグラウンドで常駐

# ログ確認

docker compose logs -f api
docker compose logs -f worker

# 停止（graceful shutdown）

docker compose down

```

---

## Worker について

- Worker は 常駐プロセスとして動作します。
- SIGTERM / SIGINT を受け取って graceful shutdown
- 現在はダミー処理

### workerの動作確認
シグナル送信（コンテナに）

```
docker compose kill -s SIGUSR1 worker
```

結果を見る（ホスト側）

```
cat tmp/worker_result.txt
```