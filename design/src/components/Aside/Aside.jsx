import './Aside.css'

import { useState } from 'react';

/*Importando icons */
import Code from '../../assets/icons/code.png'
import SunIcon from '../../assets/icons/sun.png'
import MoonIcon from '../../assets/icons/moon.png'
import DashIcon from '../../assets/icons/dashboard.png'

export default function Aside() {

  const [isDarkMode, setIsDarkMode] = useState(false);
  const [open, setOpen] = useState(false);

  const changeTheme = () => {
    setIsDarkMode(prev => !prev);
    document.body.classList.toggle('dark-mode', !isDarkMode);
  }

  const togglePanel = () => {
    setOpen(prev => !prev);
  }

return (

    <aside className='dash-aside'>

      <h1>NetBoard</h1>
      <div className="sidebar">

        <button className="side-item" onClick={togglePanel}>

          <img src={DashIcon} alt="Imagem de DashBoard" />
          <span>Filtrar Rede</span>

        </button>

        <a href="https://github.com/MayColdHeart/NetBoard" target='_blank' className="side-item">

          <img src={Code} alt="Código" />
          <span>Código</span>   

        </a>

        <button className="side-item" onClick={changeTheme}>

          <img src={isDarkMode ? MoonIcon : SunIcon} alt="Imagem de troca de tema" />
          <span>Alterar tema</span>

        </button>

        {open && (
            <section className='bg-control-panel'>

                <div className="control-panel">

                    <h2>Filtros</h2>
                    <form onSubmit={(e) => e.preventDefault()}>

                    <label>IP <input type="text" placeholder='Digite aqui o IP' /></label>
                    <label>Protocolo <input type="text" placeholder='Digite aqui o protocolo HTTP ou FTP' /></label>

                    <button type="submit">APLICAR</button>
                    <button type="button" onClick={() => setOpen(false)}>Fechar</button>

                    </form>

                </div>

            </section>

        )}

      </div>

    </aside>

)

}