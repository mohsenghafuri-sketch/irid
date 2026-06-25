import axios from "axios";
import { getCsrfToken } from "./csrf";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface AuthUser {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
}

// تنظیمات سراسری اکسیس برای ارسال کوکی‌ها
axios.defaults.withCredentials = true;

// ایجاد یک اینستنس سفارشی برای تزریق خودکار توکن CSRF در هدرها
const api = axios.create({
  baseURL: "/api"
});

api.interceptors.request.use((config) => {
  const token = getCsrfToken();
  if (token) {
    config.headers["X-CSRFToken"] = token;
  }
  return config;
});

export const login = async (payload: LoginPayload) => {
  const response = await api.post("/accounts/login/", payload);
  return response.data;
};

export const logout = async () => {
  const response = await api.post("/accounts/logout/");
  return response.data;
};

export const getMe = async (): Promise<AuthUser> => {
  const response = await api.get("/accounts/me/");
  return response.data;
};
