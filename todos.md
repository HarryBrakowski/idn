- Setup RDF/knowledge graph on top of the sql data model
- Eliminate Date -- move to parameter


Important Features
    - in "Define new Materials"
        - Save "Processes" as Template
        - Load Materials from Template
    - in "Add Data"
        - Connect Scrolling behavior in both add data tables
        - reupdate rowData after submitting data to the database (to harmonize rowData with the new database status)
        - Dynamic Dropdown Population based on previous selection
        - Load Template
        - Assign 'Specification'
    -in "Dashboard":
        - Introduce some date picker / date interval picker

- robust error handling
    - duplicate handling when trying to register identical materials
    - duplicate handling when creating identical parameters

- pop ups as success and error feedbacks
    - trigger csv download upon material registration
    - when successfully submitted data
    - when data submission error -- e.g. parameter selected but not re-updated before pushing new data -- implement some smart automation

