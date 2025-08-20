from pathlib import Path

_env_ = 'dev' # dev or prod
db_path = Path(__file__).parent / f'app_{_env_}.db'