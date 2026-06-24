export function getCookie(name: string): string | null {
  const cookies = document.cookie ? document.cookie.split("; ") : [];

  for (const cookie of cookies) {
    const separatorIndex = cookie.indexOf("=");
    const cookieName = decodeURIComponent(cookie.slice(0, separatorIndex));
    const cookieValue = decodeURIComponent(cookie.slice(separatorIndex + 1));

    if (cookieName === name) {
      return cookieValue;
    }
  }

  return null;
}

export function getCsrfToken(): string | null {
  return getCookie("csrftoken");
}
