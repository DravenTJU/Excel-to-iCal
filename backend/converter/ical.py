import os
import pandas as pd
from datetime import datetime, timedelta
import re
from icalendar import Calendar, Event
import pytz
import sys

class ShiftScheduler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.week_info = None
        self.days_info = []
        self.timezone = pytz.timezone('Pacific/Auckland')
        self.debug = True  # 添加调试模式
    
    def debug_print(self, message):
        if self.debug:
            print(message)
    
    def read_excel(self):
        try:
            # 读取Excel文件，不使用默认的header
            self.df = pd.read_excel(self.file_path, header=None)
            self.debug_print(f"成功读取Excel文件")
            return True
        except Exception as e:
            print(f"读取Excel文件错误: {str(e)}")
            return False
    
    def get_week_info(self):
        try:
            # 从B1和B2获取周信息
            week_info_b1 = str(self.df.iloc[0, 1]).strip()
            week_info_b2 = str(self.df.iloc[1, 1]).strip()
            
            self.week_info = week_info_b1 if week_info_b1 and week_info_b1 != 'nan' else week_info_b2
            self.debug_print(f"获取到的周信息: {self.week_info}")
            
            return True
        except Exception as e:
            print(f"获取周信息错误: {str(e)}")
            return False
    
    def get_days_info(self):
        try:
            # 获取每天的日期信息（B4, E4, H4, K4, N4, Q4, T4）
            day_columns = [1, 4, 7, 10, 13, 16, 19]  # B=1, E=4, H=7 等
            
            # 先收集所有日期信息，检查是否跨年
            temp_days_info = []
            months = set()
            
            for col in day_columns:
                day_info = str(self.df.iloc[3, col]).strip()
                if day_info and day_info != 'nan':
                    # 解析日期，格式如 "Monday 11/11"
                    match = re.search(r'(\w+)\s+(\d{1,2}/\d{1,2})', day_info)
                    if match:
                        day, month = map(int, match.group(2).split('/'))
                        months.add(month)
                        temp_days_info.append({
                            'weekday': match.group(1),
                            'date': match.group(2),
                            'column': col,
                            'month': month,
                            'day': day
                        })
            
            # 检查是否跨年（同时存在12月和1月）
            is_year_end = 12 in months and 1 in months
            current_year = datetime.now().year
            
            # 处理年份
            self.days_info = []
            for day_data in temp_days_info:
                # 只有在跨年且月份为1月时才加一年
                year = current_year + 1 if (is_year_end and day_data['month'] == 1) else current_year
                day_data['year'] = year
                self.days_info.append(day_data)
                self.debug_print(f"解析到日期信息: {day_data}")
            
            return True
        except Exception as e:
            print(f"获取日期信息错误: {str(e)}")
            return False
    
    def get_employees(self):
        """获取员工列表"""
        try:
            # 从第4行开始查找A列的员工名字
            employees = []
            for idx in range(4, len(self.df)):
                name = str(self.df.iloc[idx, 0]).strip()
                if name and name != 'nan':
                    employees.append({
                        'name': name,
                        'row': idx
                    })
            
            self.debug_print(f"找到的员工列表: {employees}")
            return employees
        except Exception as e:
            print(f"获取员工列表错误: {str(e)}")
            return []
    
    def find_employee_row(self, employee_name):
        """根据员工名字查找对应的行号"""
        try:
            # 在A列查找指定员工名字的单元格
            column_a = self.df.iloc[:, 0].astype(str)
            employee_rows = column_a.str.contains(employee_name, case=False, regex=False)
            matching_rows = self.df.index[employee_rows].tolist()
            
            if not matching_rows:
                print(f"未找到员工 {employee_name} 的排班信息")
                return None
            
            self.debug_print(f"找到员工 {employee_name} 所在行: {matching_rows[0]}")
            return matching_rows[0]  # 返回第一个匹配的行号
        except Exception as e:
            print(f"查找员工行号错误: {str(e)}")
            return None
    
    def get_shift_times(self, row_index, day_column):
        try:
            start_time = str(self.df.iloc[row_index, day_column]).strip()
            end_time = str(self.df.iloc[row_index, day_column + 1]).strip()  # 修改：在同一行获取结束时间
            task = str(self.df.iloc[row_index, day_column + 2]).strip()  # 修改：在同一行获取任务
            
            # 检查时间格式
            if start_time == 'nan' or end_time == 'nan':
                return None, None, None
            
            self.debug_print(f"获取到班次信息 - 开始: {start_time}, 结束: {end_time}, 任务: {task}")
            
            # 统一时间格式（去除秒）
            if ':' in start_time:
                start_time = start_time.split(':')[0] + ':' + start_time.split(':')[1]
            if ':' in end_time:
                end_time = end_time.split(':')[0] + ':' + end_time.split(':')[1]
            
            return start_time, end_time, task
        except Exception as e:
            print(f"获取班次时间错误: {str(e)}")
            return None, None, None
    
    def create_calendar(self, employee_row):
        cal = Calendar()
        cal.add('prodid', '-//Sushi Restaurant Shift Schedule//EN')
        cal.add('version', '2.0')
        
        for day_info in self.days_info:
            start_time, end_time, task = self.get_shift_times(employee_row, day_info['column'])
            if not all([start_time, end_time]):
                continue
            
            try:
                start_hour, start_minute = map(int, start_time.split(':'))
                end_hour, end_minute = map(int, end_time.split(':'))
                
                # 使用 day_info 中的年份、月份和日期
                start_dt = self.timezone.localize(datetime(
                    day_info['year'],
                    day_info['month'],
                    day_info['day'],
                    start_hour,
                    start_minute
                ))
                
                end_dt = self.timezone.localize(datetime(
                    day_info['year'],
                    day_info['month'],
                    day_info['day'],
                    end_hour,
                    end_minute
                ))
                
                event = Event()
                event.add('summary', f'{task if task else "Work"} {start_hour}-{end_hour}')
                event.add('dtstart', start_dt)
                event.add('dtend', end_dt)
                event.add('description', f'Task: {task}')
                
                cal.add_component(event)
                self.debug_print(f"添加事件: {day_info['year']}/{day_info['month']}/{day_info['day']} {start_time}-{end_time} {task}")
            except Exception as e:
                print(f"创建事件错误: {str(e)}")
                continue
        
        return cal
    
    def save_calendar(self, cal, output_file):
        try:
            with open(output_file, 'wb') as f:
                f.write(cal.to_ical())
            print(f"日历文件已保存到: {output_file}")
            return True
        except Exception as e:
            print(f"保存日历文件错误: {str(e)}")
            return False
    
    def process(self):
        if not self.read_excel():
            return False
            
        if not self.get_week_info():
            return False
            
        if not self.get_days_info():
            return False
            
        lulu_row = self.find_lulu_row()
        if lulu_row is None:
            return False
            
        cal = self.create_calendar(lulu_row)
        
        # 生成输出文件名
        output_file = f"sushi_schedule_week_{datetime.now().strftime('%Y%m%d')}.ics"
        
        return self.save_calendar(cal, output_file)

if __name__ == "__main__":
    try:
        # 获取程序运行路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe运行
            application_path = os.path.dirname(sys.executable)
        else:
            # 如果是python脚本运行
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        # 查找以"Duty Roster"开头的xlsx文件
        excel_file = None
        for file in os.listdir(application_path):
            if file.startswith("Duty Roster") and file.endswith(".xlsx"):
                excel_file = os.path.join(application_path, file)
                break
        
        if excel_file:
            print(f"找到排班表: {excel_file}")
            scheduler = ShiftScheduler(excel_file)
            scheduler.process()
        else:
            print("错误: 在当前目录下未找到以'Duty Roster'开头的xlsx文件")
        
        # 添加程序结束提示
        input("\n按回车键退出程序...")
            
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        input("\n按回车键退出程序...")