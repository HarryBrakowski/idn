import './styles.css';

function Home() {
    return (
        <div className='home-page-container'>
            <h3>Welcome!</h3>
            <br/>
            <div className="w-50 d-flex flex-column align-items-center" style={{fontSize:'15px'}}>
                <b>Introduction</b>
                <p>
                    This app is a prototype demonstrating how simple and flexible manual data capturing can be in 
                    product- or material-centric environments.
                </p>
                
                <b>Why?</b>
                <p>
                    Even today, many individuals, teams, and organizations rely on unstructured formats to capture data, 
                    such as local spreadsheets, text documents (PDFs, Word files, electronic notebooks), or, worst of all, memory.
                </p>
                <p>
                    Making data accessible without slowing down the capture process is key. People cannot spend hours on data entry 
                    instead of focusing on value-generating tasks. This prototype shows an efficient approach to define materials 
                    and parameters in a familiar, spreadsheet-like interface.
                </p>
                
                <b>How?</b>
                <p>
                    The core of this prototype is a flexible meta-data management system. 
                    You can dynamically define parameter- and material-specific select options, which serve as the foundation for:
                    <br/>a) defining new parameters of interest, and  
                    <br/>b) registering new materials.  
                </p>
                <p>
                    Once parameters and materials are set up, corresponding values can be entered directly in a spreadsheet-like UI. 
                    All data is saved with timestamps, ensuring full traceability and historical tracking. 
                    This makes the app highly adaptable across different projects, departments, or procedures—without requiring any code changes.
                </p>
                <p>
                    In short: the app demonstrates how dynamic meta-data and option management can make manual data entry 
                    both efficient and adaptable, while keeping the system extensible for future use.
                </p>

            </div>
            <br/>
            <div className="w-50 d-flex flex-column align-items-center" style={{fontSize:'15px'}}>
                <b>Quick Guide</b>
                <ol>
                    <li>Define the specific parameters you want to capture, including select options if needed.</li>
                    <li>Register your materials, with their own dynamic select options if applicable.</li>
                    <li>
                        Add your data on the "Data Input / Add Data" page:
                        <ol>
                            <li>Filter materials of interest.</li>
                            <li>Select parameters you want to capture data for.</li>
                            <li>Click <i>Get your Data</i> to retrieve matching materials and existing values.</li>
                            <li>Enter your data in the editable table, then press <i>Submit</i>.</li>
                            <li>
                                All data is saved in the backend with a timestamp. Nothing is overwritten, 
                                so historical values and changes remain traceable.
                            </li>
                        </ol>
                    </li>
                </ol>
            </div>
        </div>
    );
};

export default Home;

