import './styles.css';
import { useEffect, useState, useRef } from 'react';
import Button from 'react-bootstrap/Button';
import DataGrid from '../../components/grid/grid';
import plusIcon from '../../assets/img/plus-icon.png';
import minusIcon from '../../assets/img/minus-icon.png';
import { handleClickAddRow, handleClickRemoveRows } from './callbacks';
import { createEmptyRow } from '../../components/grid/column_defs';



// wraps the input grid component plus additional UI elements like adding new rows and columns
function RegisterDataPage({ schema, rowData, setRowData, onSubmit, height='70%', width='80%' }) {

    // get a reference to the grid
    const gridRef = useRef();

    // emptyRow state to hold the template for a new row
    const [emptyRow, setEmptyRow] = useState({});
    
    // update emptyRowData to add one initial empty row to rowData in case rowData is empty
    useEffect(() => {
        const eR = createEmptyRow(schema);
        setEmptyRow(eR);

        // If rowData is empty, initialize it with the empty row -- use eR due to async nature of setState
        rowData.length == 0 && setRowData([{...eR}]);

    }, [rowData, schema]);



    return (
        <div className='register-materials-page-wrapper'>

            <div className='options-wrapper'>
                <Button variant="outline-secondary" className='d-flex gap-2' onClick={() => handleClickAddRow(setRowData, emptyRow)}>
                    <img draggable={false} alt="plusIcon" src={plusIcon} height="25" width="25" />
                    <div>Add New Row</div>
                </Button>
                <Button variant="outline-secondary" className='d-flex gap-2' onClick={() => handleClickRemoveRows(setRowData, emptyRow, gridRef)}>
                    <img draggable={false} alt="minusIcon" src={minusIcon} height="25" width="25" />
                    <div>Remove Selected Rows</div>
                </Button>
            </div>

            <div style={{ height: height, width: width }}>
                <DataGrid schema={schema} rowData={rowData} setRowData={setRowData} gridRef={gridRef} />
            </div>

            <div className='options-wrapper'>
                <Button variant="outline-success" className='mt-2' size='lg' onClick={() => onSubmit(schema, rowData, setRowData, emptyRow)}>Submit</Button>
            </div>
            
        </div>
    );
};
export default RegisterDataPage;
