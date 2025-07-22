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

## 🔄 การอัปเดตโปรเจคจาก GitHub ไป PythonAnywhere

### วิธีที่ 1: อัปเดตโปรเจคที่มีอยู่แล้ว

เปิด **Bash Console** ใน PythonAnywhere และรันคำสั่งต่อไปนี้:

```bash
# เข้าไปในโฟลเดอร์โปรเจค
cd MainDjangoProject

# ดึงการอัปเดตล่าสุดจาก GitHub
git pull origin main

# เปิดใช้งาน virtual environment
source venv/bin/activate

# อัปเดต dependencies (หากมีการเปลี่ยนแปลง)
pip install -r requirements.txt

# อัปเดต database (หากมี migration ใหม่)
python manage.py migrate

# รวบรวมไฟล์ static ใหม่
python manage.py collectstatic --noinput

# ตรวจสอบว่าทุกอย่างทำงานได้
python manage.py check
```

### วิธีที่ 2: หากมีปัญหากับ git pull

```bash
# ตรวจสอบสถานะ git
cd MainDjangoProject
git status

# หากมีไฟล์ที่ถูกแก้ไขใน server
git stash  # เก็บการเปลี่ยนแปลงชั่วคราว
git pull origin main
git stash pop  # นำการเปลี่ยนแปลงกลับมา

# หรือถ้าต้องการเขียนทับ (ระวัง: จะเสียข้อมูลใน server)
git reset --hard HEAD
git pull origin main
```

### วิธีที่ 3: Clone ใหม่ทั้งหมด (หากมีปัญหามาก)

```bash
# ลบโฟลเดอร์เก่า (ระวัง: จะเสียข้อมูลทั้งหมด)
rm -rf MainDjangoProject

# Clone ใหม่
git clone https://github.com/RAM-D-PAGE/MainDjangoProject.git

# ตั้งค่าใหม่ตั้งแต่ต้น (ตามขั้นตอนที่ 3-8 ข้างต้น)
```

### ⚠️ สำคัญ: หลังจากอัปเดตเสร็จแล้ว

1. ไปที่ **Web** tab ใน PythonAnywhere Dashboard
2. คลิก **Reload** web app
3. ตรวจสอบเว็บไซต์ว่าทำงานปกติ

### 🔍 การตรวจสอบปัญหา

หากเว็บไซต์ไม่ทำงาน ให้ตรวจสอบ:

```bash
# ดู error logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# ตรวจสอบ settings
python manage.py check --settings=MainProject.settings

# ทดสอบการทำงานของ Django
python manage.py runserver
```

## 🌐 URL ของเว็บไซต์

เว็บไซต์จะอยู่ที่: `https://yourusername.pythonanywhere.com`

(แทนที่ `yourusername` ด้วยชื่อผู้ใช้ PythonAnywhere ของคุณ)

## 🚨 แก้ไขปัญหาทั่วไป

### ปัญหา: เว็บไซต์ไม่ทำงานหลังอัปเดต

1. **ตรวจสอบ Error Logs**:
```bash
# ดู error logs แบบ real-time
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# ดู error logs ล่าสุด
tail -50 /var/log/yourusername.pythonanywhere.com.error.log
```

2. **ตรวจสอบ WSGI Configuration**:
- ไปที่ **Web** tab
- คลิก **WSGI configuration file**
- ตรวจสอบ path ให้ถูกต้อง

3. **ตรวจสอบ Virtual Environment**:
- ไปที่ **Web** tab
- ตรวจสอบ Virtualenv path: `/home/yourusername/MainDjangoProject/venv`

### ปัญหา: Static Files ไม่แสดง

```bash
# Collect static files ใหม่
cd MainDjangoProject
source venv/bin/activate
python manage.py collectstatic --clear --noinput
```

### ปัญหา: Database Error

```bash
# ตรวจสอบและแก้ไข database
cd MainDjangoProject
source venv/bin/activate
python manage.py check
python manage.py migrate
```

### การ Debug แบบละเอียด

1. **เปิด DEBUG mode ชั่วคราว**:
   - แก้ไข `settings.py`: `DEBUG = True`
   - Reload web app
   - ดูข้อผิดพลาดบนเว็บไซต์
   - **อย่าลืมปิด DEBUG** หลังแก้ไขเสร็จ

2. **ทดสอบใน Console**:
```bash
cd MainDjangoProject
source venv/bin/activate
python manage.py shell

# ใน Django shell
from django.conf import settings
print(settings.ALLOWED_HOSTS)
print(settings.STATIC_ROOT)
```
