import React, { useState } from 'react';
import { Upload, message, Button, Card, Typography, Space } from 'antd';
import { UploadOutlined, CalendarOutlined } from '@ant-design/icons';
import type { UploadProps, UploadFile } from 'antd';
import './App.css';

const { Title, Text } = Typography;

// API基础URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://192.168.1.122:8000';

function App() {
  const [downloadUrl, setDownloadUrl] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const uploadProps: UploadProps = {
    name: 'file',
    action: `${API_BASE_URL}/api/convert/`,
    accept: '.xlsx,.xls',
    showUploadList: true,
    maxCount: 1,
    withCredentials: true,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
    onChange(info) {
      const { status, name, response } = info.file;
      
      if (status === 'uploading') {
        setLoading(true);
        return;
      }
      
      setLoading(false);

      if (status === 'done') {
        if (response && !response.error) {
          message.success(`${name} 文件上传成功`);
          if (response.download_url) {
            setDownloadUrl(`${API_BASE_URL}${response.download_url}`);
          }
        } else {
          const errorMsg = response?.message || '文件处理失败';
          console.error('上传响应:', response);
          message.error(`处理失败: ${errorMsg}`);
        }
      } else if (status === 'error') {
        console.error('上传错误:', info.file.error);
        message.error(`上传失败: ${name}`);
      }
    },
  };

  return (
    <div className="app-container">
      <Card className="upload-card">
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div className="header">
            <CalendarOutlined className="logo" />
            <Title level={2}>Excel 排班表转日历</Title>
          </div>
          
          <div className="upload-section">
            <Upload {...uploadProps}>
              <Button icon={<UploadOutlined />} loading={loading} size="large">
                选择Excel文件
              </Button>
            </Upload>
            <Text type="secondary">支持 .xlsx 或 .xls 格式的Excel文件</Text>
          </div>

          {downloadUrl && (
            <div className="download-section">
              <Button 
                type="primary" 
                href={downloadUrl}
                size="large"
                icon={<CalendarOutlined />}
              >
                下载日历文件
              </Button>
            </div>
          )}

          <div className="instructions">
            <Title level={4}>使用说明</Title>
            <ul>
              <li>上传Excel格式的排班表文件</li>
              <li>系统会自动处理并生成iCal格式的日历文件</li>
              <li>下载生成的日历文件</li>
              <li>将日历文件导入到你的日历应用中</li>
            </ul>
          </div>
        </Space>
      </Card>
    </div>
  );
}

export default App;
