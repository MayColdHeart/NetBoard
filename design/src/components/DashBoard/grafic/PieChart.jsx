import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const PieChart = () => {
  const data = {
    labels: ["Vermelho", "Azul", "Verde"],
    datasets: [
      {
        label: "Meu Gráfico de Pizza",
        data: [300, 50, 100],
        backgroundColor: ["red", "blue", "green"],
        borderColor: ["#fff", "#fff", "#fff"],
        borderWidth: 1,
      },
    ],
  };
    
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
    },
  };

  return <Pie data={data} options={options} />;
};

export default PieChart;