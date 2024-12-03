export function Actions({
  summary,
  handleRegisterPoint,
  handleViewReport,
  setShowModal,
  setShowEditModal, // Nova prop
}) {
  return (
    <div className="flex justify-around mt-8">
      <button
        onClick={handleRegisterPoint}
        className={`bg-blue-500 text-white py-2 px-6 rounded hover:bg-blue-600 transition-colors ${
          summary?.all_points_registered
            ? "opacity-50 cursor-not-allowed"
            : ""
        }`}
        disabled={summary?.all_points_registered}
      >
        Bater Ponto Automático
      </button>
      <button
        onClick={() => setShowModal(true)}
        className="bg-green-500 text-white py-2 px-6 rounded hover:bg-green-600 transition-colors"
      >
        Bater Ponto Manual
      </button>
      <button
        onClick={handleViewReport}
        className="bg-purple-500 text-white py-2 px-6 rounded hover:bg-purple-600 transition-colors"
      >
        Ver Relatório
      </button>
      <button
        onClick={() => setShowEditModal(true)}
        className="bg-yellow-500 text-white py-2 px-6 rounded hover:bg-yellow-600 transition-colors"
      >
        Editar Usuário
      </button>
    </div>
  );
}
