import { useState } from 'react'
import { useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

import { getRoot } from "./api"
import { searchSongs } from "./api"

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);

  // Handle search song function
  const handleSearch = async () => {
    try {
      if (!searchQuery) return;
      const data = await searchSongs(searchQuery);
      setSearchResults(data);
    } catch (error) {
      console.error("Search failed:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Music Search</h1>

      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search for a song, album, or artist..."
      />

      <button onClick={handleSearch}>Search</button>

      <div style={{ marginTop: "20px" }}>
        {searchResults.map((track, index) => (
          <div key={index} style={{ marginBottom: "10px" }}>
            <strong>{track.name}</strong> - {track.artist}
            <div>{track.album}</div>
            {track.image && (
              <img src={track.image} width={100} alt="album cover"/>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App
