import os
import pyzipper
from dotenv import load_dotenv
from io import BytesIO

def encrypt_file_to_zip(file_bytes, filename):
    """
    Архивирует и шифрует файл в zip с паролем из .env.
    Возвращает байты zip-архива.
    """
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    password = os.getenv('ZIP_PASSWORD', 'default_password').encode()
    zip_buffer = BytesIO()
    with pyzipper.AESZipFile(zip_buffer, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password)
        zf.writestr(filename, file_bytes)
    zip_buffer.seek(0)
    return zip_buffer.read()
