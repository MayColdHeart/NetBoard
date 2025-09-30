import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const COLORS = ["red", "blue", "green"];
const PROTOCOLS = ["FTP", "HTTP", "FTP-DATA"]; // ou os três que você usa

const PieChart = ({ trafficData }) => {
  // Soma totalSizeKbps por protocolo
  const dataMap = PROTOCOLS.map(proto => {
    const total = trafficData
      .filter(item => item.protocol === proto)
      .reduce((sum, item) => sum + item.totalSizeKbps, 0);
    return total;
  });

  const data = {
    labels: PROTOCOLS,
    datasets: [
      {
        label: "Tráfego por protocolo (Kbps)",
        data: dataMap,
        backgroundColor: COLORS,
        borderColor: ["#fff", "#fff", "#fff"],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
    },
  };

  return <Pie data={data} options={options} />;
};

export default PieChart;