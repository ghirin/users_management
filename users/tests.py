import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import CustomUser, UserFile
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import zipfile

@pytest.mark.django_db
def test_user_creation(client):
	user = CustomUser.objects.create_user(username='testuser', password='testpass', email='test@example.com', phone='(123)456-78-90')
	assert CustomUser.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_import_export(client, admin_client, tmp_path):
	# Экспорт
	url = reverse('export_users')
	response = admin_client.get(url)
	assert response.status_code == 200
	assert response['Content-Disposition'].startswith('attachment')
	# Импорт
	import pandas as pd
	df = pd.DataFrame([
		{'username': 'imported', 'email': 'imported@example.com', 'phone': '(111)222-33-44', 'comment': 'test', 'password_expiration_date': '2025-12-31'}
	])
	file_path = tmp_path / 'import.xlsx'
	df.to_excel(file_path, index=False, engine='openpyxl')
	with open(file_path, 'rb') as f:
		response = admin_client.post(reverse('import-users'), {'xlsx_file': f})
	assert CustomUser.objects.filter(username='imported').exists()

@pytest.mark.django_db
def test_file_upload_and_encryption(client, admin_user, tmp_path):
	client.force_login(admin_user)
	file_content = b'hello secret'
	file = SimpleUploadedFile('secret.txt', file_content)
	response = client.post(reverse('profile', args=[admin_user.id]), {'file': file})
	user_file = UserFile.objects.filter(user=admin_user).last()
	assert user_file is not None
	# Проверяем, что файл - zip
	with open(user_file.file.path, 'rb') as f:
		z = zipfile.ZipFile(io.BytesIO(f.read()))
		assert 'secret.txt' in z.namelist()
from django.test import TestCase

# Create your tests here.
