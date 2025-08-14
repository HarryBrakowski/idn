// TODO: create dynamically in page 'Define your Material Options -- for 'select' data types only'
export const defaultMaterialSchemaSelectOptions = {
    'project': [
        {field: 'project_a', label: 'Project A'},
        {field: 'project_b', label: 'Project B'},
        {field: 'project_c', label: 'Project C'},
        {field: 'project_d', label: 'Project D'}
    ],
    'department': [
        {field: 'department_a', label: 'Department A' },
        {field: 'department_b', label: 'Department B' },
        {field: 'department_c', label: 'Department C' }
    ],
    'procedure': [
        {field: 'batch_manufacture', label: 'Batch Manufacture' },
        {field: 'lab_experiment', label: 'Lab Experiment' }
    ],
    'unitProcedure': [
        {field: 'unit_a', label: 'Unit A' },
        {field: 'unit_b', label: 'Unit B' },
        {field: 'unit_c', label: 'Unit C' }
    ],
    'operation': [
        {field: 'operation_a', label: 'Operation A' },
        {field: 'operation_b', label: 'Operation B' },
        {field: 'operation_c', label: 'Operation C' }
    ]
};


// parameter specific group options
export const defaultGroupOptions = [
    {field: 'mass_balance', label: 'Mass Balance Specific Parameter'},
    {field: 'process_parameter', label: 'Process Parameter'},
    {field: 'equipment', label: 'Equipment Parameter'},
    {field: 'quality_control', label: 'Quality Control Parameter'},
];
export const defaultTypeOptions = [
    {field: 'select', label: 'Select Type'},
    {field: 'number', label: 'Number Type'},
    {field: 'text', label: 'Text Type'},
    {field: 'largeText', label: 'Long Text Type'},
    {field: 'date', label: 'Date Type'},
]
export const defaultUnitOptions = [
    {field: '', label: ''},
    {field: 'percent', label: '%'},
    {field: 'kilogram', label: 'kg'},
    {field: 'gram', label: 'g'},
    {field: 'liter', label: 'L'},
    {field: 'gramm_per_l', label: 'g/L'},
    {field: 'milligram', label: 'mg'},
    {field: 'milliliter', label: 'mL'},
    {field: 'ton', label: 't'},
    {field: 'parts_per_million', label: 'ppm'},
    {field: 'international_units', label: 'IU'},
    {field: 'international_units_per_ml', label: 'IU/mL'},
]

// default material schema definition
// must be aligned with the type definitions in type-defs.js
export const defaultMaterialSchema = [
    {type: 'select', field: 'project', label: 'Project', options: defaultMaterialSchemaSelectOptions['project']},
    {type: 'select', field: 'department', label: 'Department', options: defaultMaterialSchemaSelectOptions['department']},
    {type: 'select', field: 'procedure', label: 'Procedure', options: defaultMaterialSchemaSelectOptions['procedure']},
    {type: 'text', field: 'procedure_spec', label: 'Batch/Experiment Specifier', maxLength: 20},
    {type: 'select', field: 'unitProcedure', label: 'Unit Procedure', options: defaultMaterialSchemaSelectOptions['unitProcedure']},
    {type: 'select', field: 'operation', label: 'Operation', options: defaultMaterialSchemaSelectOptions['operation']},
    {type: 'date', field: 'date', label: 'Date of Execution'},
    {type: 'largeText', field: 'description', label: 'Description (optional)', maxLength: 100},
];

export const defaultParameterSchema = [
    {type: 'select', field: 'type', label: 'Parameter Type', options: defaultTypeOptions.filter(opt => opt.field != 'select')},
    {type: 'select', field: 'group', label: 'Parameter Group', options: defaultGroupOptions},
    {type: 'text', field: 'name', label: 'Parameter Name', maxLength: 20},
    {type: 'select', field: 'unit', label: 'Parameter Unit', options: defaultUnitOptions},
]




