import './styles.css'
import RegisterDataPage from '../register-data/register-data'
import { handleSubmitParameterOptions, handleSubmitMaterialOptions } from '../../api-calls/api-calls';



function RegisterSelectOptionsPage({
    materialOptionsSchema,
    materialOptionsRowData,
    setMaterialOptionsRowData,
    parameterOptionsSchema,
    parameterOptionsRowData,
    setParameterOptionsRowData
}) {

    return (
        <div className="select-options-page-wrapper">

            <div className="grid-wrapper">
                <div className="grid-header" >Material Specific Select Options</div>
                <RegisterDataPage
                    schema={materialOptionsSchema}
                    rowData={materialOptionsRowData}
                    setRowData={setMaterialOptionsRowData}
                    onSubmit={handleSubmitMaterialOptions}
                    height='50%'
                    width='95%'
                />
            </div>

            <div className="grid-wrapper">
                <div className="grid-header" >Parameter Specific Select Options</div>
                <RegisterDataPage
                    schema={parameterOptionsSchema}
                    rowData={parameterOptionsRowData}
                    setRowData={setParameterOptionsRowData}
                    onSubmit={handleSubmitParameterOptions}
                    height='50%'
                    width='95%'
                />
            </div>

        </div>
    )
}

export default RegisterSelectOptionsPage;
