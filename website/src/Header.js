import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import About from './About';

const Header = () => {

    const location = useLocation()

    var language = new URLSearchParams(location.search).get("language")
    var text = language === "pt" ? "Sobre" : "About";

    const redirect = () => {
        if(location.pathname !== '/'){
            window.location.href = `/?language=${language}`
        }
    }

    const [showAbout, setShowAbout] = useState(false)

    return ( 
        <div className="header-wrapper">
            <h2 style={{cursor: `${location.pathname !== '/' ? "pointer" : "default"}`}} onClick={() => redirect()}>multiverse</h2>
            <div onClick={() => setShowAbout(true)} className="about-button">{text}</div>
            {showAbout && (
                <div className='about-wrapper'>
                    <div className='positioning'>
                        <div className="translucent" onClick={() => setShowAbout(false)}/>
                        <About language={language} />
                    </div>
                </div>
            )}
        </div>
     );
}
 
export default Header;