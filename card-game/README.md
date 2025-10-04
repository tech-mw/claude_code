# High-Low Card Game

FastAPI（Python）と typescript（vue.js）を用いて作成したシンプルなハイ＆ローのカードゲームです。  
ローカル環境で API サーバーとフロントエンドを起動し、ブラウザからプレイできます。

---

## 必要な環境
- Node.js：v22.19.0
- Python：3.11.9（3.12 or 3.12系推奨）
  - 当初`3.13`では依存関係インストール時にエラーがでたためpyenvで3.11.9を指定しました
---

## セットアップと実行方法

### 1. バックエンドの準備
- 起動後、バックエンド API は http://localhost:8000 で待機
  - FastAPI の自動ドキュメント: http://localhost:8000/docs
```
$ cd backend

# python バージョン（3.11 or 3.12を推奨）
$ pyenv install 3.11.9
$ pyenv local 3.11.9

# 仮想環境作成
$ python3.11 -m venv .venv
$ source .venv/bin/activate

# 依存関係インストール
$ pip install -r requirements.txt

# サーバー起動
$ python main.py
```

### 2. フロントエンド
- `http://localhost:3000`でゲーム画面にアクセス
```
$ cd ../frontend

# 依存関係インストール
$ npm install

# 開発サーバー起動
$ npm run dev
```

## ゲームルール
- 現在のカードより「高い」か「低い」かを予想
- 正解するとスコア +10点、連続正解数もカウント 
- 同じ値は不正解扱い 
- デッキがなくなると自動でシャッフル