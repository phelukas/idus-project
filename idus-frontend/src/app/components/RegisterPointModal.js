export function RegisterPointModal({
    showModal,
    setShowModal,
    manualPointTime,
    setManualPointTime,
    handleRegisterPointManual,
    manualPointError,
  }) {
    if (!showModal) return null;
  
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <div className="bg-white p-6 rounded-lg shadow-lg w-96">
          <h2 className="text-lg font-bold mb-4 text-gray-800 text-center">
            Registrar Ponto Manual
          </h2>
          <input
            type="datetime-local"
            value={manualPointTime}
            onChange={(e) => setManualPointTime(e.target.value)}
            max={new Date().toISOString().slice(0, 16)}
            className="w-full px-3 py-2 border border-gray-800 rounded mb-4 text-gray-800"
          />
          {manualPointError && (
            <p className="text-red-600 text-sm mb-4">{manualPointError}</p>
          )}
          <div className="flex justify-end space-x-4">
            <button
              onClick={() => setShowModal(false)}
              className="bg-gray-300 text-gray-800 py-2 px-4 rounded hover:bg-gray-400"
            >
              Cancelar
            </button>
            <button
              onClick={handleRegisterPointManual}
              className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
            >
              Registrar
            </button>
          </div>
        </div>
      </div>
    );
  }
  