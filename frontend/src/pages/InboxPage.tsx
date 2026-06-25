import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface WorkflowRequest {
  id: number;
  tracking_code: string;
  current_state_name: string;
  created_at: string;
}

const InboxPage: React.FC = () => {
  const [requests, setRequests] = useState<WorkflowRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // فراخوانی API بک‌اِند برای دریافت لیست نامه‌ها
    axios.get('/api/workflow/inbox/')
      .then(res => {
        setRequests(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("خطا در دریافت لیست:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{padding: '20px', fontFamily: 'Tahoma', direction: 'rtl'}}>در حال دریافت نامه‌ها...</div>;

  return (
    <div style={{ padding: '20px', direction: 'rtl', fontFamily: 'Tahoma' }}>
      <h2 style={{ borderBottom: '2px solid #3498db', paddingBottom: '10px' }}>کارتابل ورودی</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px', backgroundColor: 'white' }}>
        <thead>
          <tr style={{ backgroundColor: '#f8f9fa', textAlign: 'right' }}>
            <th style={{ padding: '12px', border: '1px solid #ddd' }}>شناسه</th>
            <th style={{ padding: '12px', border: '1px solid #ddd' }}>کد رهگیری</th>
            <th style={{ padding: '12px', border: '1px solid #ddd' }}>وضعیت فعلی</th>
            <th style={{ padding: '12px', border: '1px solid #ddd' }}>تاریخ ایجاد</th>
          </tr>
        </thead>
        <tbody>
          {requests.length > 0 ? requests.map(req => (
            <tr key={req.id}>
              <td style={{ padding: '12px', border: '1px solid #ddd' }}>{req.id}</td>
              <td style={{ padding: '12px', border: '1px solid #ddd' }}>{req.tracking_code || '---'}</td>
              <td style={{ padding: '12px', border: '1px solid #ddd' }}>
                <span style={{ backgroundColor: '#e1f5fe', padding: '4px 8px', borderRadius: '4px', fontSize: '0.9rem' }}>
                  {req.current_state_name}
                </span>
              </td>
              <td style={{ padding: '12px', border: '1px solid #ddd' }}>
                {new Date(req.created_at).toLocaleDateString('fa-IR')}
              </td>
            </tr>
          )) : (
            <tr>
              <td colSpan={4} style={{ padding: '20px', textAlign: 'center' }}>هیچ موردی در کارتابل شما نیست.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default InboxPage;
