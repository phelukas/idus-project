"use client";

import React, { useState, useEffect, use } from "react";
import { UserInfo } from "../../components/UserInfo";
import { LocationMap } from "../../components/LocationMap";
import { PointsList } from "../../components/PointsList";
import { DailySummary } from "../../components/DailySummary";
import { RegisterPointModal } from "../../components/RegisterPointModal";
import { EditUserModal } from "../../components/EditUserModal";
import styles from "./Page.module.css";
import {
  registerPoint,
  getDailySummary,
  registerPointManual,
  getUserInfo,
  updateUser,
} from "../../api/user";

export default function UserDetails({ params: paramsPromise }) {
  const params = use(paramsPromise);
  const { id } = params;

  const [activeTab, setActiveTab] = useState("map");
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [locationAddress, setLocationAddress] = useState("");
  const [pointMessage, setPointMessage] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [summary, setSummary] = useState(null);
  const [manualPointTime, setManualPointTime] = useState("");
  const [manualPointError, setManualPointError] = useState("");
  const [userInfo, setUserInfo] = useState(null);
  const [horaAtual, setHoraAtual] = useState("");
  const [feedbackMessage, setFeedbackMessage] = useState("");
  const [feedbackType, setFeedbackType] = useState("");

  const handleRegisterPointManual = async () => {
    if (!manualPointTime) {
      setManualPointError("Por favor, insira uma data e hora válidas.");
      return;
    }

    try {
      const response = await registerPointManual(id, manualPointTime);
      setPointMessage(
        `Ponto manual registrado com sucesso: ${new Date(
          response.timestamp
        ).toLocaleString("pt-BR")} (${
          response.type === "in" ? "Entrada" : "Saída"
        })`
      );

      const updatedSummary = await getDailySummary(id);
      setSummary(updatedSummary);

      setManualPointTime("");
      setManualPointError("");
      setShowModal(false);
    } catch (error) {
      console.error("Erro ao registrar ponto manual:", error);
      setManualPointError(
        error.response?.data?.detail || "Erro ao registrar ponto manual."
      );
    }
  };

  const handleUpdateUser = async (updatedData) => {
    try {
      const response = await updateUser(id, updatedData);
      setUserInfo({ ...userInfo, ...updatedData });
      setFeedbackMessage("Usuário atualizado com sucesso!");
      setFeedbackType("success");
      setShowEditModal(false);
    } catch (error) {
      console.error("Erro ao atualizar o usuário:", error);
      setFeedbackMessage(
        error.response?.data?.detail || "Erro ao atualizar o usuário."
      );
      setFeedbackType("error");
    }
  };

  const handleRegisterPoint = async () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          setLatitude(latitude);
          setLongitude(longitude);

          try {
            const point = await registerPoint(id, latitude, longitude);
            setPointMessage(
              `Ponto registrado com sucesso: ${new Date(
                point.timestamp
              ).toLocaleString("pt-BR")} (${
                point.type === "in" ? "Entrada" : "Saída"
              })`
            );

            const updatedSummary = await getDailySummary(id);
            setSummary(updatedSummary);
          } catch (error) {
            console.error("Erro ao registrar ponto:", error);
            setPointMessage("Erro ao registrar ponto.");
          }
        },
        (error) => {
          console.error("Erro ao obter localização:", error);
          setPointMessage(
            "Erro ao obter localização. Verifique as permissões do navegador."
          );
        }
      );
    } else {
      setPointMessage("Geolocalização não é suportada pelo navegador.");
    }
  };

  const fetchLocationAddress = async (lat, lon) => {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`
      );
      const data = await response.json();

      const { road, suburb, city, state, country } = data.address;
      const simplifiedAddress = `${road || ""}, ${suburb || ""}, ${
        city || ""
      }, ${state || ""}, ${country || ""}`;
      setLocationAddress(simplifiedAddress.trim().replace(/(^,)|(,$)/g, ""));
    } catch (error) {
      console.error("Erro ao buscar endereço:", error);
      setLocationAddress("Erro ao obter endereço.");
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userData = await getUserInfo(id);
        const dailySummary = await getDailySummary(id);

        setUserInfo(userData);
        setSummary(dailySummary);
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      }
    };

    fetchData();

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLatitude(position.coords.latitude);
          setLongitude(position.coords.longitude);
          fetchLocationAddress(
            position.coords.latitude,
            position.coords.longitude
          );
        },
        () => {
          console.warn(
            "Permissão de localização negada ou erro ao obter localização."
          );
        }
      );
    } else {
      console.warn("Geolocalização não é suportada pelo navegador.");
    }
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      const agora = new Date().toLocaleTimeString("pt-BR");
      setHoraAtual(agora);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 py-10">
      <div className="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-8 border border-gray-200">
        <h1 className="text-3xl font-bold text-black mb-6 text-center">
          Informações do Usuário
        </h1>

        {feedbackMessage && (
          <div
            className={`p-4 mb-4 text-center rounded-md ${
              feedbackType === "success"
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }`}
          >
            {feedbackMessage}
          </div>
        )}

        <div className={`${styles.tabs} flex justify-center gap-4 mb-6`}>
          <button
            onClick={() => setActiveTab("map")}
            className={`${styles.tabButton} ${
              activeTab === "map" ? styles.activeTab : ""
            } px-4 py-2 rounded-md text-sm font-semibold`}
          >
            Mapa
          </button>
          <button
            onClick={() => setActiveTab("info")}
            className={`${styles.tabButton} ${
              activeTab === "info" ? styles.activeTab : ""
            } px-4 py-2 rounded-md text-sm font-semibold`}
          >
            Informações
          </button>
          <button
            onClick={() => setActiveTab("points")}
            className={`${styles.tabButton} ${
              activeTab === "points" ? styles.activeTab : ""
            } px-4 py-2 rounded-md text-sm font-semibold`}
          >
            Pontos
          </button>
          <button
            onClick={() => setActiveTab("summary")}
            className={`${styles.tabButton} ${
              activeTab === "summary" ? styles.activeTab : ""
            } px-4 py-2 rounded-md text-sm font-semibold`}
          >
            Resumo
          </button>
        </div>

        {activeTab === "info" && userInfo && (
          <>
            <UserInfo
              user={{
                name: `${userInfo.first_name} ${userInfo.last_name}`,
                cpf: userInfo.cpf,
                email: userInfo.email,
                birthDate: new Date(userInfo.birth_date).toLocaleDateString(
                  "pt-BR"
                ),
                workload: userInfo.work_schedule,
                role:
                  userInfo.role === "admin" ? "Administrador" : "Usuário Comum",
              }}
            />
            <div className="mt-6 flex justify-center">
              <button
                onClick={() => setShowEditModal(true)}
                className="bg-yellow-500 text-white py-2 px-6 rounded hover:bg-yellow-600 transition-all shadow-md"
              >
                Editar Usuário
              </button>
            </div>
          </>
        )}

        {showEditModal && (
          <EditUserModal
            showModal={showEditModal}
            setShowModal={setShowEditModal}
            user={userInfo}
            handleUpdateUser={handleUpdateUser}
          />
        )}

        {activeTab === "map" && (
          <>
            <LocationMap latitude={latitude} longitude={longitude} />
            <div className="mt-4 flex flex-col items-center gap-4">
              <div className="flex justify-center gap-4">
                <button
                  onClick={handleRegisterPoint}
                  className="bg-blue-600 text-white py-2 px-6 rounded hover:bg-blue-700 transition-all shadow-md"
                >
                  Bater Ponto Automático
                </button>
                <button
                  onClick={() => setShowModal(true)}
                  className="bg-green-600 text-white py-2 px-6 rounded hover:bg-green-700 transition-all shadow-md"
                >
                  Bater Ponto Manual
                </button>
              </div>
              <div className="mt-4 text-center">
                <p className="text-lg font-semibold text-gray-700">
                  <span className="text-black font-bold">Hora Atual:</span>{" "}
                  {horaAtual}
                </p>
                <p className="text-lg font-semibold text-gray-700">
                  <span className="text-black font-bold">Localização:</span>{" "}
                  {locationAddress}
                </p>
              </div>
            </div>
            {pointMessage && (
              <p
                className={`mt-4 text-center font-semibold ${
                  pointMessage.includes("sucesso")
                    ? "text-green-500"
                    : "text-red-500"
                }`}
              >
                {pointMessage}
              </p>
            )}
          </>
        )}

        {showModal && (
          <RegisterPointModal
            showModal={showModal}
            setShowModal={setShowModal}
            manualPointTime={manualPointTime}
            setManualPointTime={setManualPointTime}
            handleRegisterPointManual={handleRegisterPointManual}
            manualPointError={manualPointError}
          />
        )}

        {activeTab === "points" && summary && (
          <>
            <PointsList points={summary.points} />
            <div className="mt-6 flex justify-center">
              <button
                onClick={() => (window.location.href = `/report/${id}`)}
                className="bg-blue-500 text-white py-2 px-6 rounded hover:bg-blue-600 transition-all shadow-md"
              >
                Gerar Relatório
              </button>
            </div>
          </>
        )}

        {activeTab === "summary" && summary && (
          <DailySummary summary={summary} />
        )}
      </div>
    </div>
  );
}
