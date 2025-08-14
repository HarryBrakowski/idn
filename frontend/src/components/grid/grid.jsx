import { useEffect, useState } from 'react';
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community'; 
ModuleRegistry.registerModules([ AllCommunityModule ]);
import { AgGridReact } from 'ag-grid-react';
import { createColumnDefs } from './column_defs';


function DataGrid({schema, rowData, setRowData, gridRef, editable=true, dragRows=true}) {
    // Build Column Definitions
    const [colDefs, setColDefs] = useState([]);
    useEffect(() => {
        createColumnDefs(schema, setColDefs);
    }, [schema]);


    // handleDragEnd
    const handleDragEnd = (event) => {
        let newData = [];

        // iterate through the nodes in the "virtual grid order" to push each nodes's data into newData
        event.api.forEachNodeAfterFilterAndSort((node) => {
            newData.push(node.data);
        });

        // set the new row data
        setRowData(newData);
    };

    const defaultColumnDefs = {
        editable: editable,
        cellClass: params => {
            return params.value === null || params.value === undefined || params.value === ''? 'empty-cell' : '';
        }
    }

    return (
        <div style={{ height: '100%', width: '100%' }}>
            <AgGridReact
                ref={gridRef}
                // column settings
                defaultColDef={defaultColumnDefs}
                autoSizeStrategy={{type: 'fitGridWidth'}}

                // row settings
                rowHeight={30}

                // cell settings
                singleClickEdit={true}

                // data
                columnDefs={colDefs}
                rowData={rowData}
                onCellValueChanged={() => console.log(rowData)}

                // row dragging
                {...(dragRows && {
                        rowSelection:{mode: "multiRow", copySelectedRows: true},
                        rowDragEntireRow:true,
                        rowDragManaged:true,
                        rowDragMultiRow:true,
                        animateRows:true,
                        onRowDragEnd:handleDragEnd
                    })
                }
                
            />
        </div>
    );
};

export default DataGrid;
