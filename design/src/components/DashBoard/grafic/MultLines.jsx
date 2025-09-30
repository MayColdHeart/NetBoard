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

export default function MultiLineChart({ trafficHistory }) {
  const labels = trafficHistory.map(w => 
    new Date(w.createdAt).toLocaleTimeString()
  );

  const data = {
    labels,
    datasets: [
      {
        label: 'Upload (Kbps)',
        data: trafficHistory.map(w => w.uploadSizeKbps),
        borderColor: '#4dc0b5',
        backgroundColor: 'rgba(77, 192, 181, 0.2)',
        tension: 0.3
      },
      {
        label: 'Download (Kbps)',
        data: trafficHistory.map(w => w.downloadSizeKbps),
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        tension: 0.3
      },
      {
        label: 'Total (Kbps)',
        data: trafficHistory.map(w => w.totalSizeKbps),
        borderColor: '#f87171',
        backgroundColor: 'rgba(248, 113, 113, 0.2)',
        tension: 0.3
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
    },
    scales: {
      x: { title: { display: true, text: 'Tempo' } },
      y: { title: { display: true, text: 'Kbps' } },
    },
  };

  return <Line data={data} options={options} />;
}
