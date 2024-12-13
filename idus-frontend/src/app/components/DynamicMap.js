"use client";

import React, { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

export default function DynamicMap({ latitude, longitude }) {
  useEffect(() => {
    const mapContainer = document.getElementById("map");
    if (mapContainer._leaflet_id) {
      return;
    }

    const map = L.map("map").setView([latitude, longitude], 15);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors',
    }).addTo(map);

    L.marker([latitude, longitude]).addTo(map).openPopup();

    return () => {
      map.remove();
    };
  }, [latitude, longitude]);

  return <div id="map" style={{ height: "300px", width: "100%" }} />;
}
