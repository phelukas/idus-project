"use client";

import React, { useState } from "react";
import { getWorkPointReport, downloadWorkPointPDF } from "../api/user";
import { useParams } from "next/navigation";
import DateInput from "../components/DateInput";
import ErrorMessage from "../components/ErrorMessage";
import ReportDetails from "../components/ReportDetails";

const WorkPointReport = () => {
  const { id } = useParams();

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const validateInputs = () => {
    if (!id) {
      setError("ID de usuário inválido.");
      return false;
    }

    if (!startDate || !endDate) {
      setError("Por favor, insira datas válidas no formato YYYY-MM-DD.");
      return false;
    }

    if (startDate > endDate) {
      setError("A data de início não pode ser maior que a data de fim.");
      return false;
    }

    return true;
  };

  const handleFetchReport = async () => {
    if (!validateInputs()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await getWorkPointReport(id, { startDate, endDate });
      setReport(data);
    } catch {
      setError(
        "Erro ao buscar relatório. Verifique as datas ou tente novamente."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!validateInputs()) return;

    setLoading(true);
    setError(null);

    try {
      await downloadWorkPointPDF(id, { startDate, endDate });
    } catch {
      setError(
        "Erro ao baixar o relatório em PDF. Verifique as datas ou tente novamente."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10">
      <div className="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6 border border-gray-200">
        <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">
          Relatório de Pontos
        </h1>

        <DateInput
          startDate={startDate}
          setStartDate={setStartDate}
          endDate={endDate}
          setEndDate={setEndDate}
          handleFetchReport={handleFetchReport}
        />

        {loading && (
          <p className="mt-6 text-gray-600 text-center">Carregando...</p>
        )}
        {error && <ErrorMessage message={error} />}
        {report && <ReportDetails report={report} />}

        {report && (
          <div className="mt-6 flex justify-center">
            <button
              className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700"
              onClick={handleDownloadPDF}
              disabled={loading}
            >
              Baixar Relatório em PDF
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkPointReport;
