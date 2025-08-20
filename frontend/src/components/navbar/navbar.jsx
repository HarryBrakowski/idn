import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import logo from '../../assets/img/app-logo.png';

function MyNavbar({setPage}) {
    return (
        <Navbar expand="lg" className="bg-body-tertiary">
            <Container>

                <Navbar.Brand href="/">
                    <img
                        alt=""
                        src={logo}
                        width="34"
                        height="30"
                        className="d-inline-block align-middle"
                    />{' '}
                    IDN
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />

                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto gap-3">
                        <Nav.Link onClick={() => setPage('home')} >Home</Nav.Link>

                        <NavDropdown title="Data Input" id="basic-nav-dropdown">                   
                            <NavDropdown.Item onClick={() => setPage('newMaterials')}>Register New Material(s)</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => setPage('addData')}>Add Data</NavDropdown.Item>
                        </NavDropdown>
                    
                        <NavDropdown title="Get your Data" id="basic-nav-dropdown">
                            <NavDropdown.Item onClick={() => setPage('dashboard')}>Dashboard</NavDropdown.Item>
                        </NavDropdown>

                        <NavDropdown title="Meta Data Definition" id="basic-nav-dropdown">
                            <NavDropdown.Item onClick={() => setPage('newOptions')}>Define your 'Select Options'</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => setPage('newParameters')}>Define your Parameters</NavDropdown.Item>
                        </NavDropdown>

                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default MyNavbar;