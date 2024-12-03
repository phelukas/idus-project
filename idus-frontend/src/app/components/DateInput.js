const DateInput = ({ reportDate, setReportDate, handleFetchReport }) => (
  <div>
    <div className="mb-4">
      <label
        htmlFor="report-date"
        className="block text-gray-700 font-semibold mb-2"
      >
        Data do Relatório
      </label>
      <input
        type="date"
        id="report-date"
        value={reportDate}
        onChange={(e) => setReportDate(e.target.value)}
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
