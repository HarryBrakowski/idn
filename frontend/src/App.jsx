import { useEffect, useState } from 'react';
import MyNavbar from './components/navbar/navbar';
import Home from './pages/home/home';
import RegisterDataPage from './pages/register-data/register-data';
import AddDataPage from './pages/add_data/add_data';
import Dashboard from './pages/dashboard/dashboard';
import RegisterSelectOptionsPage from './pages/register-select-options/register-select-options';
import { 
    getMaterialsSchema, 
    getParametersSchema, 
    getParametersTable,
    handleSubmitNewMaterials, 
    handleSubmitNewParameters,
} from './api-calls/api-calls';



function App() {
    // schema and row data state
    const [page, setPage] = useState('home');
    const [rowData, setRowData] = useState([]); // core rowData for Materials and Data
    const [parameterRowData, setParameterRowData] = useState([]);
    const [materialOptionsRowData, setMaterialOptionsRowData] = useState([]);
    const [parameterOptionsRowData, setParameterOptionsRowData] = useState([]);
    const [parameterOptions, setParameterOptions] = useState([]) // just the up-to-date "parameters" table

    // initialize AgGrid schema and option data -- AgGrid Schema derived from ORM -- see useEffects below
    const [materialsSchema, setMaterialsSchema] = useState([]);
    const [materialOptionsSchema, setMaterialOptionsSchema] = useState([]);
    const [parametersSchema, setParametersSchema] = useState([]);
    const [parameterOptionsSchema, setParameterOptionsSchema] = useState([]);

    // define the schema based on backend ORM info processing (see respective api routes & useEffects below) -- update on-mount and on-options-submit
    useEffect(() => getMaterialsSchema(setMaterialsSchema), [materialOptionsRowData] ) 
    useEffect(() => getParametersSchema(setParametersSchema), [parameterOptionsRowData] )

    // get available parameters from the parameters table
    useEffect(() => getParametersTable(setParameterOptions), [parameterRowData]) // update whenever parameters are added in page 'newParameters'

    // material options schema -- populate select-types from materialsSchema
    useEffect(() => {
        const opts = materialsSchema.filter(column => column.type == 'select');
        const schema = [
            {type:'select', field: 'material_feature', 'label': 'Material Feature', options:opts},
            {type: 'text', field: 'option', 'label': 'New Option', maxLength: 25},
        ];
        setMaterialOptionsSchema(schema);
    }, [materialsSchema])

    // parameter options schema -- populate select-types from parametersSchema
    useEffect(() => {
        const opts = parametersSchema.filter(column => column.type == 'select' && column.field != 'type');
        const schema = [
            {type:'select', field: 'parameter_feature', 'label': 'Parameter Feature', options:opts},
            {type: 'text', field: 'option', 'label': 'New Option', maxLength: 25},
        ];
        setParameterOptionsSchema(schema);
    }, [parametersSchema])



    return (
        <>
            <MyNavbar setPage={setPage} />

            {page === 'home' && <Home />}

            {page === 'newOptions' && <RegisterSelectOptionsPage
                materialOptionsSchema={materialOptionsSchema}
                materialOptionsRowData={materialOptionsRowData}
                setMaterialOptionsRowData={setMaterialOptionsRowData}
                
                parameterOptionsSchema={parameterOptionsSchema}
                parameterOptionsRowData={parameterOptionsRowData}
                setParameterOptionsRowData={setParameterOptionsRowData}
            />}

            {page === 'newParameters' && <RegisterDataPage
                schema={parametersSchema}
                rowData={parameterRowData}
                setRowData={setParameterRowData}
                onSubmit={handleSubmitNewParameters}
            />}


            {page === 'newMaterials' && <RegisterDataPage
                schema={materialsSchema}
                rowData={rowData}
                setRowData={setRowData}
                onSubmit={handleSubmitNewMaterials}
            />}

            {page === 'addData' && <AddDataPage
                schema={materialsSchema}
                parameterOptions={parameterOptions}
            />} {/* TODO: Add Caching -- default row data based on recently registered materials */}

            {page === 'dashboard' && <Dashboard />}
        </>
    )
}

export default App;
