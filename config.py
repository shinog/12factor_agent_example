# config.py
from dotenv import load_dotenv
import os

# .envファイルを読み込む
load_dotenv()

# OpenAI APIキーとモデル名を環境変数から取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

