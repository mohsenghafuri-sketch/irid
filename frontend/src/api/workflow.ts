import axios from "axios";

export interface Transition {
  id: number;
  name: string;
  from_state?: string;
  to_state?: string;
}

export interface WorkflowRequest {
  id: number;
  tracking_code?: string;
  form_name?: string;
  current_state?: string;
  created_at?: string;
  user_full_name?: string;
  available_transitions?: Transition[];
}

export interface ExecuteTransitionPayload {
  request_id: number;
  transition_id: number;
  comment: string;
}

const API_BASE_URL = "/api/workflow";

export const workflowApi = {
  // دریافت لیست کارتابل
  getInbox: async (): Promise<WorkflowRequest[]> => {
    const response = await axios.get(`${API_BASE_URL}/inbox/`, {
      withCredentials: true,
    });
    // مدیریت حالت‌های مختلف بازگشت داده (لیست ساده یا با Pagination)
    if (Array.isArray(response.data)) return response.data;
    if (Array.isArray(response.data.results)) return response.data.results;
    return [];
  },

  // اجرای یک انتقال در گردش کار
  executeTransition: async (payload: ExecuteTransitionPayload) => {
    const response = await axios.post(`${API_BASE_URL}/execute/`, payload, {
      withCredentials: true,
    });
    return response.data;
  },
};
