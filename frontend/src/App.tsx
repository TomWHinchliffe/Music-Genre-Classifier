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
      <div className="min-h-screen bg- text-white p-6">
        <h1 className="text-2x1 font-bold mb-4">Search for music</h1>

        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search for a song, album, or artist..."
          className="w-full p-3 rounded-lg bg-gray-800 text-white outline-none focus:ring-1"
        />

        {loading && <p className="mt-3 text-gray-400">Searching...</p>}

        {/* Display search results */}
        <div className="mt-6 space-y-2">
          {searchResults.map((track, index) => (
            <div
              key={index}
              className="flex items-center justify-between bg-gray-900 hover:bg-gray-800 p-3 rounded-lg transition"
            >
              {/* Left: Album cover and track info */}
              <div className="flex items-center gap-4">
                {track.image && (
                  <img
                    src={track.image}
                    alt="album cover"
                    className="w-14 h-14 object-cover rounded"
                  />
                )}

                <div>
                  <div className="text-white font-semibold">
                    {track.name}
                  </div>
                  <div className="text-gray-400 text-sm">
                    {track.artist}
                  </div>
                </div>
              </div>

              {/* Right: Artist name and release year */}
              <div className="text-gray-400 text-sm">
                {track.album} - {track.release_year}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App
