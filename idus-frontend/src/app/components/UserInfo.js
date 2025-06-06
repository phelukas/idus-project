export function UserInfo({ user }) {
  return (
    <div className="mb-8 bg-gray-50 p-4 rounded-lg shadow">
      <p className="text-lg text-gray-800">
        <span className="font-semibold">Nome Completo:</span> {user.name}
      </p>
      <p className="text-lg text-gray-800">
        <span className="font-semibold">CPF:</span> {user.cpf}
      </p>
      <p className="text-lg text-gray-800">
        <span className="font-semibold">E-mail:</span> {user.email}
      </p>
      <p className="text-lg text-gray-800">
        <span className="font-semibold">Data de Nascimento:</span>{" "}
        {user.birthDate}
      </p>
      <p className="text-lg text-gray-800">
        <span className="font-semibold">Jornada de Trabalho:</span>{" "}
        {user.workload}
      </p>
      <p className="text-lg text-gray-800">
        <span className="font-semibold">Cargo:</span>{" "}
        {user.role === "admin" ? "Administrador" : "Usuário Comum"}
      </p>
    </div>
  );
}
