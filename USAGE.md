# การใช้งาน Django Person Management System

## การติดตั้งและเรียกใช้

### 1. เปิด Terminal/Command Prompt
```bash
cd "c:\MainFolder\Project\จารเกต\661320105\MainDjangoProject\MainProject"
```

### 2. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 3. เรียกใช้ Database Migrations
```bash
python manage.py migrate
```

### 4. เริ่มเซิร์ฟเวอร์
```bash
python manage.py runserver
```

### 5. เปิดเว็บไซต์
เปิดเบราว์เซอร์และไปที่: http://127.0.0.1:8000/

## การใช้งานระบบ

### หน้าหลัก (/)
- แสดงการนำทางไปยังหน้าต่างๆ
- ลิงก์ไปยังฟอร์มกรอกข้อมูลและดูข้อมูล

### ฟอร์มกรอกข้อมูล (/form/)
- กรอกชื่อ-นามสกุล และอายุ
- ระบบตรวจสอบความถูกต้องแบบ real-time
- บันทึกข้อมูลลงฐานข้อมูล

### รายการบุคคล (/person/)
- แสดงตารางข้อมูลบุคคลทั้งหมด
- ปุ่มแก้ไขและลบข้อมูล
- สถิติข้อมูล (จำนวนคน, อายุเฉลี่ย)

### การแก้ไขข้อมูล
1. คลิกปุ่มแก้ไข (สีส้ม) ในตาราง
2. ระบบจะนำไปยังฟอร์มพร้อมข้อมูลเดิม
3. แก้ไขข้อมูลและกดอัปเดต

### การลบข้อมูล
1. คลิกปุ่มลบ (สีแดง) ในตาราง
2. ยืนยันการลบในหน้าต่าง Modal
3. ข้อมูลจะถูกลบออกจากระบบ

## คุณสมบัติพิเศษ

- **Responsive Design**: ใช้งานได้บนมือถือและแท็บเล็ต
- **Real-time Validation**: ตรวจสอบข้อมูลขณะพิมพ์
- **Auto-refresh**: รีเฟรชข้อมูลอัตโนมัติ
- **Bootstrap UI**: ส่วนติดต่อผู้ใช้ที่สวยงาม
- **CSRF Protection**: ระบบความปลอดภัย

## การ Backup ข้อมูล

ไฟล์ `db.sqlite3` เก็บข้อมูลทั้งหมด สามารถคัดลอกเก็บไว้เป็น backup ได้

## หากมีปัญหา

1. ตรวจสอบว่าติดตั้ง Django แล้ว: `python -m django --version`
2. ตรวจสอบว่าอยู่ในโฟลเดอร์ที่ถูกต้อง
3. ตรวจสอบว่า port 8000 ไม่ถูกใช้งานโดยโปรแกรมอื่น

## วิธีอัปโหลดไปยัง GitHub

### 1. สร้าง Repository ใหม่บน GitHub
1. ไปที่ https://github.com/
2. คลิก "New repository"
3. ตั้งชื่อ repository เช่น "django-person-management"
4. เลือก "Public" หรือ "Private"
5. **ไม่ต้อง** เลือก "Initialize with README"
6. คลิก "Create repository"

### 2. เชื่อมต่อกับ GitHub
```bash
# เพิ่ม remote repository
git remote add origin https://github.com/USERPrime/django-person-management.git

# Push ไฟล์ขึ้น GitHub
git branch -M main
git push -u origin main
```

### 3. การอัปเดตครั้งต่อไป
```bash
git add .
git commit -m "Update: รายละเอียดการเปลี่ยนแปลง"
git push
```

## ลิงก์ที่เป็นประโยชน์

- **GitHub Repository**: https://github.com/USERPrime/django-person-management
- **Django Documentation**: https://docs.djangoproject.com/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/
