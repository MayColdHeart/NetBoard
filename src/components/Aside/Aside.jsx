import './Aside.css'

import { useState } from 'react';

/*Importando icons */
import UsersIcon from '../../assets/icons/users.png'
import Code from '../../assets/icons/code.png'
import SunIcon from '../../assets/icons/sun.png'
import MoonIcon from '../../assets/icons/moon.png'

export default function Aside(){

const [isDarkMode, setIsDarkMode] = useState(false);

const changeTheme = () => {
    setIsDarkMode(prev => !prev);
    document.body.classList.toggle('dark-mode', !isDarkMode);
}

return(

    <aside className='dash-aside'>

        <h1>
            DashBoard
        </h1>
        <div className="sidebar">
            
            <button className="side-item">

                <img src={UsersIcon} alt="Imagem de usuário" />
                <span>
                    Integrantes
                </span>

            </button>
            <a href="https://github.com/MayColdHeart/NetBoard" target='_blank'
            className="side-item">

                <img src={Code} alt="Código" />
                <span>
                    Código
                </span>    

            </a>
            <button className="side-item" onClick={changeTheme}>

                <img src={isDarkMode ? MoonIcon : SunIcon} alt="Imagem de troca de tema" />
                <span>Alterar tema</span>

            </button>
            
        </div>

    </aside>

)

}