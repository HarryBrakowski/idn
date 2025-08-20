import './styles.css';
import { useEffect } from 'react';
import Form from 'react-bootstrap/Form';

function SelectForm({schema, selectedValues, setSelectedValues, size}) {
    // controlId will automatically set the id of the Form.Select element and connect it to the Form.Label
    // schema must be aligned with the schema defined in the grid component

    // set the initial selectedValues when mounting the component
    useEffect(() => {
        setSelectedValues( () => {
            let newValues = {};
            schema.forEach(col => newValues[col.field] = "" );
            return newValues;
        });
    }, [])

    // handle select dropdown changes
    const handleChange = (event, columnDef) => {
        const newVal = event.target.value;
        setSelectedValues(prevSelectedValues => ({...prevSelectedValues, [columnDef.field]:newVal}));
    };



    return (
        <Form className="select-form">
            {schema.map((col, index) => {
                return (
                    <Form.Group className="select-form-group" key={index} controlId={col.field}>
                        <Form.Label sm="6" md="6" lg="4" className="select-form-label" size={size || "sm"}>
                            {col.label}
                        </Form.Label>
                        <Form.Select size={size || "sm"} value={selectedValues[col.field] || ""} onChange={(event) => handleChange(event, col)} >
                            <option value="">Please Select...</option>
                            {col.options && col.options.map(
                                (opt, index) => <option key={index} value={opt.field}>{opt.label}</option>
                            )}
                        </Form.Select>
                    </Form.Group>
                )
            })}
        </Form>
    )
};

export default SelectForm;
