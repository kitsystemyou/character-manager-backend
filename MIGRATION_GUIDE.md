# Database Migration Guide

このガイドでは、ORM ベースのマイグレーションシステムを使用してデータベースを初期化する方法を説明します。

## 概要

従来の `initialize.sql` は MySQL 専用でしたが、ORM ベースのマイグレーションシステムにより、以下のデータベースで動作するようになりました：

- MySQL / MariaDB
- PostgreSQL
- SQLite
- その他 SQLAlchemy がサポートするデータベース

## 前提条件

```bash
pip install -r requirements.txt
```

必要なパッケージ：
- `flask-sqlalchemy`: ORM
- `flask-migrate`: マイグレーション管理
- `alembic`: マイグレーションエンジン

## 使用方法

### 1. データベースの準備

#### MySQL の場合

```bash
# Docker で MySQL を起動
docker run \
  --restart=always \
  --name charamane \
  -e MYSQL_ROOT_PASSWORD=pass \
  -e MYSQL_USER=user \
  -e MYSQL_PASSWORD=pass \
  -e TZ=Asia/Tokyo \
  -p 3308:3306 \
  -d mysql:8.0

# データベースを作成
mysql -h 127.0.0.1 --port 3308 -u root -ppass -e "CREATE DATABASE IF NOT EXISTS charamane CHARACTER SET utf8mb4;"
```

#### PostgreSQL の場合

```bash
docker run \
  --name charamane_pg \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_DB=charamane \
  -p 5432:5432 \
  -d postgres:15
```

#### SQLite の場合

```bash
# ファイルベースなので準備不要
# 環境変数で指定するだけ
export SQLALCHEMY_DATABASE_URI="sqlite:///charamane.db"
```

### 2. 環境変数の設定

#### MySQL の場合

```bash
export DB_USER=root
export DB_PASS=pass
export DB_HOST=127.0.0.1
export DB_PORT=3308
export DB_NAME=charamane
```

#### PostgreSQL の場合

```bash
export DB_USER=postgres
export DB_PASS=pass
export DB_HOST=127.0.0.1
export DB_PORT=5432
export DB_NAME=charamane

# PostgreSQL 用に接続文字列を変更
# __init__.py で以下のように変更:
# SQLALCHEMY_DATABASE_URI=f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
```

### 3. マイグレーションの実行

#### 方法 A: migrations_cli.py を使用（推奨）

```bash
# 初回のみ: マイグレーションディレクトリを初期化
python migrations_cli.py init

# モデルからマイグレーションを生成
python migrations_cli.py migrate "Initial schema"

# データベースにマイグレーションを適用
python migrations_cli.py upgrade
```

#### 方法 B: db.create_all() を使用（簡易版）

```python
from flaskr import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
```

### 4. マイグレーションの確認

```bash
# MySQL の場合
mysql -h 127.0.0.1 --port 3308 -u root -ppass charamane -e "SHOW TABLES;"

# PostgreSQL の場合
psql -h 127.0.0.1 -U postgres -d charamane -c "\dt"

# SQLite の場合
sqlite3 charamane.db ".tables"
```

## テーブル構造

マイグレーションにより以下のテーブルが作成されます：

### users
- `id` (CHAR(36), PRIMARY KEY): ユーザーID (UUID)
- `user_name` (VARCHAR(50), NOT NULL): ユーザー名
- `email` (VARCHAR(50), NOT NULL): メールアドレス
- `login_type` (VARCHAR(20), NOT NULL): ログイン種別
- `used_system` (VARCHAR(255), NULL): ゲームシステム利用実績
- `create_time` (DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- `update_time` (DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- `delete_time` (DATETIME, NULL)

### characters
- `id` (INT, PRIMARY KEY, AUTO_INCREMENT): キャラクターID
- `user_id` (CHAR(36), NOT NULL): ユーザーID
- `character_name` (VARCHAR(255), NOT NULL): PC名
- `player_name` (VARCHAR(20), NOT NULL): PL名
- `game_system` (VARCHAR(20), NOT NULL): ゲームシステム
- `prof_img_path` (VARCHAR(50), NULL): プロフ画像パス
- `tags` (VARCHAR(255), NULL): タグ
- `create_time` (DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- `update_time` (DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- `delete_time` (DATETIME, NULL)

### coc_meta_info
- `character_id` (INT, PRIMARY KEY, FOREIGN KEY → characters.id)
- `job`, `sex`, `age`, `height`, `weight` など (各種メタ情報)

### coc_status_parameters
- `character_id` (INT, PRIMARY KEY, FOREIGN KEY → characters.id)
- `str`, `con`, `pow`, `dex`, `app`, `size`, `inte`, `edu` など (ステータス)

### coc_skills
- `skill_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `character_id` (INT, NOT NULL, FOREIGN KEY → characters.id)
- `skill_name` (VARCHAR(50), NOT NULL)
- `job_point`, `concern_point`, `grow`, `other`, `skill_type` (スキル情報)

## トラブルシューティング

### エラー: "No module named 'MySQLdb'"

```bash
# MySQL クライアントライブラリをインストール
pip install mysqlclient

# または PyMySQL を使用
pip install pymysql
# __init__.py で: import pymysql; pymysql.install_as_MySQLdb()
```

### エラー: "Can't connect to MySQL server"

- データベースが起動しているか確認
- ホスト名、ポート番号が正しいか確認
- ファイアウォール設定を確認

### PostgreSQL で使用する場合

1. `requirements.txt` に `psycopg2-binary` を追加
2. `__init__.py` の接続文字列を変更:
   ```python
   SQLALCHEMY_DATABASE_URI=f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
   ```

## 従来の SQL ファイルとの比較

| 項目 | initialize.sql | ORM Migration |
|------|----------------|---------------|
| データベース | MySQL のみ | MySQL, PostgreSQL, SQLite など |
| 管理方法 | 手動 SQL | バージョン管理された Python コード |
| スキーマ変更 | SQL を手動編集 | モデル変更 → マイグレーション生成 |
| ロールバック | 手動 | `python migrations_cli.py downgrade` |
| テスト | 本番 DB が必要 | SQLite で簡単にテスト可能 |

## 推奨事項

1. **開発環境**: SQLite を使用して高速に開発
2. **テスト環境**: Docker で MySQL/PostgreSQL を使用
3. **本番環境**: マネージドデータベースサービスを使用
4. **マイグレーション**: Git でバージョン管理し、チームで共有

## 参考資料

- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
