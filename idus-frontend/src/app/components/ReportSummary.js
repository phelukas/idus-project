const ReportSummary = ({ report }) => (
  <div className="bg-gray-50 p-4 rounded shadow-sm mb-4">
    <h3 className="text-lg font-bold text-gray-800 mb-3">Resumo da Jornada</h3>
    <p className="text-gray-700">
      <span className="font-semibold">Total Trabalhado:</span>{" "}
      {report.total_worked?.split(".")[0] || "Não disponível"} horas
    </p>
    <p className="text-gray-700">
      <span className="font-semibold">Horas Restantes:</span>{" "}
      {report.remaining_hours?.split(".")[0] || "Não disponível"} horas
    </p>
    <p className="text-gray-700">
      <span className="font-semibold">Horas Extras:</span>{" "}
      {report.extra_hours || "Não disponível"}
    </p>
    <p className="text-gray-700">
      <span className="font-semibold">Jornada Completa:</span>{" "}
      {report.is_complete ? "Sim" : "Não"}
    </p>
  </div>
);

export default ReportSummary;
