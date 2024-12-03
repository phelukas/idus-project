import React, { useState, useRef, useEffect } from "react";
import styles from "./EditUserModal.module.css";
import ErrorMessage from "./ErrorMessage";

export function EditUserModal({
  showModal,
  setShowModal,
  user,
  handleUpdateUser,
}) {
  const [formData, setFormData] = useState({
    first_name: user?.first_name || "",
    last_name: user?.last_name || "",
    email: user?.email || "",
    cpf: user?.cpf || "",
    birth_date: user?.birth_date || "",
    work_schedule: user?.work_schedule || "8h",
  });

  const [formErrors, setFormErrors] = useState(null);
  const modalRef = useRef(null);

  const resetForm = () => {
    setFormData({
      first_name: user?.first_name || "",
      last_name: user?.last_name || "",
      email: user?.email || "",
      cpf: user?.cpf || "",
      birth_date: user?.birth_date || "",
      work_schedule: user?.work_schedule || "8h",
    });
    setFormErrors(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await handleUpdateUser(formData);
      setFormErrors(null);
      setShowModal(false);
    } catch (err) {
      const isFormError =
        err.response?.data?.errors &&
        typeof err.response.data.errors === "object";
      const errorDetails = isFormError ? err.response.data.errors : null;

      setFormErrors(errorDetails);

      if (!isFormError) {
        console.error("Erro inesperado:", err.response || err.message);
      }

      return;
    }
  };

  const handleClickOutside = (event) => {
    if (modalRef.current && !modalRef.current.contains(event.target)) {
      resetForm();
      setShowModal(false);
    }
  };

  useEffect(() => {
    if (showModal) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showModal]);

  const handleClose = () => {
    resetForm();
    setShowModal(false);
  };

  if (!showModal) return null;

  return (
    <div className={styles["modal-overlay"]}>
      <div ref={modalRef} className={styles["modal-container"]}>
        <button onClick={handleClose} className={styles["close-button"]}>
          ✕
        </button>
        <h2 className="text-lg font-bold mb-4 text-gray-800 text-center">
          Editar Usuário
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              className="block text-gray-700 font-semibold mb-2"
              htmlFor="first_name"
            >
              Primeiro Nome
            </label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-black rounded text-black"
              required
            />
          </div>
          <div>
            <label
              className="block text-gray-700 font-semibold mb-2"
              htmlFor="last_name"
            >
              Sobrenome
            </label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-black rounded text-black"
              required
            />
          </div>
          <div>
            <label
              className="block text-gray-700 font-semibold mb-2"
              htmlFor="email"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-black rounded text-black"
              required
            />
          </div>
          <div>
            <label
              className="block text-gray-700 font-semibold mb-2"
              htmlFor="cpf"
            >
              CPF
            </label>
            <input
              type="text"
              id="cpf"
              name="cpf"
              value={formData.cpf}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-black rounded text-black"
              required
            />
          </div>
          <div>
            <label
              className="block text-gray-700 font-semibold mb-2"
              htmlFor="birth_date"
            >
              Data de Nascimento
            </label>
            <input
              type="date"
              id="birth_date"
              name="birth_date"
              value={formData.birth_date}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-black rounded text-black"
              required
            />
          </div>
          <div>
            <label
              className="block text-gray-700 font-semibold mb-2"
              htmlFor="work_schedule"
            >
              Jornada de Trabalho
            </label>
            <select
              id="work_schedule"
              name="work_schedule"
              value={formData.work_schedule}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-black rounded text-black"
            >
              <option value="6h">6 Horas</option>
              <option value="8h">8 Horas</option>
            </select>
          </div>
          <ErrorMessage errors={formErrors}></ErrorMessage>
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={handleClose}
              className="bg-gray-300 text-gray-800 py-2 px-4 rounded hover:bg-gray-400 focus:outline-none"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none"
            >
              Salvar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
