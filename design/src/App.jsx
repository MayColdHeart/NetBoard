import './GlobalStyles.css'
import axios from 'axios';
import { API_URL } from './consts/urls';
import { useEffect } from 'react';

/*Importando componentes*/
import Aside from './components/Aside/Aside'
import DashBoard from './components/DashBoard/DashBoard'
import Control from './components/Control/Control'

function App() {
  useEffect(() => {
    async function fetchTraffic() {
      const options = { method: 'GET', url: `${API_URL}/network/traffic` };
      try {
        console.log("Start request...")
        const { data } = await axios.request(options);
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchTraffic();
  }, []);

  return (

    <>
      <Aside/>
      <DashBoard/>
      <Control/>
    </>

  )

}

export default App;