import React, { useState, useRef } from 'react';
import { Upload, message, Button, Card, Typography, Space, Select, Table } from 'antd';
import { UploadOutlined, CalendarOutlined, GlobalOutlined, DownloadOutlined, CheckCircleOutlined } from '@ant-design/icons';
import type { UploadProps, UploadFile } from 'antd';
import { translations } from './locales/translations';
import './App.css';

const { Title, Text } = Typography;
const { Option } = Select;

// API Base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

// Language type
type LanguageType = 'en' | 'zh' | 'ja';

// Employee type
interface Employee {
  name: string;
  row: number;
}

// Schedule Preview type
interface SchedulePreview {
  date: string;
  day: number;
  month: number;
  year: number;
  weekday: string;
  start_time: string;
  end_time: string;
  task: string;
}

// 获取浏览器语言
const getBrowserLanguage = (): LanguageType => {
  const lang = navigator.language.toLowerCase();
  if (lang.startsWith('zh')) return 'zh';
  if (lang.startsWith('ja')) return 'ja';
  return 'en';
};

function App() {
  const [downloadUrl, setDownloadUrl] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [lang, setLang] = useState<LanguageType>(getBrowserLanguage());
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [selectedEmployee, setSelectedEmployee] = useState<string>('');
  const [loadingEmployees, setLoadingEmployees] = useState<boolean>(false);
  const [schedulePreview, setSchedulePreview] = useState<SchedulePreview[]>([]);
  const [weekInfo, setWeekInfo] = useState<string>('');
  const [converted, setConverted] = useState<boolean>(false);
  const downloadSectionRef = useRef<HTMLDivElement>(null);

  const t = translations[lang];

  // 表格列定义
  const columns = [
    {
      title: t.table.date,
      dataIndex: 'date',
      key: 'date',
      render: (_: any, record: SchedulePreview) => {
        return `${record.weekday} ${record.day}/${record.month}/${record.year}`;
      }
    },
    {
      title: t.table.time,
      key: 'time',
      render: (_: any, record: SchedulePreview) => `${record.start_time} - ${record.end_time}`
    },
    {
      title: t.table.task,
      dataIndex: 'task',
      key: 'task'
    }
  ];

  // 重置上传状态
  const resetUpload = () => {
    setDownloadUrl('');
    setFileList([]);
    setEmployees([]);
    setSelectedEmployee('');
    setSchedulePreview([]);
    setWeekInfo('');
    setConverted(false);
  };

  // 处理员工选择变化
  const handleEmployeeChange = (value: string) => {
    setSelectedEmployee(value);
    setDownloadUrl(''); // 清除下载链接
    setSchedulePreview([]); // 清除排班预览
    setConverted(false);
  };

  // 处理文件上传并获取员工列表
  const handleFileUpload = async (file: File) => {
    setLoadingEmployees(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/employees/`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();

      if (!data.error && data.employees) {
        setEmployees(data.employees);
      } else {
        message.error(data.message || t.messages.employeeLoadError);
      }
    } catch (error) {
      message.error(t.messages.employeeLoadError);
    } finally {
      setLoadingEmployees(false);
    }
  };

  const uploadProps: UploadProps = {
    name: 'file',
    accept: '.xlsx,.xls',
    showUploadList: true,
    maxCount: 1,
    fileList,
    beforeUpload: (file) => {
      resetUpload(); // 在上传新文件前重置所有状态
      handleFileUpload(file);
      return false; // 阻止自动上传
    },
    onChange(info) {
      setFileList(info.fileList);
    },
    onRemove: () => {
      resetUpload();
    }
  };

  // 处理转换请求
  const handleConvert = async () => {
    if (!selectedEmployee) {
      message.warning(t.messages.pleaseSelectEmployee);
      return;
    }

    if (!fileList.length) {
      message.warning(t.messages.uploadFailed);
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', fileList[0].originFileObj as File);
    formData.append('employee_name', selectedEmployee);

    try {
      const response = await fetch(`${API_BASE_URL}/api/convert/`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();

      if (!data.error) {
        message.success(t.messages.convertSuccess);
        setDownloadUrl(`${API_BASE_URL}${data.download_url}`);
        setSchedulePreview(data.schedule_preview);
        setWeekInfo(data.week_info);
        setConverted(true);
        
        setTimeout(() => {
          downloadSectionRef.current?.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          });
        }, 100);
      } else {
        message.error(data.message || t.messages.processingFailed);
      }
    } catch (error) {
      message.error(t.messages.processError.replace('{error}', ''));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Card className="upload-card">
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div className="header">
            <Space align="center" style={{ width: '100%', justifyContent: 'space-between' }}>
              <Space>
                <CalendarOutlined className="logo" />
                <Title level={2} style={{ margin: 0 }}>{t.title}</Title>
              </Space>
              <Select
                value={lang}
                onChange={setLang}
                style={{ width: 120 }}
                suffixIcon={<GlobalOutlined />}
              >
                <Option value="en">English</Option>
                <Option value="zh">中文</Option>
                <Option value="ja">日本語</Option>
              </Select>
            </Space>
          </div>
          
          <div className="upload-section">
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <Upload {...uploadProps}>
                <Button 
                  icon={<UploadOutlined />} 
                  loading={loading} 
                  size="large"
                  onClick={(e) => {
                    resetUpload();
                  }}
                >
                  {t.selectFile}
                </Button>
              </Upload>
              <Text type="secondary">{t.fileSupport}</Text>

              <div className="employee-select">
                <Select
                  placeholder={t.employeePlaceholder}
                  style={{ width: '100%', marginTop: '8px' }}
                  value={selectedEmployee || undefined}
                  onChange={handleEmployeeChange}
                  loading={loadingEmployees}
                  disabled={!employees.length}
                  notFoundContent={t.noEmployee}
                >
                  {employees.map((emp) => (
                    <Option key={emp.row} value={emp.name}>{emp.name}</Option>
                  ))}
                </Select>
              </div>

              {fileList.length > 0 && employees.length > 0 && (
                <Button
                  type="primary"
                  onClick={handleConvert}
                  loading={loading}
                  disabled={converted}
                  style={{ width: '100%' }}
                >
                  {converted ? t.messages.converted : t.steps.convert}
                </Button>
              )}
            </Space>
          </div>

          {downloadUrl && (
            <div className="download-section" ref={downloadSectionRef}>
              <Space align="center" className="success-message">
                <CheckCircleOutlined style={{ color: '#52c41a', fontSize: '24px' }} />
                <Text style={{ color: '#52c41a', fontSize: '16px' }}>
                  {t.messages.convertSuccess}
                </Text>
              </Space>

              {weekInfo && (
                <div className="week-info">
                  <Text strong>{weekInfo}</Text>
                </div>
              )}

              {schedulePreview.length > 0 && (
                <div className="schedule-preview">
                  <Table
                    dataSource={schedulePreview}
                    columns={columns}
                    pagination={false}
                    size="small"
                    className="preview-table"
                  />
                </div>
              )}

              <Button 
                type="primary" 
                href={downloadUrl}
                size="large"
                icon={<DownloadOutlined />}
              >
                {t.downloadFile}
              </Button>
            </div>
          )}

          <div className="instructions">
            <Title level={4}>{t.instructions}</Title>
            <ul>
              <li>{t.steps.upload}</li>
              <li>{t.steps.select}</li>
              <li>{t.steps.convert}</li>
              <li>{t.steps.download}</li>
              <li>{t.steps.import}</li>
            </ul>
          </div>
        </Space>
      </Card>
    </div>
  );
}

export default App;
