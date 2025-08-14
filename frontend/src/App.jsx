import { useEffect, useState } from 'react';
import { defaultMaterialSchema, defaultParameterSchema } from './shared-data/default-options';
import MyNavbar from './components/navbar/navbar';
import Home from './pages/home/home';
import RegisterDataPage from './pages/register-data/register-data';
import AddDataPage from './pages/add_data/add_data';
import Dashboard from './pages/dashboard/dashboard';
import MaterialOptions from './pages/material-options/material-options';
import { handleClickRegisterMaterials, handleClickRegisterParameters } from './api-calls/api-calls';



function App() {
    // schema and row data state
    const [page, setPage] = useState('home');
    const [rowData, setRowData] = useState([]); // core rowData for Materials and Data
    const [parameterRowData, setParameterRowData] = useState([])



    return (
        <>
            <MyNavbar 
                setPage={setPage}
            />

            {page === 'home' && <Home />}
            {page === 'newMaterials' && <RegisterDataPage
                schema={defaultMaterialSchema}
                rowData={rowData}
                setRowData={setRowData}
                onSubmit={handleClickRegisterMaterials}
            />}
            {page === 'addData' && <AddDataPage schema={defaultMaterialSchema} />} {/* TODO: Add Caching -- default row data based on recently registered materials */}

            {page === 'dashboard' && <Dashboard />}

            {page === 'newParameters' && <RegisterDataPage
                schema={defaultParameterSchema}
                rowData={parameterRowData}
                setRowData={setParameterRowData}
                onSubmit={handleClickRegisterParameters}
            />}
            {page === 'materialOptions' && <MaterialOptions />}
        </>
    )
}

export default App;
