import { BASE_URL } from "./config";
import { refreshAccessToken } from "./auth";

/**
 * Requisição genérica para a API.
 * @param {string} endpoint Caminho da API (ex: "/users/list/")
 * @param {string} method Método HTTP (GET, POST, PUT, DELETE)
 * @param {Object} [body] Corpo da requisição (opcional)
 * @returns {Promise<Object>} Resposta da API em JSON
 */
async function apiRequest(endpoint, method, body = null) {
  const headers = {
    "Content-Type": "application/json",
  };

  try {
    let response = await fetch(`${BASE_URL}${endpoint}`, {
      method,
      headers,
      credentials: "include",
      body: body ? JSON.stringify(body) : null,
    });

    if (response.status === 401) {
      console.warn("Token expirado. Tentando renovar...");
      await refreshAccessToken();
      response = await fetch(`${BASE_URL}${endpoint}`, {
        method,
        headers,
        credentials: "include",
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

export const registerPoint = (id, latitude, longitude) =>
  apiRequest(`/workpoints/${id}/register-point/`, "POST", {
    latitude,
    longitude,
  });

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

export const getWorkPointReport = (userId, { startDate, endDate }) =>
  apiRequest(
    `/workpoints/report/${userId}/?start_date=${startDate}&end_date=${endDate}`,
    "GET"
  );

export const downloadWorkPointPDF = async (userId, { startDate, endDate }) => {
  const headers = {};

  try {
    const response = await fetch(
      `${BASE_URL}/workpoints/report/${userId}/pdf/?start_date=${startDate}&end_date=${endDate}`,
      {
        method: "GET",
        headers,
        credentials: "include",
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Erro ao gerar o relatório em PDF.");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `relatorio_${userId}_${startDate}_to_${endDate}.pdf`;
    link.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Erro ao baixar PDF:", error.message);
    throw error;
  }
};
