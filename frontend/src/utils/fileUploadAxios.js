import axios from "axios";

const fileUploadAxios = axios.create({
  baseURL: "http://localhost:5000",
});

export default fileUploadAxios;
