import { useLocation } from 'react-router-dom';

const Header = () => {

    const location = useLocation()

    var text = new URLSearchParams(location.search).get("language") === "pt" ? "Sobre" : "About";

    const redirect = () => {
        if(location.pathname !== '/'){
            window.location.href = "/"
        }
    }

    return ( 
        <div className="header-wrapper">
            <h2 style={{cursor: `${location.pathname !== '/' ? "pointer" : "default"}`}} onClick={() => redirect()}>multiverse</h2>
            <div className="about-button">{text}</div>
        </div>
     );
}
 
export default Header;