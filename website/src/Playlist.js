import { useLocation } from 'react-router-dom';

const Playlist = () => {
    var searchParameters = new URLSearchParams(useLocation().search)
    var language = searchParameters.get("language") === "pt" ? 'pt' : "en";
    var playlist = searchParameters.get("playlist")

    return (
        <div>
            <h1>Analysis</h1>
            <p>Language: {language}</p>
            <p>Playlist: {playlist}</p>
        </div>
    );
}
 
export default Playlist;