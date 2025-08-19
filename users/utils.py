import pyzipper
import os
from dotenv import load_dotenv
def encrypt_file_to_zip(file_path, zip_path, arcname=None):
    """
    Архивирует и шифрует файл в zip с паролем из .env (ZIP_PASSWORD)
    file_path: путь к исходному файлу
    zip_path: путь к архиву
    arcname: имя файла внутри архива (по умолчанию — имя исходного файла)
    """
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    password = os.getenv('ZIP_PASSWORD', 'default_password').encode()
    with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password)
        zf.write(file_path, arcname=arcname or os.path.basename(file_path))
import openpyxl
from io import BytesIO

def generate_xlsx(users):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Users'

    headers = ['ID', 'Username', 'Email', 'First Name', 'Last Name']
    sheet.append(headers)

    for user in users:
        sheet.append([user.id, user.username, user.email, user.first_name, user.last_name])

    output = BytesIO()
    workbook.save(output)
    return output.getvalue()
