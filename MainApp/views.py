# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.html import escape
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Python imports
import logging
import re

# Local imports
from .models import Person

# Set up logging
logger = logging.getLogger(__name__)

# =============================================================================
# Main Views
# =============================================================================

def about(request):
    """หน้าเกี่ยวกับ"""
    return render(request, 'about.html')


# =============================================================================
# Person Management Views
# =============================================================================

def person(request):
    """หน้าแสดงรายการบุคคล - ปรับปรุงประสิทธิภาพด้วย pagination และ search"""
    try:
        # รับพารามิเตอร์การค้นหา
        search_query = request.GET.get('search', '').strip()
        page_number = request.GET.get('page', 1)
        
        # ดึงข้อมูลพร้อม search
        if search_query:
            all_persons = Person.search_persons(search_query)
        else:
            all_persons = Person.objects.filter(is_active=True).order_by('-date')
        
        # Pagination
        paginator = Paginator(all_persons, 10)  # 10 รายการต่อหน้า
        try:
            persons_page = paginator.page(page_number)
        except PageNotAnInteger:
            persons_page = paginator.page(1)
        except EmptyPage:
            persons_page = paginator.page(paginator.num_pages)
        
        # ใช้ cache สำหรับสถิติ
        stats = Person.get_statistics()
        
        context = {
            'persons': persons_page,
            'search_query': search_query,
            'total_count': stats['total_count'],
            'avg_age': round(stats['avg_age'], 1),
            'age_distribution': stats['age_distribution'],
            'has_persons': stats['total_count'] > 0,
            'today': timezone.now().date(),
        }
        
        logger.info(f"Person list displayed. Total: {stats['total_count']}, Search: '{search_query}'")
        return render(request, 'person.html', context)
        
    except Exception as e:
        logger.error(f"Error in person view: {str(e)}")
        messages.error(request, 'เกิดข้อผิดพลาดในการโหลดข้อมูล')
        return render(request, 'person.html', {'persons': [], 'total_count': 0, 'avg_age': 0})

def about(request):
    return render(request, 'about.html')

@csrf_protect
def from_view(request):
    # เตรียมข้อมูลสำหรับ template
    context = {
        'total_persons': Person.objects.count(),
        'today': timezone.now().date(),
        'edit_mode': False,
        'edit_data': {},
        'edit_id': None,
    }
    
    # ตรวจสอบโหมดแก้ไข
    edit_id = request.GET.get('edit')
    if edit_id:
        try:
            person = Person.objects.get(id=edit_id)
            context.update({
                'edit_mode': True,
                'edit_data': {
                    'name': person.name,
                    'age': person.age,
                },
                'edit_id': edit_id,
            })
        except Person.DoesNotExist:
            messages.error(request, 'ไม่พบข้อมูลที่ต้องการแก้ไข')
    
    if request.method == 'POST':
        try:
            # รับข้อมูลจากฟอร์ม
            name = escape(request.POST.get('name', '').strip())
            age = request.POST.get('age', '').strip()
            edit_id = request.POST.get('edit_id')
            
            # ตรวจสอบข้อมูลที่จำเป็น
            if not name or not age:
                messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
                return render(request, 'from_view.html', context)
            
            # ตรวจสอบอายุ
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 100:
                    messages.error(request, 'อายุต้องอยู่ระหว่าง 1-100 ปี')
                    return render(request, 'from_view.html', context)
            except ValueError:
                messages.error(request, 'กรุณากรอกอายุเป็นตัวเลข')
                return render(request, 'from_view.html', context)
            
            # บันทึกหรืออัปเดตข้อมูล
            with transaction.atomic():
                if edit_id:
                    # แก้ไขข้อมูลเดิม
                    person = Person.objects.get(id=edit_id)
                    person.name = name
                    person.age = age_int
                    person.save()
                    
                    logger.info(f"อัปเดตข้อมูล: {name}, อายุ {age_int} (ID: {edit_id})")
                    messages.success(request, f'อัปเดตข้อมูลของ "{name}" เรียบร้อยแล้ว!')
                    
                    # กลับไปหน้าแสดงข้อมูล
                    return redirect('person')
                else:
                    # เพิ่มข้อมูลใหม่
                    person = Person(
                        name=name,
                        age=age_int
                    )
                    person.save()
                    
                    logger.info(f"บันทึกข้อมูลใหม่: {name}, อายุ {age_int}")
                    messages.success(request, f'บันทึกข้อมูลของ "{name}" (อายุ {age_int} ปี) เรียบร้อยแล้ว!')
            
            # อัปเดตจำนวนคนทั้งหมด
            context['total_persons'] = Person.objects.count()
            
            return render(request, 'from_view.html', context)
            
        except Person.DoesNotExist:
            messages.error(request, 'ไม่พบข้อมูลที่ต้องการแก้ไข')
            logger.warning(f"Person not found for edit: {edit_id}")
            
        except Exception as e:
            logger.error(f"Error in form submission: {str(e)}")
            messages.error(request, 'เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาลองใหม่อีกครั้ง')
            return render(request, 'from_view.html', context)
    
    return render(request, 'from_view.html', context)

@csrf_protect
@require_http_methods(["POST"])
def delete_person(request):
    """ลบข้อมูลบุคคล - ปรับปรุงประสิทธิภาพและความปลอดภัย"""
    try:
        person_id = request.POST.get('person_id')
        logger.info(f"Delete request received for person_id: {person_id}")
        
        if not person_id:
            messages.error(request, 'ไม่พบข้อมูลที่ต้องการลบ')
            logger.warning("No person_id provided in delete request")
            return redirect('person')
        
        with transaction.atomic():
            # ใช้ get_object_or_404 เพื่อประสิทธิภาพที่ดีกว่า
            person = get_object_or_404(Person, id=person_id, is_active=True)
            name = person.name
            
            # Soft delete แทนการลบจริง
            person.is_active = False
            person.save()
            
            logger.info(f"Soft deleted person: {name} (ID: {person_id})")
            messages.success(request, f'ลบข้อมูลของ "{name}" เรียบร้อยแล้ว')
        
    except Exception as e:
        logger.error(f"Error deleting person: {str(e)}")
        messages.error(request, 'เกิดข้อผิดพลาดในการลบข้อมูล')
    
    return redirect('person')