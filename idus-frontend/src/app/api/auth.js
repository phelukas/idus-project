import { BASE_URL } from "./config";

/**
 * Since the backend now manages authentication tokens using HttpOnly cookies,
 * the frontend no longer stores or directly accesses these values. All
 * requests that require authentication should include `credentials: "include"`
 * so the cookies are sent along.
 */

export async function refreshAccessToken() {
  const response = await fetch(`${BASE_URL}/auth/jwt/refresh/`, {
    method: "POST",
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Falha ao renovar o token.");
  }

  return await response.json();
}

export async function login(credentials) {
  const response = await fetch(`${BASE_URL}/auth/jwt/create/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Erro no login.");
  }

  return await response.json();
}

export async function logout() {
  try {
    await fetch(`${BASE_URL}/auth/logout/`, {
      method: "POST",
      credentials: "include",
    });
  } catch (error) {
    console.error("Erro no logout:", error.message);
  }
}
