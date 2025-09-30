import './Control.css';
import { useState } from 'react';
import { devices } from '../../ControlData';

export default function Control({ trafficData }) {
  const [selectedRow, setSelectedRow] = useState(null);
  const [selectedDevice, setSelectedDevice] = useState(null);

  const toggleRow = (index) => setSelectedRow(selectedRow === index ? null : index);
  const toggleDevicePopup = (device) => setSelectedDevice(selectedDevice?.id === device.id ? null : device);

  // Agrupa todos os dados por IP
  const groupedByIP = Object.values(
    trafficData.reduce((acc, curr) => {
      if (!acc[curr.deviceIp]) {
        acc[curr.deviceIp] = { deviceIp: curr.deviceIp, protocols: {} };
      }
      acc[curr.deviceIp].protocols[curr.protocol] = {
        upload: curr.uploadSizeKbps,
        download: curr.downloadSizeKbps
      };
      return acc;
    }, {})
  );

  const drillProtocols = ['FTP', 'FTP-DATA', 'HTTP'];

  return (
    <section className='dash-control'>
      <div className="control-table-container">
        <header className='control-table-header'>
          <span>IP's</span>
          <span>UPLOAD</span>
          <span>DOWNLOAD</span>
          <span>TOTAL</span>
        </header>

        <div className="control-table-content">
          {groupedByIP.map((item, index) => {
            const totalUpload = Object.values(item.protocols).reduce((sum, p) => sum + p.upload, 0);
            const totalDownload = Object.values(item.protocols).reduce((sum, p) => sum + p.download, 0);

            return (
              <div key={index}>
                <div className="device-row" onClick={() => toggleRow(index)}>
                  <span>{item.deviceIp}</span>
                  <span>{totalUpload.toFixed(2)} kbps</span>
                  <span>{totalDownload.toFixed(2)} kbps</span>
                  <span>{(totalUpload + totalDownload).toFixed(2)} kbps</span>
                </div>

                {selectedRow === index && (
                  <div className="device-row-details">
                    {drillProtocols.map((prot, pIndex) => {
                      const data = item.protocols[prot] || { upload: 0, download: 0 };
                      return (
                        <div key={pIndex} className="protocol-row">
                          <span><strong>{prot}</strong></span>
                          <span>{data.upload.toFixed(2)} kbps</span>
                          <span>{data.download.toFixed(2)} kbps</span>
                          <span>{(data.upload + data.download).toFixed(2)} kbps</span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="control-device-buttons">
          {devices.map(device => (
            <button
              key={device.id}
              className={`device-card ${device.status}`}
              onClick={() => toggleDevicePopup(device)}
            >
              <img src={device.icon} alt={`Ícone ${device.name}`} className="device-icon" />
              <div className={`status-indicator ${device.status}`}></div>
            </button>
          ))}
        </div>
      </div>

      {selectedDevice && (
        <div className="device-popup">
          <h3>Dispositivo {selectedDevice.name}</h3>
          <p><strong>IP:</strong> {selectedDevice.ip}</p>
          <p>
            <strong>Largura de banda:</strong> Upload {selectedDevice.bandwidth.upload} / Download {selectedDevice.bandwidth.download}
          </p>
          <button onClick={() => setSelectedDevice(null)}>Fechar</button>
        </div>
      )}
    </section>
  );
}
