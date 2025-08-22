import os
import time
import pyzipper
from dotenv import load_dotenv
from io import BytesIO

def encrypt_file_to_zip(file_bytes, filename):
    """
    Архивирует и шифрует файл в zip с паролем из .env.
    Возвращает байты zip-архива.
    """
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    password = os.getenv('ZIP_PASSWORD')
    if not password:
        raise ValueError("ZIP_PASSWORD not found in environment")
    password = password.encode()

    safe_filename = os.path.basename(filename)
    zip_buffer = BytesIO()
    with pyzipper.AESZipFile(zip_buffer, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password)
        zf.setencryption(pyzipper.WZ_AES, nbits=256)
        zip_info = pyzipper.ZipInfo(safe_filename)
        zip_info.date_time = time.localtime(time.time())[:6]
        zf.writestr(safe_filename, file_bytes)
    zip_buffer.seek(0)
    return zip_buffer.read()
