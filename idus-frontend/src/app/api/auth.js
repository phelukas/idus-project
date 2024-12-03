import { BASE_URL } from "./config";

/**
 * Salvar tokens no localStorage com validação.
 * @param {Object} tokens { access, refresh }
 */
export function saveTokens({ access, refresh }) {
  if (access) localStorage.setItem("access_token", access);
  if (refresh) localStorage.setItem("refresh_token", refresh);
}

/**
 * Obter token de acesso.
 * @returns {string|null} Token de acesso
 */
export const getAccessToken = () => localStorage.getItem("access_token");

/**
 * Obter token de refresh.
 * @returns {string|null} Token de refresh
 */
export const getRefreshToken = () => localStorage.getItem("refresh_token");

/**
 * Limpar tokens (logout).
 */
export const clearTokens = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

/**
 * Renovar token de acesso usando o token de refresh.
 * @returns {Promise<string>} Novo token de acesso
 */
export async function refreshAccessToken() {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
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
      throw new Error("Falha ao renovar o token. Faça login novamente.");
    }

    const data = await response.json();
    saveTokens({ access: data.access, refresh: refreshToken });
    return data.access;
  } catch (error) {
    console.error("Erro ao renovar token:", error.message);
    clearTokens();
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
