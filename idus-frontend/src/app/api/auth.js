import { BASE_URL } from "./config";

export function storeTokens({ access, refresh }) {
  if (typeof window !== "undefined") {
    localStorage.setItem("access_token", access);
    if (refresh) {
      localStorage.setItem("refresh_token", refresh);
    }
  }
}

export function clearTokens() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }
}

export async function refreshAccessToken() {
  const refresh =
    typeof window !== "undefined" ? localStorage.getItem("refresh_token") : null;

  const response = await fetch(`${BASE_URL}/auth/jwt/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });

  if (!response.ok) {
    throw new Error("Falha ao renovar o token.");
  }

  const data = await response.json();
  if (data.access) {
    storeTokens({ access: data.access, refresh });
  }
  return data;
}

export async function login(credentials) {
  const response = await fetch(`${BASE_URL}/auth/jwt/create/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Erro no login.");
  }

  const data = await response.json();
  storeTokens(data);
  return data;
}

export async function logout() {
  try {
    await fetch(`${BASE_URL}/auth/logout/`, {
      method: "POST",
    });
  } catch (error) {
    console.error("Erro no logout:", error.message);
  } finally {
    clearTokens();
  }
}
