import React, { useState } from 'react';
import { Upload, message, Button, Card, Typography, Space } from 'antd';
import { UploadOutlined, CalendarOutlined } from '@ant-design/icons';
import type { UploadProps, UploadFile } from 'antd';
import './App.css';

const { Title, Text } = Typography;

// API Base URL
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
          message.success(`${name} uploaded successfully`);
          if (response.download_url) {
            setDownloadUrl(`${API_BASE_URL}${response.download_url}`);
          }
        } else {
          const errorMsg = response?.message || 'File processing failed';
          console.error('Upload response:', response);
          message.error(`Processing failed: ${errorMsg}`);
        }
      } else if (status === 'error') {
        console.error('Upload error:', info.file.error);
        message.error(`Upload failed: ${name}`);
      }
    },
  };

  return (
    <div className="app-container">
      <Card className="upload-card">
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div className="header">
            <CalendarOutlined className="logo" />
            <Title level={2}>Excel to iCal Converter</Title>
          </div>
          
          <div className="upload-section">
            <Upload {...uploadProps}>
              <Button icon={<UploadOutlined />} loading={loading} size="large">
                Select Excel File
              </Button>
            </Upload>
            <Text type="secondary">Supports .xlsx or .xls format files</Text>
          </div>

          {downloadUrl && (
            <div className="download-section">
              <Button 
                type="primary" 
                href={downloadUrl}
                size="large"
                icon={<CalendarOutlined />}
              >
                Download Calendar File
              </Button>
            </div>
          )}

          <div className="instructions">
            <Title level={4}>Instructions</Title>
            <ul>
              <li>Upload your Excel format schedule file</li>
              <li>System will automatically process and generate iCal file</li>
              <li>Download the generated calendar file</li>
              <li>Import the calendar file into your calendar app</li>
            </ul>
          </div>
        </Space>
      </Card>
    </div>
  );
}

export default App;
