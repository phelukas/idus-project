const ReportPoints = ({ points }) => (
  <div className="bg-gray-50 p-4 rounded shadow-sm">
    <h3 className="text-lg font-bold text-gray-800 mb-3">Pontos Registrados</h3>
    <ul className="space-y-2">
      {points.length > 0 ? (
        points.map((point, index) => (
          <li key={index} className="text-gray-700">
            <span className="font-semibold">Horário:</span> {point.timestamp} -{" "}
            {point.type === "in" ? "Entrada" : "Saída"}
          </li>
        ))
      ) : (
        <li className="text-gray-700 text-center">
          Nenhum ponto registrado para esta data.
        </li>
      )}
    </ul>
  </div>
);

export default ReportPoints;
