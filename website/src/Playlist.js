import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import headphone from "./assets/headphone.png"

const Playlist = () => {

    const [fetched, setFetched] = useState(false);
    const [data, setData] = useState();
    const [error, setError] = useState(false);
    const [tracks, setTracks] = useState([]);
    const [end, setEnd] = useState(20)

    var searchParameters = new URLSearchParams(useLocation().search)
    var language = searchParameters.get("language") === "pt" ? 'pt' : "en";
    var playlist = searchParameters.get("playlist")

    const replaceSong = (index) => {
        if(end < 50) {
            var currentSongs = tracks;
            currentSongs[index] = data.tracks[end]
            setEnd(end + 1)
        }
   }

    useEffect( () => {
        console.log(playlist)
        fetch(`http://127.0.0.1:5000/analysis?key=aHVnb3N0b3Nv&amount=50&playlist=${playlist}`)
        // fetch(`http://127.0.0.1:5000/fake?key=aHVnb3N0b3Nv&offset=10&limit=15&amount=50&`)
        .then(res => res.json())
        .then(data => {
            setData(data)
            console.log(data.code)

            if(data.code !== 0){
                setError(true)
            }

            if(data.tracks){
                setTracks(data.tracks.slice(0, 20))
            }
            setFetched(true);
        })
        .then(() => {
            console.log(data)
            console.log(error)
        })
    }, [])

    const texts = {
        error: {
            en: ["Error", "Return to home"],
            pt: ["Erro", "Retornar ao início"]
        },
        loading: {
            en: {
                "disclaimer": "This might take up to about a minute...",
                "texts": ["Turning on the multiverse machine", "Putting on special suit", "Adjusting travel parameters", "Accessing interdimensional portal", "Attempting radio contact"]
            },
            pt: {
                "disclaimer": "Isso pode demorar até cerca de um minuto...",
                "texts":["Ligando a máquina multiversal", "Vestindo traje especial", "Ajustando parâmetros da viagem", "Acessando portal interdimensional", "Tentando contato via rádio"]
            }
        }
    }

    return (
        <div className='playlist-wrapper'>
        {
           (fetched && (
               <div style={{width: '100%', height: '100%'}}>
                {(error && (
                            <div className="error-wrapper">
                                <div className='error-div'>
                                    <h1>{texts.error[language][0]}</h1> 
                                    <h3 className='error-description'>{data.error}</h3>
                                    <div onClick={() => window.location.href = "/"} className='return-button'>{texts.error[language][1]}</div>
                                </div>
                            </div>
                        )
                    )  || (
                        <div className='playlist-div'>
                            <div className="playlist-infos">
                                <div className="cover-wrapper">
                                    <img src={data.infos.cover} alt="Cover" className='cover-image' />
                                </div>
                                <span className='playlist-title'>{data.infos.name}</span>
                            </div>
                            <div className='tracks-wrapper'>
                                {tracks && tracks.map((track, idx) => (
                                    <div className='track-div' key={track.id}>
                                        <iframe style={{border: 'none'}} title={track.track_id} src={`https://open.spotify.com/embed/track/${track.track_id}?utm_source=generator&theme=0`} width="80%" height="100%" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy" />
                                        <RestartAltIcon fontSize="large" color={end < 50 ? "success" : "disabled"} className='update' onClick={() => replaceSong(idx)} /> 
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
           )) 
           ||
           <div style={{width: '100%', height: '60vh'}}>
                <Loading args={texts.loading[language]}/>
            </div> 
        }
        </div>
    );
}

const Loading = (props) => {

    const texts = props.args.texts
    const disclaimer = props.args.disclaimer

    console.log(props.texts)

    return (
        <div className='loading-wrapper'>
            <div className="loading-headphone-div">
                <img className='loading-headphone-img' src={headphone} alt="" />
            </div>
            <div className="texts-wrapper">
                <div className='texts-div'>
                    {texts.map(text => (
                        <div className="single-text">{text}</div>
                    ))}
                    {texts.map(text => (
                        <div className="single-text">{text}</div>
                    ))}
                </div>
            </div>
            <span>{disclaimer}</span>
        </div>
    )
}
 
export default Playlist;