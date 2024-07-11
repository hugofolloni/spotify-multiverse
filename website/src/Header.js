import { useLocation } from 'react-router-dom';

const Header = () => {

    var text = new URLSearchParams(useLocation().search).get("language") === "pt" ? "Sobre" : "About";


    return ( 
        <div className="header-wrapper">
            <h2>multiverse</h2>
            <div className="about-button">{text}</div>
        </div>
     );
}
 
export default Header;