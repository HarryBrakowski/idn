materials = {
    # schema and types dynamically created based on frontend
    'project',
    'department',
    'procedure',
    'procedure_spec',
    'unitProcedure',
    'operation',
    'date',
    'description',
    'id'
}

parameters = [
    # schema and types dynamically created based on frontend
    'type',
    'group',
    'name',
    'unit',
    'id'
]

gui_data_spec = [
    # statically created
    {'type': 'text', 'field': 'material_id'}, 
    {'type': 'text', 'field': 'parameter_id'}, 
    {'type': 'text', 'field': 'value'},
    {'type': 'auto_timestamp', 'field':'timestamp'}
]
