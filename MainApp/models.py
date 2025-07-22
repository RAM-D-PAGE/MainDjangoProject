from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from django.core.cache import cache
from django.db.models import Avg, Count, Q

class Person(models.Model):
    """Model สำหรับเก็บข้อมูลพนักงาน - ปรับปรุงให้มีประสิทธิภาพสูงสุด"""
    
    # Field validations - ปรับปรุงให้รองรับข้อมูลที่หลากหลายมากขึ้น
    name_validator = RegexValidator(
        regex=r'^[ก-๙a-zA-Z\s\(\)0-9\-\.\_]+$',
        message='ชื่อต้องประกอบด้วยตัวอักษรไทย ภาษาอังกฤษ ตัวเลข วงเล็บ ขีดกลาง จุด ขีดล่าง และช่องว่างเท่านั้น'
    )
    
    age_validator = RegexValidator(
        regex=r'^([1-9]|[1-9][0-9]|100)$',
        message='อายุต้องอยู่ระหว่าง 1-100 ปี'
    )
    
    name = models.CharField(
        max_length=255,
        validators=[
            name_validator,
            MinLengthValidator(3, message='ชื่อต้องมีความยาวอย่างน้อย 3 ตัวอักษร')
        ],
        help_text='ชื่อ นามสกุล และรหัสพนักงาน',
        db_index=True  # เพิ่ม index เพื่อประสิทธิภาพในการค้นหา
    )
    
    age = models.PositiveIntegerField(
        help_text='อายุ (1-100 ปี)',
        validators=[age_validator],
        db_index=True  # เพิ่ม index เพื่อการค้นหาที่เร็วขึ้น
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
        verbose_name = 'ข้อมูลพนักงาน'
        verbose_name_plural = 'ข้อมูลพนักงานทั้งหมด'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['date']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_student_id(self):
        """ดึงรหัสพนักงานจากชื่อ"""
        import re
        match = re.search(r'\((\d{9})\)', self.name)
        return match.group(1) if match else None
    
    def get_full_name(self):
        """ดึงชื่อ-นามสกุลโดยไม่รวมรหัสพนักงาน"""
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
        """ดึงรายชื่อพนักงานที่ยังใช้งานอยู่ - มี cache"""
        cache_key = 'active_employees'
        result = cache.get(cache_key)
        if result is None:
            result = list(cls.objects.filter(is_active=True).values('id', 'name', 'age'))
            cache.set(cache_key, result, 300)  # Cache 5 นาที
        return result
    
    @classmethod
    def get_statistics(cls):
        """ดึงสถิติข้อมูลพร้อม cache"""
        cache_key = 'person_statistics'
        result = cache.get(cache_key)
        if result is None:
            queryset = cls.objects.filter(is_active=True)
            result = {
                'total_count': queryset.count(),
                'avg_age': queryset.aggregate(avg_age=Avg('age'))['avg_age'] or 0,
                'age_distribution': dict(queryset.values('age').annotate(count=Count('age')).values_list('age', 'count'))
            }
            cache.set(cache_key, result, 600)  # Cache 10 นาที
        return result
    
    @classmethod
    def search_persons(cls, query):
        """ค้นหาข้อมูลแบบ full-text search"""
        if not query:
            return cls.objects.none()
        
        return cls.objects.filter(
            Q(name__icontains=query) | 
            Q(age__exact=query if query.isdigit() else None),
            is_active=True
        ).distinct()
    
    @classmethod
    def get_students_by_year(cls, year):
        """ดึงรายชื่อพนักงานตามอายุ - ปรับปรุงให้รองรับอายุ"""
        return cls.objects.filter(age=year, is_active=True).select_related()
    
    def save(self, *args, **kwargs):
        """Override save method เพื่อเพิ่มการตรวจสอบข้อมูลและ clear cache"""
        # อัปเดตเวลาก่อนบันทึก
        if not self.pk:  # ถ้าเป็นการสร้างใหม่
            self.date = timezone.now()
        self.updated_at = timezone.now()
        
        # Validate ข้อมูลก่อนบันทึก
        self.full_clean()
        
        super().save(*args, **kwargs)
        
        # Clear cache เมื่อมีการเปลี่ยนแปลง
        self.clear_cache()
    
    def delete(self, *args, **kwargs):
        """Override delete method เพื่อ clear cache"""
        super().delete(*args, **kwargs)
        self.clear_cache()
    
    @classmethod
    def clear_cache(cls):
        """ล้าง cache ที่เกี่ยวข้อง"""
        cache_keys = ['active_employees', 'person_statistics']
        cache.delete_many(cache_keys)