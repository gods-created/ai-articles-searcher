from create_db import init as create_db
from create_secrets import init as create_secrets
from typing import Callable

def main() -> Callable[..., None]:
    return create_db(), create_secrets()

if __name__ == '__main__':
    main()
