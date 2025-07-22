from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils import timezone

class Person(models.Model):
    """Model สำหรับเก็บข้อมูลนักศึกษา - ปรับปรุงให้มีประสิทธิภาพสูงสุด"""
    
    # Field validations
    name_validator = RegexValidator(
        regex=r'^[ก-๙a-zA-Z\s\(\)0-9]+$',
        message='ชื่อต้องประกอบด้วยตัวอักษรไทย ภาษาอังกฤษ ตัวเลข วงเล็บ และช่องว่างเท่านั้น'
    )
    
    name = models.CharField(
        max_length=255,
        validators=[
            name_validator,
            MinLengthValidator(3, message='ชื่อต้องมีความยาวอย่างน้อย 3 ตัวอักษร')
        ],
        help_text='ชื่อ นามสกุล และรหัสนักศึกษา',
        db_index=True  # เพิ่ม index เพื่อประสิทธิภาพในการค้นหา
    )
    
    age = models.IntegerField(
        help_text='ชั้นปีการศึกษา',
        validators=[
            RegexValidator(
                regex=r'^[1-6]$',
                message='ชั้นปีต้องอยู่ระหว่าง 1-6'
            )
        ]
    )
    
    date = models.DateTimeField(
        auto_now_add=True,
        help_text='วันที่ลงทะเบียน',
        db_index=True  # เพิ่ม index สำหรับการเรียงลำดับ
    )
    
    # เพิ่ม field สำหรับการอัปเดต
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='วันที่อัปเดตล่าสุด'
    )
    
    # เพิ่ม field สำหรับสถานะ
    is_active = models.BooleanField(
        default=True,
        help_text='สถานะการใช้งาน'
    )
    
    class Meta:
        ordering = ['-date']  # เรียงลำดับตามวันที่ล่าสุดก่อน
        verbose_name = 'ข้อมูลนักศึกษา'
        verbose_name_plural = 'ข้อมูลนักศึกษาทั้งหมด'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['date']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_student_id(self):
        """ดึงรหัสนักศึกษาจากชื่อ"""
        import re
        match = re.search(r'\((\d{9})\)', self.name)
        return match.group(1) if match else None
    
    def get_full_name(self):
        """ดึงชื่อ-นามสกุลโดยไม่รวมรหัสนักศึกษา"""
        return self.name.split(' (')[0] if ' (' in self.name else self.name
    
    def get_year_display(self):
        """แสดงชั้นปีในรูปแบบที่อ่านง่าย"""
        year_map = {
            1: 'ปีที่ 1',
            2: 'ปีที่ 2', 
            3: 'ปีที่ 3',
            4: 'ปีที่ 4',
            5: 'ปีที่ 5',
            6: 'ปีที่ 6'
        }
        return year_map.get(self.age, f'ปีที่ {self.age}')
    
    @classmethod
    def get_active_students(cls):
        """ดึงรายชื่อนักศึกษาที่ยังใช้งานอยู่"""
        return cls.objects.filter(is_active=True)
    
    @classmethod
    def get_students_by_year(cls, year):
        """ดึงรายชื่อนักศึกษาตามชั้นปี"""
        return cls.objects.filter(age=year, is_active=True)
    
    def save(self, *args, **kwargs):
        """Override save method เพื่อเพิ่มการตรวจสอบข้อมูล"""
        # อัปเดตเวลาก่อนบันทึก
        if not self.pk:  # ถ้าเป็นการสร้างใหม่
            self.date = timezone.now()
        self.updated_at = timezone.now()
        
        super().save(*args, **kwargs)