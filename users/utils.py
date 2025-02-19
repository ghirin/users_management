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
