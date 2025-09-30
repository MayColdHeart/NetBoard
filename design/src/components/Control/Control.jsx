import './Control.css'

import { useState } from 'react';

/* Dados */
import { devices, protocolData } from '../../ControlData';

export default function Control(){

    const [selectedDevice, setSelectedDevice] = useState(null);

    const openDevicePopup = (device) => {
        setSelectedDevice(device);
        setOpen(false);
    }

    const closeDevicePopup = () => {
        setSelectedDevice(null);
    }

    const [expanded, setExpanded] = useState(false);

return(

    <section className='dash-control'>

        <div className="control-tabel-container">

            <div 
            className={`control-tabel ${expanded ? "expanded" : ""}`} 
            onClick={() => setExpanded(prev => !prev)}
            >

                <div className="tabel-itens">
                    <h3>
                        HTTP+UTP
                    </h3>
                    <div className="tabel-itens-data">
                        {protocolData.http_utp.ips.map(ip => (
                        <span key={ip}>{ip}</span>
                        ))}                        
                    </div>
                </div>
                <div className="tabel-itens">
                    <h3>
                        HTTP
                    </h3>
                    <div className="tabel-itens-data">
                        {protocolData.http.ips.map(ip => (
                        <span key={ip}>{ip}</span>
                        ))}
                    </div>
                </div>
                <div className="tabel-itens">
                    <h3>
                        UTP
                    </h3>
                    <div className="tabel-itens-data">
                        {protocolData.utp.ips.map(ip => (
                        <span key={ip}>{ip}</span>
                        ))}
                    </div>
                </div>

            </div>

        </div>

        <div className={`control-device ${selectedDevice ? "with-popup" : ""}`}>
            {devices.map(device => (
                <button 
                    key={device.id} 
                    className={`device-card ${device.status}`}
                    onClick={() => openDevicePopup(device)}
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
                <p><strong>Largura de banda:</strong> Upload {selectedDevice.bandwidth.upload} / Download {selectedDevice.bandwidth.download}</p>
                <button onClick={closeDevicePopup}>Fechar</button>
            </div>
        )}

    </section>

)

}