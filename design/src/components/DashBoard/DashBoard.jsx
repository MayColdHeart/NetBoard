import './DashBoard.css'

import PieChart from "./grafic/PieChart";
import MultiLineChart from './grafic/MultLines';

export default function DashBoard({ trafficData, trafficHistory }){

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
                    <PieChart trafficData={trafficData} />

                </li>
                <li className="medium-block">
                    <h2>
                        Gráfico de tempo
                    </h2>
                    <MultiLineChart trafficHistory={trafficHistory} />

                </li>

            </ul>

        </section>

    </main>

)

}