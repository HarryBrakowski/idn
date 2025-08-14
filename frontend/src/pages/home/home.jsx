import './styles.css';

function Home() {
    return (
        <div className='home-page-container'>
            <h3>Welcome!</h3>
            <br/>
            <div className="w-50 d-flex flex-column align-items-center" style={{fontSize:'15px'}}>
                <b>Introduction</b>
                <p>
                    This app is a prototype demonstrating how simple manual data capturing can be in product- or material-centric environments.
                </p>
                
                <b>Why?</b>
                <p>
                    Even today, many individuals, teams, and organizations rely on unstructured formats to capture data, 
                    such as local spreadsheets, text documents (PDFs, Word files, electronic notebooks), or, worst of all, memory.
                </p>
                <p>
                    Making data accessible without slowing down the capture process is key. People cannot spend hours on data entry 
                    instead of focusing on value-generating tasks. This prototype shows a very efficient approach to define materials 
                    and assign data in a familiar, spreadsheet-like interface.
                </p>
                <b>How?</b>
                <p>
                    This prototype is built around a flexible meta-data management approach. You first define the parameters 
                    you want to capture, which are stored in a structured backend. Materials can then be registered and combined with these parameters, 
                    and corresponding values entered in a simple, spreadsheet-like interface.
                </p>
                <p>
                    The structure of materials and their associated parameters is dynamic: you can add or modify fields, define dropdown selections, 
                    or change data types at any time. This flexibility allows you to adapt the system to different projects, departments, or procedures 
                    without changing the core application. All captured data is consistently stored and timestamped, making it traceable and auditable.
                </p>
                <p>
                    In short, the app demonstrates how a well-designed meta-data framework can make manual data entry both efficient and adaptable, 
                    while keeping the system extensible for future use.
                </p>
            </div>
            <br/>
            <div className="w-50 d-flex flex-column align-items-center" style={{fontSize:'15px'}}>
                <b>Quick Guide</b>
                <ol>
                    <li>Define the specific parameters you want to capture (Meta Data Management / Define Your Parameters).</li>
                    <li>Define the materials you manufacture, develop, or create (Data Input / Register New Material(s)).</li>
                    <li>
                        Add your data on the "Data Input / Add Data" page:
                        <ol>
                            <li>Query your materials of interest using the filter criteria (top-left block).</li>
                            <li>Select the parameters you want to add data for.</li>
                            <li>Click 'Get your Data' to retrieve matching materials and existing data.</li>
                            <li>Enter your data in the table rendered next to each material and parameter, then press 'Submit'.</li>
                            <li>
                                All data is saved in the backend with a timestamp. Nothing is overwritten, so historical values 
                                and changes can be traced back to the respective time points.
                            </li>
                        </ol>
                    </li>
                </ol>
            </div>
        </div>
    );
};
export default Home;