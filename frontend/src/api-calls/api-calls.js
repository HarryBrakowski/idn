import { backendUrl } from './shared';
import { defaultUnitOptions } from '../shared-data/default-options';

const apiCall = (url, payload, successFunction, ...successArgs) => {
    fetch(url, {
        'method': 'POST',
        headers: {
            'Authorization': '',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            successFunction?.(data, ...successArgs);
        })
        .catch(error => console.error(`Error during api call '${url}'. Error: `, error));
};



export const handleClickRegisterMaterials = (schema, rowData, setRowData, emptyRow) => {
    const url = `${backendUrl}/api/v1/register-materials`;
    const payload = {schema: schema, rowData: rowData}
    const successFunction = () => setRowData([{...emptyRow}]);

    apiCall(url, payload, successFunction);
};


export const handleClickRegisterParameters = (schema, rowData, setRowData, emptyRow) => {
    const url = `${backendUrl}/api/v1/register-parameters`;
    const payload = {schema: schema, rowData: rowData}
    const successFunction = () => setRowData([{...emptyRow}]);

    apiCall(url, payload, successFunction, {});
};


export const getParameters = (tableName, setData) => {
    const url = `${backendUrl}/api/v1/get-table`;
    const payload = { tableName: tableName }
    const successFunction = (data) => setData(() => {
        // modify data to construct field and label from the database columns "name, unit and id"
        data = data.map(node => {
            const unit_label = defaultUnitOptions.filter(opt => opt.field == node.unit)[0].label
            return ({
                ...node, 
                ['field']: node.id, 
                ['label']:`${node.name} [${unit_label}]`,
            })
        });
        return data
    });

    apiCall(url, payload, successFunction);
};


export const handleClickGetMaterialData = (selectedMaterials, selectedParameters, setRowData) => {
    // find all matching materials and corresponding data based on selected values for materials & parameters, 
    // in the form: {'project': 'project_a', 'department': 'department_a',...}
    const url = `${backendUrl}/api/v1/get-materials-and-data`;
    const payload = {selectedMaterials, selectedParameters}

    const successFunction = (data) => {
        let combinedRowData = []

        // iterate through each material
        data['materials'].forEach(node => {
            let newNode = {...node}

            // iterate through every selected material (selected in ag grid)
            selectedParameters['parameters'].forEach(par => {
                // add matching data for this material_id and parameter_id to the respective material rowData
                const match = data['data'].filter(row => row['material_id'] == node.id && row['parameter_id'] == par.id)[0]
                const value = match?.['value']
                // convert parameter type 'number' to Number
                value
                    ? par.type=='number' ?newNode[par.id]=Number(value) :newNode[par.id]=value
                    : newNode[par.id]=""
            })
            combinedRowData.push(newNode);

        })
        setRowData(combinedRowData);
        //setParameterRowData(data['data']);
        console.log('combined Row Data', combinedRowData);
    };

    apiCall(url, payload, successFunction);
};




export const handleClickSubmitData = (rowData, selectedParameters) => {
    // submit manually entered data
    const parameters = selectedParameters['parameters'].map(par => par.id)

    const url = `${backendUrl}/api/v1/save-manual-data`;
    const payload = {rowData, parameters};
    const successFunction = (data) => {console.log(data)};

    apiCall(url, payload, successFunction);
};


