import { BASE_URL } from "./config";
import { getAccessToken, refreshAccessToken } from "./auth";

/**
 * Requisição genérica para a API.
 * @param {string} endpoint Caminho da API (ex: "/users/list/")
 * @param {string} method Método HTTP (GET, POST, PUT, DELETE)
 * @param {Object} [body] Corpo da requisição (opcional)
 * @returns {Promise<Object>} Resposta da API em JSON
 */
async function apiRequest(endpoint, method, body = null) {
  let token = getAccessToken();

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };

  try {
    let response = await fetch(`${BASE_URL}${endpoint}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
    });

    if (response.status === 401) {
      console.warn("Token expirado. Tentando renovar...");
      token = await refreshAccessToken();
      headers.Authorization = `Bearer ${token}`;

      response = await fetch(`${BASE_URL}${endpoint}`, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null,
      });
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw {
        response: {
          status: response.status,
          data: errorData,
        },
      };
    }

    return response.headers.get("Content-Type")?.includes("json")
      ? await response.json()
      : { message: "Operação concluída com sucesso." };
  } catch (error) {
    console.error(
      `Erro na requisição [${method} ${endpoint}]:`,
      error.response?.data || error.message
    );
    throw error;
  }
}

export const listUsers = () => apiRequest("/users/list/", "GET");

export const updateUser = (id, data) =>
  apiRequest(`/users/update/${id}/`, "PUT", data);

export const deleteUser = (id) => apiRequest(`/users/delete/${id}/`, "DELETE");

export const registerPoint = (id) =>
  apiRequest(`/workpoints/${id}/register-point/`, "POST");

export const getDailySummary = (id = null) =>
  apiRequest(id ? `/summary/${id}/` : "/summary/", "GET");

export const fetchUsers = () => apiRequest("/users/list/", "GET");

export const getUserInfo = (id = null) =>
  apiRequest(id ? `/users/info/${id}/` : "/users/info/", "GET");

export const createUser = (data) => apiRequest("/users/create/", "POST", data);

export const registerPointManual = (userId, timestamp) =>
  apiRequest(`/workpoints/${userId}/register-point-manual/`, "POST", {
    timestamp,
  });

export const getWorkPointReport = (userId, date) =>
  apiRequest(`/workpoints/report/${userId}/?date=${date}`, "GET");

export const downloadWorkPointPDF = async (userId, date) => {
  const token = getAccessToken();

  const headers = {
    Authorization: `Bearer ${token}`,
  };

  try {
    const response = await fetch(
      `${BASE_URL}/workpoints/report/${userId}/pdf/?date=${date}`,
      {
        method: "GET",
        headers,
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Erro ao gerar o relatório em PDF.");
    }

    const blob = await response.blob(); // Obtém o arquivo PDF como blob
    const url = window.URL.createObjectURL(blob); // Cria uma URL temporária para o arquivo
    const link = document.createElement("a");
    link.href = url;
    link.download = `relatorio_${userId}_${date}.pdf`; // Nome do arquivo
    link.click(); // Inicia o download
    window.URL.revokeObjectURL(url); // Revoga a URL temporária após o uso
  } catch (error) {
    console.error("Erro ao baixar PDF:", error.message);
    throw error;
  }
};
