import axios from "axios";

const API = "http://127.0.0.1:8000";

export const getRoot = async () => {
  const res = await axios.get(`${API}/`);
  return res.data;
};