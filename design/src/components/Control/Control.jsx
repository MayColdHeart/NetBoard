import './Control.css';
import { useState } from 'react';
import { devices, ProtocolData} from '../../ControlData';

export default function Control() {
  const [selectedRow, setSelectedRow] = useState(null);
  const [selectedDevice, setSelectedDevice] = useState(null);

  const toggleRow = (index) => {
    setSelectedRow(selectedRow === index ? null : index);
  }

  const toggleDevicePopup = (device) => {
    setSelectedDevice(selectedDevice?.id === device.id ? null : device);
  }

  return (

    <section className='dash-control'>

      <div className="control-table-container">

        <header className='control-table-header'>
          <h3>IP's</h3>
          <h3>UPLOAD</h3>
          <h3>DOWNLOAD</h3>
          <h3>TOTAL</h3>

        </header>

        <div className="control-table-content">

          {ProtocolData.map((prot, index) => (
            
            <div key={index}>

              <div
                className="device-row"
                onClick={() => toggleRow(index)}
                style={{ cursor: 'pointer' }}
              >
                <p>{prot.IP}</p>
                <p>{prot.UPLOAD}</p>
                <p>{prot.DOWNLOAD}</p>
                <p>{prot.Total}</p>
              </div>

            {selectedRow === index && (

            <div className="device-row-details">

                <div>
                    <strong>FTP</strong>
                    <p>{prot.ftpUpload} <span className='kbps'>kbps</span></p>
                    <p>{prot.ftpDownload} <span className='kbps'>kbps</span></p>
                    <p>{prot.ftpUpload + prot.ftpDownload} <span className='kbps'>kbps</span></p>
                    </div>
                    <div>
                    <strong>HTTP</strong>
                    <p>{prot.httpUpload} <span className='kbps'>kbps</span></p>
                    <p>{prot.httpDownload} <span className='kbps'>kbps</span></p>
                    <p>{prot.httpUpload + prot.httpDownload} <span className='kbps'>kbps</span></p>
                </div>

            </div>

            )}
            
            </div>
          ))}

        </div>

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