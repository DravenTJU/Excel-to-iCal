import os
import traceback
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.http import FileResponse
from datetime import datetime
import tempfile

from .ical import ShiftScheduler

class ConvertExcelToICalView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        try:
            # 检查是否有文件上传
            if 'file' not in request.FILES:
                return Response({
                    'error': True,
                    'message': '没有上传文件'
                }, status=status.HTTP_400_BAD_REQUEST)

            excel_file = request.FILES['file']
            
            # 检查文件类型
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return Response({
                    'error': True,
                    'message': '请上传Excel文件（.xlsx或.xls格式）'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 创建临时文件来保存上传的Excel
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_excel:
                    for chunk in excel_file.chunks():
                        temp_excel.write(chunk)
                    temp_excel_path = temp_excel.name
            except Exception as e:
                return Response({
                    'error': True,
                    'message': f'保存临时文件失败: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # 生成输出文件名
            output_filename = f"sushi_schedule_week_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ics"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

            # 确保media目录存在
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            # 使用转换类处理文件
            try:
                scheduler = ShiftScheduler(temp_excel_path)
                
                if not scheduler.read_excel():
                    return Response({
                        'error': True,
                        'message': '无法读取Excel文件，请检查文件格式'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if not scheduler.get_week_info():
                    return Response({
                        'error': True,
                        'message': '无法获取周信息，请检查Excel文件格式'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
                if not scheduler.get_days_info():
                    return Response({
                        'error': True,
                        'message': '无法获取日期信息，请检查Excel文件格式'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
                lulu_row = scheduler.find_lulu_row()
                if lulu_row is None:
                    return Response({
                        'error': True,
                        'message': '未找到排班信息，请检查Excel文件内容'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
                cal = scheduler.create_calendar(lulu_row)
                
                # 保存iCal文件
                if not scheduler.save_calendar(cal, output_path):
                    return Response({
                        'error': True,
                        'message': '保存iCal文件失败'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({
                    'error': True,
                    'message': f'处理文件时出错: {str(e)}',
                    'detail': traceback.format_exc()
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                # 清理临时文件
                try:
                    os.unlink(temp_excel_path)
                except:
                    pass

            # 返回成功响应
            return Response({
                'error': False,
                'message': '转换成功',
                'download_url': f'/api/download/{output_filename}/'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': True,
                'message': f'服务器错误: {str(e)}',
                'detail': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadICalView(APIView):
    def get(self, request, filename):
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            if not os.path.exists(file_path):
                return Response({
                    'error': True,
                    'message': '文件不存在'
                }, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'))
            response['Content-Type'] = 'text/calendar'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return Response({
                'error': True,
                'message': f'下载文件时出错: {str(e)}',
                'detail': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 