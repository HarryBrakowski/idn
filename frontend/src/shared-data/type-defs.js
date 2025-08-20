// delete as soon its coming from backend
export const defaultTypes = [
    {field: 'select', label: 'Select Type'},
    {field: 'number', label: 'Number Type'},
    {field: 'text', label: 'Text Type'},
    {field: 'largeText', label: 'Long Text Type'},
    {field: 'date', label: 'Date Type'},
]

// InputGrid type definitions
export const typeText = (field, label, maxLength) => {
    return ({
        field: field,
        headerName: label,
        valueGetter: (params) => params.data[field] || '', // important to force empty cells to store ""
        valueSetter: (params) => {
            params.data[field] = params.newValue;
            return true;
        },
        cellEditor: 'agTextCellEditor',
        cellEditorParams: {
            maxLength: maxLength || 30,
        },
    })
};
export const typeLargeText = (field, label, maxLength) => {
    return ({
        field: field,
        headerName: label,
        valueGetter: (params) => params.data[field] || '', // important to force empty cells to store ""
        valueSetter: (params) => {
            params.data[field] = params.newValue;
            return true;
        },
        cellEditor: 'agLargeTextCellEditor',
        cellEditorPopup: true,
        cellEditorParams: {
            maxLength: maxLength || 100,
        },
    })
};
export const typeNumber = (field, label, maxDecimalPlaces) => {
    return ({
        field: field,
        headerName: label,
        valueGetter: (params) => params.data[field] || null, // important to force empty cells to store null
        valueSetter: (params) => {
            params.data[field] = params.newValue;
            return true;
        },
        cellEditor: 'agNumberCellEditor',
        cellEditorParams: {
            precision: maxDecimalPlaces || 12,
            preventStepping: true
        }
    })
};
export const typeSelect = (field, label, options) => {
    const opts = Array.isArray(options) ? options : [{field:'', label:''}];
    const fields = opts.map(option => option.field || '');

    return {
        field: field,
        headerName: label,
        cellEditor: 'agSelectCellEditor',
        cellEditorParams: {
            values: fields,
        },
        // make sure to render the label - while working with the field value in all other cases
        valueFormatter: (params) => {
            const match = opts.find(opt => opt.field === params.value);
            return match ? match.label : params.value;
        },
        valueParser: (params) => {
            return params.newValue;
        },
        // ensure this field is always a valid option
        onCellValueChanged: (params) => {
            // if the value is not in the options, reset it to the first option
            if (!params.data[field] || !fields.includes(params.data[field])) {
                params.data[field] = fields[0] || '';
                params.api.refreshCells({ force: true });
            }
        }
    }
};
export const typeDate = (field, label, includeTime) => {
    return ({
        field: field,
        headerName: label,
        cellEditor: 'agDateStringCellEditor',
        cellEditorParams: {
            includeTime: includeTime || false,
        },
        // ensure this field is always a valid date
        onCellValueChanged: (params) => {
            // if the value is not in the options, reset it to the first option
            if (!params.data[field]) {
                params.data[field] = new Date().toISOString().split('T')[0];
                params.api.refreshCells({ rowNodes: [params.node], force: true });
            }
        }
    })
};
