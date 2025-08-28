from django.contrib import admin
from .models import CustomUser, UserFile, Locality
from .forms import CustomUserChangeForm
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django import forms
import pandas as pd
from .export import export_users


class UserFileInline(admin.TabularInline):
    model = UserFile
    extra = 1

# Вернуть админ-настройки в CustomUserAdmin
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        'username', 'email', 'phone', 'locality', 'plain_password_display', 'password_expiration_date',
        'preferred_messenger', 'is_active', 'is_staff', 'is_superuser',
        'last_login', 'date_joined'
    )

    @admin.display(description='Пароль (открытый текст)')
    def plain_password_display(self, obj):
        return obj.plain_password or ''
    list_filter = (
        'locality', 'is_active', 'is_staff', 'is_superuser',
        'preferred_messenger', 'password_expiration_date'
    )
    class Media:
        css = {
            'all': ('admin/css/filters_collapse.css',)
        }
        js = ('admin/js/filters_collapse.js',)

    # Удалены кастомные list_display, search_fields, list_filter и open_password для полной стандартизации
    # Удалены кастомные fieldsets и inlines для полной стандартизации формы

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-users/', self.admin_site.admin_view(self.import_users_view), name='import-users'),
            path('export-users/', self.admin_site.admin_view(self.export_users_view), name='export-users'),
            path('view-events-log/', self.admin_site.admin_view(self.view_events_log), name='view-events-log'),
        ]
        return custom_urls + urls

    def view_events_log(self, request):
        import os
        from django.conf import settings
        log_path = os.path.join(settings.BASE_DIR, 'events.log')
        try:
            with open(log_path, encoding='utf-8') as f:
                log_content = f.read()
        except Exception:
            log_content = ''
        context = dict(self.admin_site.each_context(request))
        context['log_content'] = log_content
        return TemplateResponse(request, "admin/users/customuser/view_events_log.html", context)

    def import_users_view(self, request):
        if request.method == 'POST' and request.FILES.get('xlsx_file'):
            try:
                df = pd.read_excel(request.FILES['xlsx_file'], engine='openpyxl')
                for index, row in df.iterrows():
                    # Привести дату к строке YYYY-MM-DD
                    date_val = row['password_expiration_date']
                    if hasattr(date_val, 'strftime'):
                        date_str = date_val.strftime('%Y-%m-%d')
                    else:
                        date_str = str(date_val).split()[0]
                    locality_name = row.get('locality', '').strip()
                    locality = None
                    if locality_name:
                        locality, _ = Locality.objects.get_or_create(name=locality_name)
                    user, created = CustomUser.objects.get_or_create(username=row['username'])
                    user.email = row.get('email', '')
                    user.phone = row.get('phone', '')
                    user.plain_password = row.get('plain_password', '')
                    user.comment = row.get('comment', '')
                    from datetime import datetime
                    try:
                        user.password_expiration_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    except Exception:
                        pass  # не обновлять поле, если дата некорректна
                    user.locality = locality
                    user.save()
                self.message_user(request, "Пользователи успешно импортированы и обновлены.", level=messages.SUCCESS)
                return HttpResponseRedirect("../")
            except Exception as e:
                self.message_user(request, f"Ошибка при импорте: {e}", level=messages.ERROR)
        context = dict(self.admin_site.each_context(request))
        return TemplateResponse(request, "admin/users/customuser/import_users.html", context)

    def export_users_view(self, request):
        return export_users(request)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserFile)
admin.site.register(Locality)
