const DateInput = ({
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  handleFetchReport,
}) => (
  <div>
    <div className="mb-4">
      <label
        htmlFor="start-date"
        className="block text-gray-700 font-semibold mb-2"
      >
        Data de Início
      </label>
      <input
        type="date"
        id="start-date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
        className="w-full px-3 py-2 border border-gray-900 rounded bg-white"
        style={{
          color: "black",
          backgroundColor: "white",
        }}
      />
    </div>

    <div className="mb-4">
      <label
        htmlFor="end-date"
        className="block text-gray-700 font-semibold mb-2"
      >
        Data de Fim
      </label>
      <input
        type="date"
        id="end-date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
        className="w-full px-3 py-2 border border-gray-900 rounded bg-white"
        style={{
          color: "black",
          backgroundColor: "white",
        }}
      />
    </div>

    <button
      onClick={handleFetchReport}
      className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
    >
      Buscar Relatório
    </button>
  </div>
);

export default DateInput;
