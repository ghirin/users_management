from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.core.mail import send_mass_mail
from django.contrib import messages
from .models import CustomUser
from .forms_massmail import MassMailForm

@login_required
@user_passes_test(lambda u: u.is_superuser)

def mass_mail(request):
    if request.method == 'POST':
        form = MassMailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient_ids = form.cleaned_data.get('recipients', [])
            if recipient_ids:
                users = CustomUser.objects.filter(id__in=recipient_ids).exclude(email='')
            else:
                users = CustomUser.objects.exclude(email='')
            emails = list(users.values_list('email', flat=True))
            if not emails:
                messages.error(request, 'Нет выбранных пользователей с email для рассылки.')
            else:
                datatuple = [(subject, message, None, [email]) for email in emails]
                send_mass_mail(datatuple, fail_silently=False)
                messages.success(request, f'Письма отправлены {len(emails)} пользователям.')
            return redirect('home')
    else:
        form = MassMailForm()
    users = CustomUser.objects.exclude(email='')
    return render(request, 'users/mass_mail.html', {'form': form, 'users': users})
