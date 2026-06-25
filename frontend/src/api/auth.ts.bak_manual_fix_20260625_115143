import axios from "axios";
import { ensureCsrfCookie } from "./csrf";

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

axios.defaults.withCredentials = true;

export const login = async (payload: LoginPayload) => {
  await ensureCsrfCookie();
  const response = await axios.post("/api/accounts/login/", payload);
  return response.data;
};

export const logout = async () => {
  await ensureCsrfCookie();
  const response = await axios.post("/api/accounts/logout/");
  return response.data;
};

export const getMe = async (): Promise<AuthUser> => {
  const response = await axios.get("/api/accounts/me/");
  return response.data;
};
