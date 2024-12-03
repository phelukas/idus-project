import React, { useState, useEffect, use } from "react";
import { useRouter } from "next/navigation";
import {
  getUserInfo,
  registerPoint,
  registerPointManual,
  getDailySummary,
} from "../../api/user";
import { UserInfo } from "./UserInfo";
import { DailySummary } from "./DailySummary";
import { PointsList } from "./PointsList";
import { RegisterPointModal } from "./RegisterPointModal";
import { Actions } from "./Actions";

export default function UserDetails({ params: paramsPromise }) {
  const params = use(paramsPromise);
  const { id } = params;
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [summary, setSummary] = useState(null);
  const [pointMessage, setPointMessage] = useState("");
  const [manualPointTime, setManualPointTime] = useState("");
  const [manualPointError, setManualPointError] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const userData = await getUserInfo(id);

        if (userData.id !== parseInt(id, 10)) {
          router.push(`/user/${userData.id}`);
          return;
        }

        const dailySummary = await getDailySummary(id);
        setUser(userData);
        setSummary(dailySummary);
      } catch (err) {
        setError("Erro ao carregar informações do usuário e resumo diário.");
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchData();
    }
  }, [id]);

  const handleRegisterPoint = async () => {
    try {
      const point = await registerPoint(id);
      setPointMessage(
        `Ponto registrado com sucesso: ${new Date(
          point.timestamp
        ).toLocaleString("pt-BR")} (${
          point.type === "in" ? "Entrada" : "Saída"
        })`
      );
      const updatedSummary = await getDailySummary(id);
      setSummary(updatedSummary);
    } catch {
      setPointMessage("Erro ao registrar ponto.");
    }
  };

  const handleRegisterPointManual = async () => {
    if (!manualPointTime) {
      setManualPointError("Por favor, insira uma data e hora válidas.");
      return;
    }

    const now = new Date();
    const manualTime = new Date(manualPointTime);

    if (manualTime > now) {
      setManualPointError("A hora não pode ser no futuro.");
      return;
    }

    try {
      const point = await registerPointManual(id, manualPointTime);
      setPointMessage(
        `Ponto manual registrado com sucesso: ${manualTime.toLocaleString(
          "pt-BR"
        )}`
      );
      setManualPointError("");
      const updatedSummary = await getDailySummary(id);
      setSummary(updatedSummary);
      setShowModal(false);
    } catch {
      setManualPointError("Erro ao registrar ponto manual.");
    }
  };

  const handleViewReport = () => {
    router.push(`/report/${id}`);
  };

  if (loading) return <p>Carregando...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="min-h-screen bg-gray-100 py-10">
      <div className="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-8 border border-gray-200">
        <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">
          Informações do Usuário
        </h1>
        {user && <UserInfo user={user} />}
        {summary && <PointsList points={summary.points} />}
        {summary && <DailySummary summary={summary} />}
        <Actions
          summary={summary}
          handleRegisterPoint={handleRegisterPoint}
          handleViewReport={handleViewReport}
          setShowModal={setShowModal}
        />
        {pointMessage && (
          <p className="mt-4 text-center text-green-600 font-semibold">
            {pointMessage}
          </p>
        )}
        <RegisterPointModal
          showModal={showModal}
          setShowModal={setShowModal}
          manualPointTime={manualPointTime}
          setManualPointTime={setManualPointTime}
          handleRegisterPointManual={handleRegisterPointManual}
          manualPointError={manualPointError}
        />
      </div>
    </div>
  );
}
