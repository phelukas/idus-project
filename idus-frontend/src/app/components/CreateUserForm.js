import React from "react";
import FormField from "./FormField";

const CreateUserForm = ({ formData, handleInputChange, handleSubmit }) => (
  <form onSubmit={handleSubmit}>
    <FormField
      label="CPF"
      id="cpf"
      name="cpf"
      type="text"
      value={formData.cpf}
      onChange={handleInputChange}
      required
    />
    <FormField
      label="Email"
      id="email"
      name="email"
      type="email"
      value={formData.email}
      onChange={handleInputChange}
      required
    />
    <FormField
      label="Primeiro Nome"
      id="first_name"
      name="first_name"
      type="text"
      value={formData.first_name}
      onChange={handleInputChange}
      required
    />
    <FormField
      label="Sobrenome"
      id="last_name"
      name="last_name"
      type="text"
      value={formData.last_name}
      onChange={handleInputChange}
      required
    />
    <FormField
      label="Data de Nascimento"
      id="birth_date"
      name="birth_date"
      type="date"
      value={formData.birth_date}
      onChange={handleInputChange}
      required
    />
    <FormField
      label="Senha"
      id="password"
      name="password"
      type="password"
      value={formData.password}
      onChange={handleInputChange}
      required
    />
    <FormField
      label="Cargo"
      id="role"
      name="role"
      type="select"
      options={[
        { value: "common", label: "Usuário Comum" },
        { value: "admin", label: "Administrador" },
      ]}
      value={formData.role}
      onChange={handleInputChange}
    />
    <FormField
      label="Escala"
      id="scale"
      name="scale"
      type="select"
      options={[
        { value: "5x1", label: "Tradicional (5x1)" },
        { value: "6x1", label: "6x1" },
        { value: "12x36", label: "12x36" },
        { value: "4h", label: "4 horas diárias (Estagiário)" },
        { value: "6h", label: "6 horas diárias (Aprendiz)" },
      ]}
      value={formData.scale}
      onChange={handleInputChange}
      required
    />
    <button
      type="submit"
      className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
    >
      Criar Usuário
    </button>
  </form>
);

export default CreateUserForm;
