// ControlData.js
import ComputerIcon from './assets/icons/computer.png';

export const devices = [ 
    {
      id: 1,
      name: "1",
      icon: ComputerIcon,
      ip: "192.168.0.1",
      bandwidth: { upload: "12 Mbps", download: "50 Mbps" },
    },
    {
      id: 2,
      name: "2",
      icon: ComputerIcon,
      ip: "192.168.0.2",
      bandwidth: { upload: "8 Mbps", download: "40 Mbps" },
    },
    {
      id: 3,
      name: "3",
      icon: ComputerIcon,
      ip: "192.168.0.3",
      bandwidth: { upload: "0 Mbps", download: "0 Mbps" },
    },
    {
      id: 4,
      name: "4",
      icon: ComputerIcon,
      ip: "192.168.0.4",
      bandwidth: { upload: "15 Mbps", download: "60 Mbps" },
    }
]

export const protocolData = {
  http_utp: {
    total: 5,
    ips: ['192.168.0.30', '192.168.0.40', '192.168.0.55', '192.168.0.60', '192.168.0.70']
  },
  http: {
    total: 3,
    ips: ['192.168.0.10', '192.168.0.15', '192.168.0.25']
  },
  utp: {
    total: 2,
    ips: ['192.168.0.20', '192.168.0.50']
  }
}