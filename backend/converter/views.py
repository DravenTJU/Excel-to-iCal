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

class GetEmployeesView(APIView):
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

            try:
                # 使用转换类处理文件
                scheduler = ShiftScheduler(temp_excel_path)
                
                if not scheduler.read_excel():
                    return Response({
                        'error': True,
                        'message': '无法读取Excel文件，请检查文件格式'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # 获取员工列表
                employees = scheduler.get_employees()
                
                if not employees:
                    return Response({
                        'error': True,
                        'message': '未找到员工信息'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # 返回员工列表
                return Response({
                    'error': False,
                    'employees': employees
                }, status=status.HTTP_200_OK)

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

        except Exception as e:
            return Response({
                'error': True,
                'message': f'服务器错误: {str(e)}',
                'detail': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConvertExcelToICalView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        try:
            # 检查是否有文件上传和员工名字
            if 'file' not in request.FILES:
                return Response({
                    'error': True,
                    'message': '没有上传文件'
                }, status=status.HTTP_400_BAD_REQUEST)

            if 'employee_name' not in request.data:
                return Response({
                    'error': True,
                    'message': '请选择员工'
                }, status=status.HTTP_400_BAD_REQUEST)

            excel_file = request.FILES['file']
            employee_name = request.data['employee_name']
            
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
            output_filename = f"schedule_{employee_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ics"
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
                    
                employee_row = scheduler.find_employee_row(employee_name)
                if employee_row is None:
                    return Response({
                        'error': True,
                        'message': '未找到该员工的排班信息'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
                cal = scheduler.create_calendar(employee_row)
                
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