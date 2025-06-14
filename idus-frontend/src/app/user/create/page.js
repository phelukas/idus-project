"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { createUser } from "../../api/user";
import CreateUserForm from "../../components/CreateUserForm";
import ErrorMessage from "../../components/ErrorMessage";
import SuccessMessage from "../../components/SuccessMessage";

const CreateUser = () => {
  const [formData, setFormData] = useState({
    cpf: "",
    email: "",
    first_name: "",
    last_name: "",
    birth_date: "",
    password: "",
    role: "common",
    scale: "5x1",
  });

  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const sanitizedData = {
        ...formData,
        cpf: formData.cpf.replace(/[^\d]/g, ""),
      };

      const response = await createUser(sanitizedData);
      setSuccess("Usuário criado com sucesso!");
      setError(null);
      setTimeout(() => router.push("/dashboard"), 2000);
    } catch (err) {
      const isFormError =
        err.response?.data?.errors &&
        typeof err.response.data.errors === "object";
      const errorDetails = isFormError ? err.response.data.errors : null;
      setError(errorDetails);
      setSuccess(null);

      if (!isFormError) {
        console.error(
          "Erro não relacionado ao formulário:",
          err.response || err.message
        );
      }
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10">
      <div className="max-w-md mx-auto bg-white shadow-md rounded-lg p-6 border border-gray-200">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Criar Novo Usuário
        </h1>
        <CreateUserForm
          formData={formData}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
        />
        <ErrorMessage errors={error} />
        {success && <SuccessMessage message={success} />}
      </div>
    </div>
  );
};

export default CreateUser;
