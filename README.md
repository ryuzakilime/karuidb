# Karui（軽い）

パイプラインで直感的につなぐ、SQLite向けの超軽量クエリ言語・変換エンジン。

---

## 概要

**Karui** は、「いちばん楽にクエリを書く」ことを目指して設計された超軽量クエリツールです。
データの保存や検索処理自体はすべて SQLite に任せ、独自のパイプライン記法を SQL に変換して実行します。

Python の標準ライブラリ（`re`, `sqlite3`, `sys`）のみで動作するため、**追加のライブラリやツールのインストールは一切不要**です。単一ファイル（約90行）で完結しています。

```bash
from users | where age > 20 | select name, age | sort age desc | take 3
```
↓ 次のSQLに自動変換されて実行されます。
```sql
SELECT name, age FROM users WHERE (age > 20) ORDER BY age DESC LIMIT 3
```

---

## 特徴

- **ゼロ依存**: Python 3 があればどこでも即座に動作。
- **直感的なパイプライン記法**: `|` で条件やソートを左から右へつなげて記述。
- **REPL対応**: 対話型シェルで手軽にデータ操作や変換確認が可能。
- **SQL混在可能**: `from` で始まらない行（`CREATE TABLE`, `INSERT` 等）は通常のSQLとしてそのまま実行。
- **変換プレビュー**: 先頭に `?` を付けると、実行せずに変換後のSQLを確認可能。

---

## 使えるコマンド一覧

| コマンド | 説明 | 例 |
| :--- | :--- | :--- |
| `from <テーブル名>` | 対象テーブルを指定（必須） | `from users` |
| `where <条件>` | 抽出条件を指定（複数指定時は `AND` で結合） | `where age >= 20` |
| `select <列名>` | 取得列を指定（省略時は `*`） | `select name, age` |
| `group <列名>` | 集計・グループ化の単位 | `group city` |
| `sort <並び順>` | ソート順を指定 | `sort age desc` |
| `take <件数>` | 取得件数の上限（LIMIT） | `take 5` |

---

## クイックスタート

### 1. 起動

```bash
# インメモリDBで手軽に試す場合
python3 karui.py

# ファイルにデータを保存・永続化する場合
python3 karui.py mydata.db
```

### 2. 対話モードでの実行例

起動後、以下のコマンドを順に入力してください：

```sql
karui> CREATE TABLE users(name TEXT, age INT, city TEXT)
karui> INSERT INTO users VALUES ('佐藤', 25, '東京'), ('鈴木', 19, '大阪'), ('高橋', 32, '東京')
karui> from users | where age > 20 | select name, age | sort age desc
name | age
高橋 | 32
佐藤 | 25
```

### 3. 変換後のSQLだけを確認したい場合

先頭に `?` を付けて入力します：

```sql
karui> ? from users | where age > 20 | select name, age | sort age desc | take 3
SELECT name, age FROM users WHERE (age > 20) ORDER BY age desc LIMIT 3
```

---

## ライセンス

MIT License
