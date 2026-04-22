import { useState } from 'react'
import { useEffect } from 'react'
import './App.css'

import { getRoot } from "./api"
import { searchSongs } from "./api"

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // Handle automatic search when search query changes, with debounce
  useEffect(() => {
    // Don't search if search query is empty
    if (!searchQuery) {
      setSearchResults([]);
      return;
    }

    // Set debounce timer (500ms)
    const timeout = setTimeout(async () => {
      try {
        setLoading(true);
        const data = await searchSongs(searchQuery);
        setSearchResults(data);
      } catch (error) {
        console.error("Search failed:", error);
      } finally {
        setLoading(false);
      }
    }, 500); // 500ms debounce

    // Cleanup: cancel previous timer if user keeps trying
    return () => clearTimeout(timeout);

  }, [searchQuery]);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Search for music</h1>

      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search for a song, album, or artist..."
      />

      {loading && <p>Searching...</p>}

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
