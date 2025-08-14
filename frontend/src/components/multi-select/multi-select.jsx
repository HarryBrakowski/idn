import './styles.css';
import Select from 'react-select'; // additional package for multiselect dropdowns

// options to be provided in the form [{field:'', label: '', ..}, {..}, ..]
function MultiSelect({id, options, className, selectedValues, setSelectedValues}) {
    // harmonize options --> react-select requires value, label
    options = options.map(opt => ({...opt, ['value']:opt.field}));

    // handle select dropdown changes -- onChange just passes the selected values by default to the function (feature of react-select)
    const handleChange = (selectedValues) => {
        setSelectedValues(prevSelectedValues => ({...prevSelectedValues, [id]:selectedValues}));
    };

    return <Select
        id={id}
        className={`multi-select ${className}`}
        menuPortalTarget={null}
        isMulti={true}
        options={options}
        onChange={handleChange}
    />
};

export default MultiSelect;