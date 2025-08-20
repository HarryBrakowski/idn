import { backendUrl } from './shared';


const defaultHeaders = {
    'Content-Type': 'application/json'
};


export const getRequest = async (url, successFunction, ...successArgs) => {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: defaultHeaders
        });

        if (!response.ok) {
            throw new Error(`GET ${url} failed: ${response.status}`);
        }

        const data = await response.json();
        successFunction?.(data, ...successArgs);
        return data;

    } catch (error) {
        console.error(`Error during GET request to '${url}':`, error);
        throw error;
    }
};

export const postRequest = async (url, payload, successFunction, ...successArgs) => {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: defaultHeaders,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`POST ${url} failed: ${response.status}`);
        }

        const data = await response.json();
        successFunction?.(data, ...successArgs);
        return data;

    } catch (error) {
        console.error(`Error during POST request to '${url}':`, error);
        throw error;
    }
};






// get the materials schema for aggrid creation
export const getMaterialsSchema = (setSchema) => {
    const url = `${backendUrl}/api/v1/materials/schema`;
    const successFunction = (data) => setSchema(data);

    getRequest(url, successFunction);
};
// get the parameters schema for aggrid creation
export const getParametersSchema = (setSchema) => {
    const url = `${backendUrl}/api/v1/parameters/schema`;
    const successFunction = (data) => setSchema(data);

    getRequest(url, successFunction);
};

// get parameters table to populate "parameter dropdowns etc."
export const getParametersTable = (setData) => {
    const url = `${backendUrl}/api/v1/parameters/table`;
    const successFunction = (data) => setData(data);

    getRequest(url, successFunction);
};



// registration of meta data and materials
export const handleSubmitParameterOptions = (schema, rowData, setRowData, emptyRow) => {
    const url = `${backendUrl}/api/v1/parameters/submit-options`;
    const payload = {schema: schema, rowData: rowData};
    const successFunction = () => setRowData([{...emptyRow}]);

    postRequest(url, payload, successFunction);
};
export const handleSubmitMaterialOptions = (schema, rowData, setRowData, emptyRow) => {
    const url = `${backendUrl}/api/v1/materials/submit-options`;
    const payload = {schema: schema, rowData: rowData};
    const successFunction = () => setRowData([{...emptyRow}]);

    postRequest(url, payload, successFunction);
};
export const handleSubmitNewParameters = (schema, rowData, setRowData, emptyRow) => {
    const url = `${backendUrl}/api/v2/parameters/register`;
    const payload = {schema: schema, rowData: rowData}
    const successFunction = () => setRowData([{...emptyRow}]);

    postRequest(url, payload, successFunction);
};
export const handleSubmitNewMaterials = (schema, rowData, setRowData, emptyRow) => {
    const url = `${backendUrl}/api/v2/materials/register`;
    const payload = {schema: schema, rowData: rowData};
    const successFunction = () => setRowData([{...emptyRow}]);

    postRequest(url, payload, successFunction);
};




// handle input data fetching and submitting
export const handleClickGetInputData = (selectedMaterials, selectedParameters, setRowData) => {
    // find all matching materials and corresponding data based on selected values for materials & parameters, 
    // in the form: {'project': 'project_a', 'department': 'department_a',...}
    const url = `${backendUrl}/api/v1/input-data/get`;
    const payload = {selectedMaterials, selectedParameters};
    const successFunction = (data) => {setRowData(data)};

    postRequest(url, payload, successFunction);
};

// submit manually entered data
export const handleClickSubmitInputData = (databaseRowData, rowData, selectedParameters) => {
    const parameters = selectedParameters['parameters'].map(par => par.id)
    const url = `${backendUrl}/api/v1/input-data/submit`;
    const payload = {databaseRowData, rowData, parameters};
    const successFunction = (data) => {console.log(data)};

    postRequest(url, payload, successFunction);
};


