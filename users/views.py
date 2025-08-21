def my_profile(request):
    user = request.user
    files = UserFile.objects.filter(user=user)
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        zip_bytes = encrypt_file_to_zip(file.read(), file.name)
        from django.core.files.base import ContentFile
        zip_filename = file.name + '.zip'
        UserFile.objects.create(user=user, file=ContentFile(zip_bytes, name=zip_filename))
    return render(request, 'users/profile.html', {'user': user, 'files': files})
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser, UserFile, User
from .zip_utils import encrypt_file_to_zip
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

@login_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Пользователь успешно создан.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/create_user.html', {'form': form})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Пользователь успешно удален.")
        return redirect('home')  # Перенаправление на страницу со списком пользователей или главную
    
    return render(request, 'users/delete_user.html', {'user': user})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            # Обновить plain_password и пароль, если поле заполнено
            plain_password = form.cleaned_data.get('plain_password')
            if plain_password:
                updated_user.plain_password = plain_password
                updated_user.set_password(plain_password)
            updated_user.save()
            messages.success(request, "Пользователь успешно обновлен.")
            return redirect('profile', user_id=user.pk)
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Пользователь успешно создан.")
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# @login_required
# def home(request):
#         # Получаем всех пользователей
#     users = CustomUser.objects.all()
    
#     # Передаем список пользователей в шаблон
#     return render(request, 'home.html', {'users': users})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def user_list(request):
    query = request.GET.get('q', '')  # Получаем строку поиска из параметров GET-запроса
    view_type = request.GET.get('view', 'tiles')
    User = get_user_model()  # Используем get_user_model() для получения текущей модели пользователя
    users = User.objects.all()

    if query:
        users = users.filter(username__icontains=query)  # Фильтрация по имени пользователя, нечувствительному к регистру

    sort_by = request.GET.get('sort_by', 'username')
    order = request.GET.get('order', 'asc')
    allowed_sort_fields = ['username', 'comment', 'plain_password', 'password_expiration_date']
    if sort_by not in allowed_sort_fields:
        sort_by = 'username'
    if order == 'desc':
        users = users.order_by(f'-{sort_by}')
    else:
        users = users.order_by(sort_by)
    context = {
        'users': users,
        'query': query,
        'view_type': view_type,
        'sort_by': sort_by,
        'order': order,
    }
    return render(request, 'users/user_list.html', context)

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    files = UserFile.objects.filter(user=user)
    
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        # Архивируем и шифруем файл
        zip_bytes = encrypt_file_to_zip(file.read(), file.name)
        from django.core.files.base import ContentFile
        zip_filename = file.name + '.zip'
        UserFile.objects.create(user=user, file=ContentFile(zip_bytes, name=zip_filename))
    return redirect('user_profile', user_id=user.pk)
    
    return render(request, 'users/profile.html', {'user': user, 'files': files})

@login_required
def profile(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')
    user = get_object_or_404(User, id=user_id)
    files = UserFile.objects.filter(user=user)
    context = {
        'user': user,
        'files': files,
    }
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        zip_bytes = encrypt_file_to_zip(file.read(), file.name)
        from django.core.files.base import ContentFile
        zip_filename = file.name + '.zip'
        UserFile.objects.create(user=user, file=ContentFile(zip_bytes, name=zip_filename))
    
    return render(request, 'users/profile.html', {'user': user, 'files': files})

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id)
    user_id = file.user.pk  # Get the user_id before deleting the file
    file.delete()
    return redirect('user_profile', user_id=user_id)

@login_required
def home(request):
    sort_by = request.GET.get('sort_by', 'username')
    order = request.GET.get('order', 'asc')
    if order == 'asc':
        users = User.objects.all().order_by(sort_by)
    else:
        users = User.objects.all().order_by(f'-{sort_by}')
    context = {
        'users': users,
        'sort_by': sort_by,
        'order': order,
    }
    return render(request, 'home.html', context)

@login_required
def import_users(request):
    if request.method == 'POST':
        xlsx_file = request.FILES['xlsx_file']
        try:
            df = pd.read_excel(xlsx_file, engine='openpyxl')
            for index, row in df.iterrows():
                if not CustomUser.objects.filter(username=row['username']).exists():
                    date_val = row['password_expiration_date']
                    if hasattr(date_val, 'strftime'):
                        date_str = date_val.strftime('%Y-%m-%d')
                    else:
                        date_str = str(date_val).split()[0]
                    # plain_password: всегда строка, без .0 если это float
                    raw_pass = row.get('plain_password', '')
                    if isinstance(raw_pass, float):
                        if raw_pass.is_integer():
                            raw_pass = str(int(raw_pass))
                        else:
                            raw_pass = str(raw_pass)
                    else:
                        raw_pass = str(raw_pass)
                    # Преобразовать телефон к формату (098)518-43-22
                    raw_phone = str(row.get('phone', '')).strip()
                    phone = raw_phone
                    if raw_phone.isdigit() and len(raw_phone) == 9:
                        phone = f"(0{raw_phone[:2]}){raw_phone[2:5]}-{raw_phone[5:7]}-{raw_phone[7:]}"
                    elif raw_phone.isdigit() and len(raw_phone) == 10:
                        phone = f"({raw_phone[:3]}){raw_phone[3:6]}-{raw_phone[6:8]}-{raw_phone[8:]}"
                    CustomUser.objects.create(
                        username=row['username'],
                        email=row.get('email', ''),
                        phone=phone,
                        plain_password=raw_pass,
                        comment=row.get('comment', ''),
                        password_expiration_date=date_str,
                        preferred_messenger=row.get('preferred_messenger', ''),
                    )
                else:
                    messages.warning(request, f'Пользователь с именем {row["username"]} уже существует.')
            messages.success(request, 'Пользователи успешно импортированы.')
        except Exception as e:
            messages.error(request, f'Ошибка при импорте пользователей: {e}')
        return redirect('import_users')
    return render(request, 'users/import_users.html')