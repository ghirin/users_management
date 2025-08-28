from django import forms


from .models import CustomUser


from tinymce.widgets import TinyMCE

class MassMailForm(forms.Form):
    subject = forms.CharField(label='Тема', max_length=255)
    message = forms.CharField(label='Текст письма', widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    file = forms.FileField(label='Вложение', required=False)
    recipients = forms.MultipleChoiceField(
        label='Кому отправить',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = CustomUser.objects.exclude(email='').values_list('id', 'username', 'email')
        self.fields['recipients'].choices = [
            (str(u[0]), f"{u[1]} ({u[2]})") for u in users
        ]
