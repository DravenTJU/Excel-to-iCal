import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import FileResponse
from datetime import datetime
import tempfile

from .ical import ShiftScheduler

class ConvertExcelToICalView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'converter/upload.html'

    def get(self, request):
        return Response({
            'title': 'Excel转iCal工具',
            'message': '请选择Excel文件上传'
        })

    def post(self, request):
        try:
            # 检查是否有文件上传
            if 'file' not in request.FILES:
                return Response({
                    'title': 'Excel转iCal工具',
                    'message': '没有上传文件',
                    'error': True
                })

            excel_file = request.FILES['file']
            
            # 检查文件类型
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return Response({
                    'title': 'Excel转iCal工具',
                    'message': '请上传Excel文件',
                    'error': True
                })

            # 创建临时文件来保存上传的Excel
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_excel:
                for chunk in excel_file.chunks():
                    temp_excel.write(chunk)
                temp_excel_path = temp_excel.name

            # 生成输出文件名
            output_filename = f"sushi_schedule_week_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ics"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

            # 确保media目录存在
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            # 使用你的转换类处理文件
            scheduler = ShiftScheduler(temp_excel_path)
            if not scheduler.read_excel():
                return Response({
                    'title': 'Excel转iCal工具',
                    'message': '无法读取Excel文件',
                    'error': True
                })
            
            if not scheduler.get_week_info():
                return Response({
                    'title': 'Excel转iCal工具',
                    'message': '无法获取周信息',
                    'error': True
                })
                
            if not scheduler.get_days_info():
                return Response({
                    'title': 'Excel转iCal工具',
                    'message': '无法获取日期信息',
                    'error': True
                })
                
            lulu_row = scheduler.find_lulu_row()
            if lulu_row is None:
                return Response({
                    'title': 'Excel转iCal工具',
                    'message': '未找到排班信息',
                    'error': True
                })
                
            cal = scheduler.create_calendar(lulu_row)
            
            # 保存iCal文件
            if not scheduler.save_calendar(cal, output_path):
                return Response({
                    'title': 'Excel转iCal工具',
                    'message': '保存iCal文件失败',
                    'error': True
                })

            # 清理临时文件
            os.unlink(temp_excel_path)

            # 返回成功响应
            return Response({
                'title': 'Excel转iCal工具',
                'message': '转换成功',
                'download_url': f'/api/download/{output_filename}/'
            })

        except Exception as e:
            return Response({
                'title': 'Excel转iCal工具',
                'message': str(e),
                'error': True
            })

class DownloadICalView(APIView):
    def get(self, request, filename):
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            if not os.path.exists(file_path):
                return Response({'error': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'))
            response['Content-Type'] = 'text/calendar'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 