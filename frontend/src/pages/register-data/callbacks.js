export const handleClickAddRow = (setRowData, emptyRow) => {
    // Create a new row based on the emptyRow template
    const newRow = { ...emptyRow };
    // Add the new row to the existing rowData
    setRowData(prevRowData => [...prevRowData, newRow]);
};



export const handleClickRemoveRows = (setRowData, emptyRow, gridRef) => {
    // Get the selected rows from the grid
    const selectedRows = gridRef.current.api.getSelectedRows();
    // If no rows are selected, return early
    if (selectedRows.length === 0) {
        console.warn('No rows selected for removal');
        return;
    }

    // Filter out the selected rows from the current rowData and update the state
    setRowData(prevRowData => {
        // default copy of the previous rowData
        let newData = [...prevRowData];

        // handle the case where all rows are selected or else where just a subset is selected
        if (prevRowData.length > 0 && selectedRows.length == prevRowData.length) {
            newData = [{...emptyRow}];
        } else if (prevRowData.length > 0 && selectedRows.length < prevRowData.length) {
            newData = [...prevRowData].filter(row => !selectedRows.includes(row));
        }
        return newData
    });
};



export const handleClickAddColumn = (setSchema, setRowData, columnDef) => {
    console.log('triggered menu option add column')
    // update the schema with the new column definition -- this will trigger a re-render of the grid
    setSchema(prevSchema => [...prevSchema, columnDef]);
    // also update the rowData to include the new column in each row
    switch (columnDef.type) {
        case 'text':
        case 'largeText':
            setRowData(prevRowData => prevRowData.map(row => ({ ...row, [columnDef.field]: ''})));
            break;
        case 'number':
            setRowData(prevRowData => prevRowData.map(row => ({ ...row, [columnDef.field]: null})));
            break;
        case 'select':
            setRowData(prevRowData => prevRowData.map(row => ({ ...row, [columnDef.field]: columnDef.options && columnDef.options.length > 0 ? columnDef.options[0] : ''})));
            break;
        case 'date':
            setRowData(prevRowData => prevRowData.map(row => ({ ...row, [columnDef.field]: new Date().toISOString().split('T')[0]})));
            break;
        default:
            console.warn(`Unknown column type: ${columnDef.type}`);
    }

};
