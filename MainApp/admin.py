from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """ปรับปรุง Admin interface สำหรับ Person model"""
    
    # การแสดงผลในรายการ
    list_display = ['name', 'age', 'formatted_date', 'status_badge', 'updated_at']
    list_filter = ['is_active', 'age', 'date']
    search_fields = ['name']
    date_hierarchy = 'date'
    
    # การแก้ไข
    fields = ['name', 'age', 'is_active']
    readonly_fields = ['date', 'updated_at']
    
    # การเรียงลำดับ
    ordering = ['-date']
    
    # จำนวนรายการต่อหน้า
    list_per_page = 25
    
    # Actions
    actions = ['make_active', 'make_inactive']
    
    def formatted_date(self, obj):
        """แสดงวันที่ในรูปแบบที่อ่านง่าย"""
        return timezone.localtime(obj.date).strftime('%d/%m/%Y %H:%M')
    formatted_date.short_description = 'วันที่ลงทะเบียน'
    formatted_date.admin_order_field = 'date'
    
    def status_badge(self, obj):
        """แสดงสถานะในรูปแบบ badge"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success">ใช้งาน</span>'
            )
        return format_html(
            '<span class="badge badge-danger">ไม่ใช้งาน</span>'
        )
    status_badge.short_description = 'สถานะ'
    status_badge.admin_order_field = 'is_active'
    
    def make_active(self, request, queryset):
        """เปิดใช้งานข้อมูลที่เลือก"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'เปิดใช้งาน {updated} รายการ')
    make_active.short_description = 'เปิดใช้งานรายการที่เลือก'
    
    def make_inactive(self, request, queryset):
        """ปิดใช้งานข้อมูลที่เลือก"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'ปิดใช้งาน {updated} รายการ')
    make_inactive.short_description = 'ปิดใช้งานรายการที่เลือก'

# ปรับแต่ง Admin site header
admin.site.site_header = 'ระบบจัดการข้อมูลบุคคล'
admin.site.site_title = 'Admin Panel'
admin.site.index_title = 'ยินดีต้อนรับสู่ระบบจัดการข้อมูล'