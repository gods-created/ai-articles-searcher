from Crypto.PublicKey.RSA import generate
import os
from loguru import logger

def init() -> None:
    private_key_filename = 'private_key.pem'
    public_key_filename = 'public_key.pem'
    key = generate(2048)
    
    if not os.path.exists(private_key_filename):
        private_key = key.export_key()
        with open(private_key_filename, 'wb') as f:
            f.write(
                private_key
            )
    else:
        logger.warning(f'{private_key_filename} is already exist!')
    
    if not os.path.exists(public_key_filename):
        public_key = key.publickey().export_key()
        with open(public_key_filename, 'wb') as f:
            f.write(
                public_key
            )
    else:
        logger.warning(f'{public_key_filename} is already exist!')
