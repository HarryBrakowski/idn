import './styles.css';
import { typeText, typeLargeText, typeNumber, typeSelect, typeDate } from '../../shared-data/type-defs';


// column definition function
export const createColumnDefs = (schema, setColDefs) => {
    // Clear previous definitions
    setColDefs(prev => []);

    // Build new definitions based on schema
    schema.forEach(col => {
        switch (col.type) {
            case 'text':
                setColDefs(prev => [...prev, typeText(col.field, col.label, col.maxLength)]);
                break;
            case 'largeText':
                setColDefs(prev => [...prev, typeLargeText(col.field, col.label, col.maxLength)]);
                break;
            case 'number':
                setColDefs(prev => [...prev, typeNumber(col.field, col.label, col.maxDecimalPlaces)]);
                break;
            case 'select':
                setColDefs(prev => [...prev, typeSelect(col.field, col.label, col.options)]);
                break;
            case 'date':
                setColDefs(prev => [...prev, typeDate(col.field, col.label, col.includeTime)]);
                break;
            default:
                console.warn(`Unknown column type: ${col.type}`);
        }
    })
};




// default row data definition
export const createEmptyRow = (schema) => {
    // Reset emptyRow to an empty object
    let rowData = {};

    // Populate emptyRow based on schema
    schema.forEach(col => {
        switch (col.type) {
            case 'text':
            case 'largeText':
                rowData[col.field] = '';
                break;
            case 'number':
                rowData[col.field] = null;
                break;
            case 'select':
                // take care: select type must receive an object with field and label
                rowData[col.field] = col.options && col.options.length > 0 ? col.options[0]['field'] : ''; // Default to first option if available;
                break;
            case 'date':
                rowData[col.field] = new Date().toISOString().split('T')[0]; // Default to today's date
                break;
            default:
                console.warn(`Unknown column type: ${col.type}`);
        }
    })
    return rowData;
};
