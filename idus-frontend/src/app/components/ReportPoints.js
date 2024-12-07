const ReportPoints = ({ points }) => (
  <div className="bg-gray-50 p-4 rounded shadow-sm">
    <h3 className="text-lg font-bold text-gray-800 mb-3">Pontos Registrados</h3>
    {points.length > 0 ? (
      <table className="w-full border-collapse border border-gray-200 text-sm text-black">
        <thead>
          <tr className="bg-gray-100">
            <th className="border border-gray-300 px-2 py-1 text-left">Data</th>
            <th className="border border-gray-300 px-2 py-1 text-left">Dia</th>
            <th className="border border-gray-300 px-2 py-1 text-left">
              Horários
            </th>
          </tr>
        </thead>
        <tbody>
          {points.map((point, index) => (
            <tr key={index} className="even:bg-gray-50">
              <td className="border border-gray-300 px-2 py-1 text-black">
                {point.date_point}
              </td>
              <td className="border border-gray-300 px-2 py-1 italic text-black">
                {point.weekday}
              </td>
              <td className="border border-gray-300 px-2 py-1 text-black">
                {point.timestamp.length > 0 ? (
                  <div>
                    {point.timestamp.map((entry, i) => (
                      <span key={i}>
                        {entry.time} -{" "}
                        {entry.type === "in" ? "Entrada" : "Saída"}
                        {i < point.timestamp.length - 1 && ", "}
                      </span>
                    ))}
                  </div>
                ) : (
                  <span className="italic text-gray-600">
                    Nenhum ponto registrado
                  </span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    ) : (
      <p className="text-gray-700 text-center">
        Nenhum ponto registrado para o período.
      </p>
    )}
  </div>
);

export default ReportPoints;
