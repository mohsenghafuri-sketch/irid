import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu, Typography } from 'antd';
import { 
  DashboardOutlined, 
  InboxOutlined, 
  FormOutlined, 
  FileTextOutlined, 
  BarChartOutlined, 
  UserOutlined 
} from '@ant-design/icons';

// Import Pages
import MyRequests from './pages/MyRequests';
import FormsList from './pages/FormsList';
import Reports from './pages/Reports';

const { Header, Content, Sider } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ display: 'flex', alignItems: 'center', background: '#001529', padding: '0 20px' }}>
          <div style={{ color: 'white', fontSize: '1.5rem', fontWeight: 'bold', marginLeft: '40px' }}>
            سامانه IRID
          </div>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['1']}
            style={{ flex: 1, minWidth: 0 }}
          >
            <Menu.Item key="1" icon={<DashboardOutlined />}><Link to="/">داشبورد</Link></Menu.Item>
            <Menu.Item key="2" icon={<FileTextOutlined />}><Link to="/my-requests">درخواست‌های من</Link></Menu.Item>
            <Menu.Item key="3" icon={<InboxOutlined />}><Link to="/inbox">کارتابل اقدامات</Link></Menu.Item>
            <Menu.Item key="4" icon={<FormOutlined />}><Link to="/forms">فرم‌های من</Link></Menu.Item>
            <Menu.Item key="5" icon={<BarChartOutlined />}><Link to="/reports">گزارشات</Link></Menu.Item>
            <Menu.Item key="6" icon={<UserOutlined />}><Link to="/profile">پروفایل</Link></Menu.Item>
          </Menu>
        </Header>
        
        <Content style={{ padding: '24px', background: '#fff' }}>
          <Routes>
            <Route path="/" element={<div className="p-6"><h1>خوش آمدید</h1><p>به داشبورد مدیریتی IRID خوش آمدید.</p></div>} />
            <Route path="/my-requests" element={<MyRequests />} />
            <Route path="/forms" element={<FormsList />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/inbox" element={<div className="p-6"><h1>کارتابل</h1><p>درخواست‌های در انتظار تایید شما.</p></div>} />
            <Route path="/profile" element={<div className="p-6"><h1>پروفایل</h1><p>تنظیمات کاربری و سازمان.</p></div>} />
          </Routes>
        </Content>
      </Layout>
    </Router>
  );
};

export default App;
