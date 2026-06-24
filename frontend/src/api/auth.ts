import { getCsrfToken } from "./csrf";

export type AuthUser = {
  id: number;
  email: string;
  full_name: string;
  is_staff: boolean;
  is_superuser: boolean;
};

export type AuthState = {
  authenticated: boolean;
  user: AuthUser | null;
};

const jsonHeaders = {
  "Content-Type": "application/json",
};

async function parseJsonResponse<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const message =
      data?.detail ||
      data?.non_field_errors?.[0] ||
      data?.email?.[0] ||
      data?.password?.[0] ||
      "درخواست ناموفق بود.";

    throw new Error(message);
  }

  return data as T;
}

export async function getMe(): Promise<AuthState> {
  const response = await fetch("/api/auth/me/", {
    method: "GET",
    credentials: "include",
  });

  return parseJsonResponse<AuthState>(response);
}

export async function login(email: string, password: string): Promise<AuthState> {
  const response = await fetch("/api/auth/login/", {
    method: "POST",
    credentials: "include",
    headers: jsonHeaders,
    body: JSON.stringify({ email, password }),
  });

  return parseJsonResponse<AuthState>(response);
}

export async function logout(): Promise<AuthState> {
  const csrfToken = getCsrfToken();

  const response = await fetch("/api/auth/logout/", {
    method: "POST",
    credentials: "include",
    headers: {
      ...jsonHeaders,
      ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
    },
  });

  return parseJsonResponse<AuthState>(response);
}
