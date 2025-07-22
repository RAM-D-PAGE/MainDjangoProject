# 🌐 Deploy Django Project to PythonAnywhere

## ขั้นตอนการ Deploy

### 1. เตรียม PythonAnywhere Account
- สมัครสมาชิก PythonAnywhere (Free หรือ Paid)
- Login เข้าสู่ระบบ

### 2. Clone Repository จาก GitHub

เปิด **Bash Console** ใน PythonAnywhere และรันคำสั่ง:

```bash
# Clone repository
git clone https://github.com/RAM-D-PAGE/MainDjangoProject.git

# เข้าไปในโฟลเดอร์โปรเจค
cd MainDjangoProject
```

### 3. สร้าง Virtual Environment

```bash
# สร้าง virtual environment
python3.10 -m venv venv

# เปิดใช้งาน virtual environment
source venv/bin/activate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

### 4. ตั้งค่า Database

```bash
# Migrate database
python manage.py migrate

# สร้าง superuser (optional)
python manage.py createsuperuser
```

### 5. ตั้งค่า Web App ใน PythonAnywhere

1. ไปที่ **Web** tab ใน Dashboard
2. คลิก **Add a new web app**
3. เลือก **Manual configuration**
4. เลือก **Python 3.10**

### 6. กำหนดค่า Web App

#### WSGI Configuration File:
```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/MainDjangoProject'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'MainProject.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### Virtual Environment:
- Virtualenv: `/home/yourusername/MainDjangoProject/venv`

#### Static Files:
- URL: `/static/`
- Directory: `/home/yourusername/MainDjangoProject/static`

### 7. อัปเดต settings.py สำหรับ Production

เพิ่มใน `settings.py`:
```python
# PythonAnywhere settings
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Static files
STATIC_ROOT = '/home/yourusername/MainDjangoProject/static'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = '/home/yourusername/MainDjangoProject/media'
MEDIA_URL = '/media/'
```

### 8. Collect Static Files

```bash
python manage.py collectstatic
```

### 9. Reload Web App

- กลับไปที่ **Web** tab
- คลิก **Reload** web app

## 🔄 สำหรับการอัปเดตในอนาคต

```bash
# ใน Bash Console ของ PythonAnywhere
cd MainDjangoProject
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

จากนั้นกด **Reload** web app อีกครั้ง

## 🌐 URL ของเว็บไซต์

เว็บไซต์จะอยู่ที่: `https://yourusername.pythonanywhere.com`

(แทนที่ `yourusername` ด้วยชื่อผู้ใช้ PythonAnywhere ของคุณ)
