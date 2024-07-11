import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from "./Home";
import Header from "./Header"
import Playlist from './Playlist';

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/playlist" element={<Playlist />} />
      </Routes>
    </Router>
  );
}

export default App;
