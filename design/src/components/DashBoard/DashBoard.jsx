import './DashBoard.css'

import PieChart from "./grafic/PieChart";
import MultiLineChart from './grafic/MultLines';

export default function DashBoard(){

return(

    <main className='dash-board'>

        <header className='dash-header'>

            <div className="summary">



            </div>

        </header>
        <section className='dash-data'>

            <ul>

                <li className="min-block">

                    <h2>
                        Gráfico de Pizza
                    </h2>
                    <PieChart/>

                </li>
                <li className="medium-block">
                    <h2>
                        Gráfico de tempo
                    </h2>
                    <MultiLineChart/>

                </li>

            </ul>

        </section>

    </main>

)

}