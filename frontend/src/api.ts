import axios from "axios";

const API = "http://127.0.0.1:8000";

export const getRoot = async () => {
  const res = await axios.get(`${API}/`);
  return res.data;
};

export const searchSongs = async (query: string) => {
  const res = await axios.get(`${API}/search`, {
    params: { query },
  });
  return res.data.tracks;
}