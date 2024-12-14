"use client";

import dynamic from "next/dynamic";
import React from "react";

// Carregar dinamicamente o componente para evitar SSR
const DynamicMap = dynamic(() => import("./DynamicMap"), { ssr: false });

export function LocationMap({ latitude, longitude }) {
    if (!latitude || !longitude) {
        return <p>Localização não disponível.</p>;
    }

    return <DynamicMap latitude={latitude} longitude={longitude} />;
}
