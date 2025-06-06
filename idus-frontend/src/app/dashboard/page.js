"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchUsers } from "../api/user";
import { logout as removeTokens } from "../api/auth";

export default function Dashboard() {
  const [users, setUsers] = useState([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const response = await fetchUsers();

        if (response?.data && Array.isArray(response.data)) {
          setUsers(response.data);
          setIsAdmin(true);
        } else if (typeof response === "object" && response !== null) {
          setUsers([response.data]);
          setIsAdmin(false);
        } else {
          setUsers([]);
          setIsAdmin(false);
        }
      } catch (error) {
        console.error("Erro ao carregar usuários:", error.message);
      }
    };

    loadUsers();
  }, []);

  const handleUserClick = (userId) => {
    router.push(`/user/${userId}`);
  };

  const handleCreateUser = () => {
    router.push("/user/create");
  };

  const handleLogout = () => {
    removeTokens();
    router.push("/");
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">
            {isAdmin ? "Usuários" : "Suas Informações"}
          </h1>
          <div className="flex space-x-4">
            {isAdmin && (
              <button
                onClick={handleCreateUser}
                className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
              >
                Criar Novo Usuário
              </button>
            )}
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {users.map((user, index) => (
            <div
              key={user.id || index}
              className="bg-white shadow-md rounded-lg p-6 border border-gray-200 cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => handleUserClick(user.id)}
            >
              <h2 className="text-xl font-semibold text-gray-800 mb-2">
                {`${user.first_name || "Nome não disponível"} ${
                  user.last_name || ""
                }`}
              </h2>
              <p className="text-gray-600">
                <span className="font-semibold">Cargo:</span>{" "}
                {user.role === "admin" ? "Administrador" : "Usuário Comum"}
              </p>
              <p className="text-gray-600">
                <span className="font-semibold">Jornada:</span>{" "}
                {user.work_schedule || "Indisponível"}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
