import './GlobalStyles.css'
import axios from 'axios';
import { API_URL } from './consts/urls';
import { useEffect, useRef, useState } from 'react';
import * as signalR from '@microsoft/signalr';

/*Importando componentes*/
import Aside from './components/Aside/Aside'
import DashBoard from './components/DashBoard/DashBoard'
import Control from './components/Control/Control'

function App() {
  const [trafficData, setTrafficData] = useState([]);
  const [trafficHistory, setTrafficHistory] = useState([]);

  const connectionRef = useRef(null);

  // Busca inicial via GET
  useEffect(() => {
    async function fetchInitialTraffic() {
      try {
        const { data } = await axios.get(`${API_URL}/network/traffic`);
        setTrafficData(data);
        console.log("Initial traffic data:", data);
      } catch (err) {
        console.error('Error fetching initial traffic:', err);
      }
    }
    fetchInitialTraffic();
  }, []);

  // Conexão SignalR
  useEffect(() => {
    if (connectionRef.current) return;

    const connection = new signalR.HubConnectionBuilder()
      .withUrl(`${API_URL}/network-hub`)
      .withAutomaticReconnect()
      .build();

    connectionRef.current = connection;

    const handleTraffic = (trafficWindow) => {
      console.log('TrafficWindow received:', trafficWindow);
      setTrafficData(prevData => {
        const index = prevData.findIndex(
          item => item.deviceIp === trafficWindow.deviceIp && item.protocol === trafficWindow.protocol
        );

        if (index >= 0) {
          const updated = [...prevData];
          updated[index] = {
            ...updated[index],
            totalSizeKbps: updated[index].totalSizeKbps + trafficWindow.totalSizeKbps,
            uploadSizeKbps: updated[index].uploadSizeKbps + trafficWindow.uploadSizeKbps,
            downloadSizeKbps: updated[index].downloadSizeKbps + trafficWindow.downloadSizeKbps
          };
          return updated;
        } else {
          return [...prevData, {
            deviceIp: trafficWindow.deviceIp,
            protocol: trafficWindow.protocol,
            totalSizeKbps: trafficWindow.totalSizeKbps,
            uploadSizeKbps: trafficWindow.uploadSizeKbps,
            downloadSizeKbps: trafficWindow.downloadSizeKbps
          }];
        }
      });

      setTrafficHistory(prev => [...prev, trafficWindow]);
    };

    connection.on('ReceiveTraffic', handleTraffic);

    async function start() {
      try {
        await connection.start();
        console.log('SignalR connected.');
      } catch (err) {
        console.error('SignalR connection error:', err);
        setTimeout(start, 5000);
      }
    }

    start();

    return () => {
      connection.off('ReceiveTraffic', handleTraffic);
      connection.stop().catch(console.error);
      connectionRef.current = null;
    };
  }, []);

  // Usado para debugar. Remover/comentar.
  useEffect(() => {
    console.table(trafficData);
  }, [trafficData]);

  return (

    <>
      <Aside/>
      <DashBoard trafficData={trafficData} trafficHistory={trafficHistory} />
      <Control trafficData={trafficData}/>
    </>

  )

}

export default App;