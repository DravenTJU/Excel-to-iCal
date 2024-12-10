#!/usr/bin/env python
import os
import sys

def main():
    """Run administrative tasks."""
    # 添加当前目录到Python路径
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_path)
    
    # 设置Django的默认设置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        # 导入Django的命令行工具
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    # 执行命令行命令
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main() 