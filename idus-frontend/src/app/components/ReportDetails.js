import ReportSummary from "./ReportSummary";
import ReportPoints from "./ReportPoints";

const ReportDetails = ({ report }) => (
  <div className="mt-8">
    <h2 className="text-xl font-bold text-gray-800 mb-4">Dados do Relatório</h2>

    <div className="bg-gray-50 p-4 rounded shadow-sm mb-4">
      <p className="text-gray-700">
        <span className="font-semibold">Usuário:</span>{" "}
        {`${report.user.first_name || "Nome não disponível"} ${
          report.user.last_name || ""
        }`}
      </p>
      <p className="text-gray-700">
        <span className="font-semibold">Data:</span> {report.date || ""}
      </p>
    </div>

    <ReportSummary report={report} />
    <ReportPoints points={report.points} />
  </div>
);

export default ReportDetails;
