import { useState } from 'react'
import spotify from './assets/spotify.png'
import { useLocation } from 'react-router-dom';

const Home = () => {
    
    const [playlist, setPlaylist] = useState("")

    var language = new URLSearchParams(useLocation().search).get("language") === "pt" ? "pt" : "en";
    var languageParameter = language === "pt" ? "&language=pt" : "";
    
    const searchSong = () => {
        const baseUrl = 'http://localhost:3000'
        const redirectTo = `${baseUrl}/playlist?playlist=${playlist}${languageParameter}`
        window.location.href = redirectTo;
    }

    const texts = {
        title: {
            en: ["Another playlist", "Another you"],
            pt: ["Outra playlist", "Outro você"]
        },
        subtitle: {
            en: [
                "Create a playlist based on your current music taste.",
                "Show us a playlist that you like and we'll create one new for you."
            ],
            pt: [
                "Crie uma playlist com base no seu gosto musical atual.",
                "Mostre-nos uma playlist que você gosta e criaremos uma nova para você."
            ]
        },
        inputs: {
            en: [
                "Your current playlist",
                "Create"
            ],
            pt: [
                "Sua playlist base",
                "Gerar"
            ]
        }
    };

    return ( 
        <div className="home-wrapper">
            <div className="home-div">
                <img src={spotify} alt="" />
                <div className="title-div">
                    <h1 className="home-title">{texts.title[language][0]}</h1>
                    <h1 className="home-title">{texts.title[language][1]}</h1>
                </div>
                <div className="subtitle-div">
                    <span className="home-subtitle">{texts.subtitle[language][0]}</span>
                    <span className="home-subtitle">{texts.subtitle[language][1]}</span>
                </div>
                <div className="input-div">
                    <input className='input-line' placeholder={texts.inputs[language][0]} type="text" value={playlist} onChange={(e) => setPlaylist(e.target.value)}/>
                    <div className='underline' />
                    <div className='generate-button' onClick={() => searchSong()}>{texts.inputs[language][1]}</div>
                    <div className="generate-button-background" />
                </div>
            </div>
            <span className='footer'>{ language === "pt" ? "Criado por" : "Created by"} <a href="https://github.com/hugofolloni">@hugofolloni</a></span>
        </div>
     );
}
 
export default Home;