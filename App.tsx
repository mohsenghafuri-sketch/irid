docker compose exec -T frontend sh -c "cat <<EOF > src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { 
  DashboardOutlined, 
  InboxOutlined, 
  FormOutlined, 
  FileTextOutlined, 
  BarChartOutlined, 
  UserOutlined 
} from '@ant-design/icons';
import 'antd/dist/reset.css'; // ایمپورت استایل‌های آنت دیزاین

// Import Pages
import MyRequests from './pages/MyRequests';
import FormsList from './pages/FormsList';
import Reports from './pages/Reports';

const { Header, Content } = Layout;

const App: React.FC = () => {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh', direction: 'rtl' }}>
        <Header style={{ display: 'flex', alignItems: 'center', background: '#001529', padding: '0 20px' }}>
          <div style={{ color: 'white', fontSize: '1.2rem', fontWeight: 'bold', marginLeft: '40px' }}>
            سامانه IRID
          </div>
          <Menu
            theme=\"dark\"
            mode=\"horizontal\"
            defaultSelectedKeys={['1']}
            style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'row' }}
          >
            <Menu.Item key=\"1\" icon={<DashboardOutlined />}><Link to=\"/\">داشبورد</Link></Menu.Item>
            <Menu.Item key=\"2\" icon={<FileTextOutlined />}><Link to=\"/my-requests\">درخواست‌های من</Link></Menu.Item>
            <Menu.Item key=\"3\" icon={<InboxOutlined />}><Link to=\"/inbox\">کارتابل</Link></Menu.Item>
            <Menu.Item key=\"4\" icon={<FormOutlined />}><Link to=\"/forms\">فرم‌های من</Link></Menu.Item>
            <Menu.Item key=\"5\" icon={<BarChartOutlined />}><Link to=\"/reports\">گزارشات</Link></Menu.Item>
            <Menu.Item key=\"6\" icon={<UserOutlined />}><Link to=\"/profile\">پروفایل</Link></Menu.Item>
          </Menu>
        </Header>
        
        <Content style={{ padding: '24px', background: '#f5f5f5' }}>
          <div style={{ background: '#fff', padding: '24px', minHeight: '80vh', borderRadius: '8px' }}>
            <Routes>
              <Route path=\"/\" element={<div><h1>خوش آمدید</h1><p>به پنل مدیریت سامانه IRID خوش آمدید.</p></div>} />
              <Route path=\"/my-requests\" element={<MyRequests />} />
              <Route path=\"/forms\" element={<FormsList />} />
              <Route path=\"/reports\" element={<Reports />} />
              <Route path=\"/inbox\" element={<div><h1>کارتابل</h1><p>لیست کارهای در انتظار تایید.</p></div>} />
              <Route path=\"/profile\" element={<div><h1>پروفایل</h1><p>اطلاعات کاربری و سازمانی.</p></div>} />
            </Routes>
          </div>
        </Content>
      </Layout>
    </Router>
  );
};

export default App;
EOF"
