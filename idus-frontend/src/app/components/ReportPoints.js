import React from "react";

const ReportPoints = ({ points }) => {
  const formattedPoints = points.map((point) => {
    const datePoint = new Date(point.timestamp).toLocaleDateString("pt-BR");
    const timePoint = new Date(point.timestamp).toLocaleTimeString("pt-BR", {
      hour: "2-digit",
      minute: "2-digit",
    });

    return {
      date_point: datePoint,
      weekday: point.weekday,
      time: timePoint,
      type: point.type,
    };
  });

  const groupedPoints = formattedPoints.reduce((acc, point) => {
    const date = point.date_point;
    if (!acc[date]) {
      acc[date] = { weekday: point.weekday, timestamp: [] };
    }
    acc[date].timestamp.push({ time: point.time, type: point.type });
    return acc;
  }, {});

  const groupedPointsArray = Object.keys(groupedPoints).map((date) => ({
    date_point: date,
    weekday: groupedPoints[date].weekday,
    timestamp: groupedPoints[date].timestamp,
  }));

  return (
    <div className="bg-gray-50 p-4 rounded shadow-sm">
      <h3 className="text-lg font-bold text-gray-800 mb-3">
        Pontos Registrados
      </h3>
      {groupedPointsArray.length > 0 ? (
        <table className="w-full border-collapse border border-gray-200 text-sm text-black">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 px-2 py-1 text-left">
                Data
              </th>
              <th className="border border-gray-300 px-2 py-1 text-left">
                Dia
              </th>
              <th className="border border-gray-300 px-2 py-1 text-left">
                Horários
              </th>
            </tr>
          </thead>
          <tbody>
            {groupedPointsArray.map((point, index) => (
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
};

export default ReportPoints;
