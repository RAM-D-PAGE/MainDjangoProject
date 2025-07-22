# Django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.html import escape
from django.utils import timezone

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
    """หน้าแสดงรายการบุคคล - อัปเดตข้อมูลล่าสุดเสมอ"""
    try:
        # ดึงข้อมูลบุคคลทั้งหมด เรียงตามวันที่สร้างล่าสุด
        all_persons = Person.objects.all().order_by('-date')
        
        # สถิติเพิ่มเติม
        total_count = all_persons.count()
        
        # คำนวณอายุเฉลี่ย
        if total_count > 0:
            total_age = sum(person.age for person in all_persons)
            avg_age = total_age / total_count
        else:
            avg_age = 0
        
        context = {
            'persons': all_persons,
            'total_count': total_count,
            'avg_age': avg_age,
            'today': timezone.now().date(),
        }
        
        # ไม่ใช้ cache หากมี refresh parameter
        response = render(request, 'person.html', context)
        
        # ป้องกัน browser cache
        if request.GET.get('refresh'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response
        
    except Exception as e:
        logger.error(f"Error loading person list: {e}")
        return render(request, 'person.html', {
            'persons': [],
            'total_count': 0,
            'avg_age': 0,
            'today': timezone.now().date(),
        })

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
def delete_person(request):
    """ลบข้อมูลบุคคล"""
    if request.method == 'POST':
        try:
            person_id = request.POST.get('person_id')
            logger.info(f"Delete request received for person_id: {person_id}")
            
            if not person_id:
                messages.error(request, 'ไม่พบข้อมูลที่ต้องการลบ')
                logger.warning("No person_id provided in delete request")
                return redirect('person')
            
            with transaction.atomic():
                person = Person.objects.get(id=person_id)
                name = person.name
                person.delete()
                
                logger.info(f"ลบข้อมูล: {name} (ID: {person_id})")
                messages.success(request, f'ลบข้อมูลของ "{name}" เรียบร้อยแล้ว')
            
        except Person.DoesNotExist:
            messages.error(request, 'ไม่พบข้อมูลที่ต้องการลบ')
            logger.warning(f"Person not found for deletion: {person_id}")
            
        except Exception as e:
            logger.error(f"Error deleting person: {str(e)}")
            messages.error(request, 'เกิดข้อผิดพลาดในการลบข้อมูล')
    else:
        logger.warning(f"Invalid method for delete_person: {request.method}")
        messages.error(request, 'วิธีการเรียกใช้ไม่ถูกต้อง')
    
    return redirect('person')