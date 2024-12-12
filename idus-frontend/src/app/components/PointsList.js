export function PointsList({ points }) {
  return (
    <div className="mb-6 bg-gray-50 p-4 rounded-lg shadow">
      <h3 className="text-lg font-bold text-gray-800 mb-3">Seus Pontos</h3>
      <ul className="divide-y divide-gray-300">
        {points.length > 0 ? (
          points.map((point, index) => (
            <li key={index} className="py-2 text-gray-700">
              {new Date(point.timestamp).toLocaleString("pt-BR")} -{" "}
              {point.type === "in" ? "Entrada" : "Saída"}{" "}
              <span className="italic">({point.weekday})</span>
            </li>
          ))
        ) : (
          <p className="text-center text-gray-500 mt-4">
            Nenhum ponto registrado hoje.
          </p>
        )}
      </ul>
    </div>
  );
}
