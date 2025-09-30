import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const data = {
  labels: Array.from({ length: 20 }, (_, i) => i + 1),
  datasets: [
    {
      label: 'Dados 1',
      data: Array.from({ length: 20 }, () => Math.random() * 100),
      borderColor: '#4dc0b5',
      backgroundColor: 'rgba(77, 192, 181, 0.2)',
      tension: 0.3
    },
    {
      label: 'Dados 2',
      data: Array.from({ length: 20 }, () => Math.random() * 80 + 20),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.2)',
      tension: 0.3
    },
  ],
};

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    decimation: {
      enabled: true,
      algorithm: 'lttb',
      samples: 10
    },
  },
  scales: {
    x: { display: true, title: { display: true, text: 'Eixo X' } },
    y: { display: true, title: { display: true, text: 'Eixo Y' } },
  },
};

export default function MultiLineChart() {
  return <Line data={data} options={options} />;
}