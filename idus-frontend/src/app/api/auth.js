import { BASE_URL } from "./config";
import Cookies from "js-cookie";

export function saveTokens({ access, refresh }) {
  if (typeof window !== "undefined") {

    if (access) Cookies.set("access_token", access, { expires: 7, path: "/" });
    if (refresh)
      Cookies.set("refresh_token", refresh, { expires: 30, path: "/" });
  }
}

export const getAccessToken = () => {
  if (typeof window !== "undefined") {
    return Cookies.get("access_token");
  }
  return null;
};

export const getRefreshToken = () => {
  if (typeof window !== "undefined") {
    return Cookies.get("refresh_token");
  }
  return null;
};

export const clearTokens = () => {
  Cookies.remove("access_token", { path: "/" });
  Cookies.remove("refresh_token", { path: "/" });
};

/**
 * Renovar token de acesso usando o token de refresh.
 * @returns {Promise<string>} Novo token de acesso
 */
export async function refreshAccessToken() {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    clearTokens();
    if (typeof window !== "undefined") {
      window.location.href = "/";
    }
    throw new Error("Token de refresh não encontrado. Faça login novamente.");
  }

  try {
    const response = await fetch(`${BASE_URL}/auth/jwt/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) {
      clearTokens();
      if (typeof window !== "undefined") {
        window.location.href = "/";
      }
      throw new Error("Falha ao renovar o token. Faça login novamente.");
    }

    const data = await response.json();
    saveTokens({ access: data.access, refresh: refreshToken });
    return data.access;
  } catch (error) {
    console.error("Erro ao renovar token:", error.message);
    clearTokens();
    if (typeof window !== "undefined") {
      window.location.href = "/";
    }
    throw error;
  }
}

/**
 * Login do usuário e obtenção de tokens JWT.
 * @param {Object} credentials { cpf, password }
 * @returns {Promise<Object>} Objeto com tokens { access, refresh }
 */
export async function login(credentials) {
  try {
    const response = await fetch(`${BASE_URL}/auth/jwt/create/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Erro no login.");
    }

    const tokens = await response.json();
    saveTokens(tokens);
    return tokens;
  } catch (error) {
    console.error("Erro no login:", error.message);
    throw error;
  }
}

/**
 * Logout do usuário (limpa os tokens armazenados).
 */
export const logout = () => clearTokens();
