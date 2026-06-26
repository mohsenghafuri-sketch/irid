import React, { useEffect, useState } from 'react';
import { Table, Button, Space, message, Tag, Typography } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, ReloadOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title } = Typography;

interface FormDefinition {
  id: number;
  name: string;
  slug: string;
  description: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

const FormsList: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<FormDefinition[]>([]);

  const fetchForms = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/forms/', {
        withCredentials: true,
      });
      setData(response.data);
    } catch (error: any) {
      console.error('Fetch forms error:', error);

      if (error?.response?.status === 401) {
        message.error('نشست کاربری معتبر نیست. لطفاً دوباره وارد شوید.');
      } else {
        message.error('خطا در دریافت اطلاعات فرم‌ها');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchForms();
  }, []);

  const columns = [
    {
      title: 'نام فرم',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => <strong>{text}</strong>,
    },
    {
      title: 'شناسه فنی',
      dataIndex: 'slug',
      key: 'slug',
    },
    {
      title: 'وضعیت',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (active: boolean) => (
        <Tag color={active ? 'green' : 'red'}>
          {active ? 'فعال' : 'غیرفعال'}
        </Tag>
      ),
    },
    {
      title: 'تاریخ ایجاد',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString('fa-IR'),
    },
    {
      title: 'عملیات',
      key: 'action',
      render: () => (
        <Space size='middle'>
          <Button icon={<EditOutlined />} size='small'>ویرایش</Button>
          <Button icon={<DeleteOutlined />} danger size='small'>حذف</Button>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 24 }}>
        <Title level={3}>مدیریت فرم‌ها</Title>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={fetchForms}>به‌روزرسانی</Button>
          <Button type='primary' icon={<PlusOutlined />}>فرم جدید</Button>
        </Space>
      </div>

      <Table
        columns={columns}
        dataSource={data}
        rowKey='id'
        loading={loading}
        bordered
      />
    </div>
  );
};

export default FormsList;
