# mjerapp

## ローカル開発サーバーの起動

以下のコマンドは、ワークスペースのルート (`/workspace`) で実行します。現在地は `pwd` で確認できます。

```bash
pwd
```

出力が `/workspace` でなければ、次のコマンドで移動して確認してください。

```bash
cd /workspace
pwd
```

### 初回起動

仮想環境を有効化し、Djangoをインストールしてからサーバーを起動します。

```bash
source .venv/bin/activate
python -m pip install 'Django>=5.2,<6' 'psycopg[binary]' weasyprint 'qrcode[pil]'
DJANGO_SETTINGS_MODULE=mjerapp.settings python manage.py runserver
```

パッケージのインストールは、この仮想環境に対して一度実行すれば、通常は次回以降不要です。

### 通常起動

Djangoをインストール済みの場合は、毎回以下のコマンドで起動できます。`pip install` は不要です。

```bash
source .venv/bin/activate
DJANGO_SETTINGS_MODULE=mjerapp.settings python manage.py runserver
```

起動後、ブラウザーで `http://127.0.0.1:8000/` を開きます。開発サーバーを停止するには、起動したターミナルで `Ctrl+C` を押します。

## エラーの原因と確認

- `No module named 'django'`: 現在有効な Python 環境にDjangoがありません。仮想環境を有効化してから、初回起動のインストールコマンドを実行します。
- `No module named 'psycopg'` / `No module named 'psycopg2'`: PostgreSQL用のPythonドライバーがありません。`python -m pip install 'psycopg[binary]'` を実行します。
- `No module named 'weasyprint'`: PDF出力で使うWeasyPrintがありません。`python -m pip install weasyprint` を実行します。
- `PostgreSQL 15 or later is required (found 14.2)`: Django 6系はPostgreSQL 15以上が必要です。このプロジェクトでは既存DBを変更せずに使えるよう、PostgreSQL 14に対応するDjango 5.2系をインストールします。
- `No module named 'scoringsheets'`: Django の設定モジュールに、現在のプロジェクトにはない `scoringsheets.settings.dev` が指定されています。このプロジェクトの設定は `mjerapp.settings` です。上記の起動コマンドは設定を明示して実行します。

以前の起動案内にある `scoringsheets.settings.dev` は、このワークスペースの構成と一致しません。IDE のデバッグ設定など別の起動方法を使う場合も、設定モジュールを `mjerapp.settings` にしてください。