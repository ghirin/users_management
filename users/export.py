from django.http import HttpResponse
from .models import CustomUser
import pandas as pd

def export_users(request):
    users = CustomUser.objects.all()
    data = []
    for user in users:
        data.append({
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'plain_password': user.plain_password,
            'comment': user.comment,
            'password_expiration_date': user.password_expiration_date,
            'preferred_messenger': user.preferred_messenger,
            'locality': user.locality.name if user.locality else '',
        })
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=users_export.xlsx'
    df.to_excel(response, index=False, engine='openpyxl')
    return response
