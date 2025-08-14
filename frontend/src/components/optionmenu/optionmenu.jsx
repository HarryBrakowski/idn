import './styles.css';
import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import optionmenuIcon from '../../assets/option-icon.png';

// The forwardRef is important!!
// Dropdown needs access to the DOM node in order to position the Menu
const customToggle = React.forwardRef(({ children, onClick }, ref) => (
    <a
      href=""
      ref={ref}
      onClick={(e) => {
        e.preventDefault();
        onClick(e);
      }}
    >
      {children}
    </a>
  ));

function OptionMenu({children}) {
    return (
        <div className='optionmenu'>
            <Dropdown>
                <Dropdown.Toggle as={customToggle} style={{'height': '100%'}}>
                    <span>Additional Options</span>
                    <img 
                        className="optionmenu-button"
                        draggable={false}
                        alt="plus"
                        src={optionmenuIcon}
                        height="30"
                        width="30"
                    />
                </Dropdown.Toggle>

                {/* render the Dropdown.Items here inside a Dropdown.Menu (dynamically passed via children) */}
                {children}

            </Dropdown>

        </div>
    );
}

export default OptionMenu;