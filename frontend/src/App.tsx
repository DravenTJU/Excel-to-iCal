import React, { useState } from 'react';
import { Upload, message, Button, Card, Typography, Space, Select } from 'antd';
import { UploadOutlined, CalendarOutlined, GlobalOutlined } from '@ant-design/icons';
import type { UploadProps, UploadFile } from 'antd';
import { translations } from './locales/translations';
import './App.css';

const { Title, Text } = Typography;
const { Option } = Select;

// API Base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://192.168.1.122:8000';

// 获取浏览器语言
const getBrowserLanguage = () => {
  const lang = navigator.language.toLowerCase();
  return lang.startsWith('zh') ? 'zh' : 'en';
};

function App() {
  const [downloadUrl, setDownloadUrl] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [lang, setLang] = useState<'en' | 'zh'>(getBrowserLanguage());

  const t = translations[lang];

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
          message.success(t.messages.uploadSuccess.replace('{filename}', name));
          if (response.download_url) {
            setDownloadUrl(`${API_BASE_URL}${response.download_url}`);
          }
        } else {
          const errorMsg = response?.message || t.messages.processingFailed;
          console.error('Upload response:', response);
          message.error(t.messages.processError.replace('{error}', errorMsg));
        }
      } else if (status === 'error') {
        console.error('Upload error:', info.file.error);
        message.error(t.messages.uploadFailed.replace('{filename}', name));
      }
    },
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
                style={{ width: 100 }}
                suffixIcon={<GlobalOutlined />}
              >
                <Option value="en">English</Option>
                <Option value="zh">中文</Option>
              </Select>
            </Space>
          </div>
          
          <div className="upload-section">
            <Upload {...uploadProps}>
              <Button icon={<UploadOutlined />} loading={loading} size="large">
                {t.selectFile}
              </Button>
            </Upload>
            <Text type="secondary">{t.fileSupport}</Text>
          </div>

          {downloadUrl && (
            <div className="download-section">
              <Button 
                type="primary" 
                href={downloadUrl}
                size="large"
                icon={<CalendarOutlined />}
              >
                {t.downloadFile}
              </Button>
            </div>
          )}

          <div className="instructions">
            <Title level={4}>{t.instructions}</Title>
            <ul>
              <li>{t.steps.upload}</li>
              <li>{t.steps.process}</li>
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
