import ComputerIcon from './assets/icons/computer.png';

/* Dispositivos */
export const devices = [ 
  {
    id: 1,
    name: "1",
    icon: ComputerIcon,
    ip: "192.168.0.1",
    bandwidth: { upload: "12 Mbps", download: "50 Mbps" },
    status: "online"
  },
  {
    id: 2,
    name: "2",
    icon: ComputerIcon,
    ip: "192.168.0.2",
    bandwidth: { upload: "8 Mbps", download: "40 Mbps" },
    status: "online"
  },
  {
    id: 3,
    name: "3",
    icon: ComputerIcon,
    ip: "192.168.0.3",
    bandwidth: { upload: "0 Mbps", download: "0 Mbps" },
    status: "offline"
  },
  {
    id: 4,
    name: "4",
    icon: ComputerIcon,
    ip: "192.168.0.4",
    bandwidth: { upload: "15 Mbps", download: "60 Mbps" },
    status: "online"
  }
];

/* Protocolos */
export const ProtocolData = [
  {
    IP: "192.168.0.1",
    UPLOAD: 100,
    DOWNLOAD: 200,
    get Total() { return this.UPLOAD + this.DOWNLOAD; },
    get httpUpload() { return this.UPLOAD / 2; },
    get httpDownload() { return this.DOWNLOAD / 2; },
    get ftpUpload() { return this.UPLOAD / 2; },
    get ftpDownload() { return this.DOWNLOAD / 2; }
  },
  {
    IP: "192.168.0.2",
    UPLOAD: 150,
    DOWNLOAD: 300,
    get Total() { return this.UPLOAD + this.DOWNLOAD; },
    get httpUpload() { return this.UPLOAD / 2; },
    get httpDownload() { return this.DOWNLOAD / 2; },
    get ftpUpload() { return this.UPLOAD / 2; },
    get ftpDownload() { return this.DOWNLOAD / 2; }
  },
  {
    IP: "192.168.0.3",
    UPLOAD: 80,
    DOWNLOAD: 120,
    get Total() { return this.UPLOAD + this.DOWNLOAD; },
    get httpUpload() { return this.UPLOAD / 2; },
    get httpDownload() { return this.DOWNLOAD / 2; },
    get ftpUpload() { return this.UPLOAD / 2; },
    get ftpDownload() { return this.DOWNLOAD / 2; }
  },
  {
    IP: "192.168.0.4",
    UPLOAD: 200,
    DOWNLOAD: 400,
    get Total() { return this.UPLOAD + this.DOWNLOAD; },
    get httpUpload() { return this.UPLOAD / 2; },
    get httpDownload() { return this.DOWNLOAD / 2; },
    get ftpUpload() { return this.UPLOAD / 2; },
    get ftpDownload() { return this.DOWNLOAD / 2; }
  }
];