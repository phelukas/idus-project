export function DailySummary({ summary }) {
    return (
      <div className="mb-8">
        <div className="mb-6 bg-gray-50 p-4 rounded-lg shadow">
          <h3 className="text-lg font-bold text-gray-800 mb-3">Resumo da Jornada</h3>
          <p className="text-gray-800">
            <span className="font-semibold">Total Trabalhado:</span>{" "}
            {summary.total_worked}
          </p>
          <p className="text-gray-800">
            <span className="font-semibold">Horas Restantes:</span>{" "}
            {summary.remaining_hours}
          </p>
          <p className="text-gray-800">
            <span className="font-semibold">Horas Extras:</span>{" "}
            {summary.extra_hours}
          </p>
        </div>
      </div>
    );
  }
  