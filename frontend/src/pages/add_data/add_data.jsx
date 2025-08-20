import './styles.css';
import { useEffect, useState, useRef } from 'react';
import MultiSelect from '../../components/multi-select/multi-select';
import Button from 'react-bootstrap/Button';
import SelectForm from '../../components/select/select';
import DataGrid from '../../components/grid/grid';
import searchIcon from '../../assets/img/search-icon.png';
import uploadIcon from '../../assets/img/upload-icon.png';
import {handleClickGetInputData, handleClickSubmitInputData} from '../../api-calls/api-calls';



// wraps the register-data component plus additional UI elements like adding new rows and columns
function AddDataPage({schema, parameterOptions}) {
    // initialize rowData
    const [databaseRowData, setDatabaseRowData] = useState([]); // set via api call "handleClickGetInputData" only
    const [rowData, setRowData] = useState([]); // set by databaseRowData and changed by grid editing
    useEffect(() => setRowData(databaseRowData.map((node) => ({...node}))), [databaseRowData]);

    // initialize the selected data object -- initial values are set within the SelectForm component
    const [selectedMaterialValues, setSelectedMaterialValues] = useState({});
    const [selectedParameters, setSelectedParameters] = useState({'parameters':[]});

    // get a reference to the grid
    const materialGridRef = useRef();
    const parameterGridRef = useRef();


    return (
        <div className='add-data-page-wrapper'>

            <div className='selection-wrapper'>

                <div className="material-selection-wrapper" style={{width: '50%', marginRight:'10px'}}>
                    <div style={{fontWeight:'bold', fontSize:"20px"}} >Select your Materials</div>

                    <SelectForm 
                        schema={schema.filter(c => c.type=='select')} 
                        selectedValues={selectedMaterialValues} 
                        setSelectedValues={setSelectedMaterialValues}
                    />
                </div>

                <div className="parameter-selection-wrapper" style={{width:'50%', marginLeft:'10px'}} >
                    <div style={{fontWeight:'bold', fontSize:"20px"}} >Select your Parameters</div>
                    <MultiSelect
                        id='parameters'
                        options={parameterOptions} 
                        className='w-75' 
                        selectedValues={selectedParameters['parameters']} 
                        setSelectedValues={setSelectedParameters}
                    />
                </div>

            </div>

            <div className="d-flex flex-column align-items-center w-100">
                <Button 
                    variant="secondary" 
                    className='d-flex gap-2 m-2' 
                    style={{width: '170px'}} 
                    onClick={() => handleClickGetInputData(selectedMaterialValues, selectedParameters, setDatabaseRowData)}
                >
                    <img draggable={false} alt="searchIcon" src={searchIcon} height="25" width="25" />
                    <div>Get your Data</div>
                </Button>
            </div>

            <div className='data-grid-wrapper'>
                <div style={{ height: 'calc(100% - 0px)', width: '50%', marginRight:'10px'}}>
                    <DataGrid 
                        schema={schema} 
                        rowData={rowData} 
                        setRowData={setRowData} 
                        gridRef={materialGridRef} 
                        editable={false} 
                        dragRows={false}
                    />
                </div>
                <div style={{ height: 'calc(100% - 0px)', width: '50%', marginLeft:'10px' }}>
                    <DataGrid 
                        schema={selectedParameters['parameters']}
                        rowData={rowData} 
                        setRowData={setRowData} 
                        gridRef={parameterGridRef} 
                        editable={true} 
                        dragRows={false}
                    />
                </div>

            </div>

            <div className='w-100 d-flex flex-column align-items-end pe-5'>
                <Button variant="secondary" className='d-flex gap-2 m-2' style={{width: '220px'}} onClick={() => handleClickSubmitInputData(databaseRowData, rowData, selectedParameters)}>
                    <img draggable={false} alt="uploadIcon" src={uploadIcon} height="25" width="25" />
                    <div>Submit Entered Data</div>
                </Button>
            </div>

        </div>
    );
};

export default AddDataPage;
