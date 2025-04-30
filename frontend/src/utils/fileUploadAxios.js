import axios from "axios";

const fileUploadAxios = axios.create({
  baseURL: "https://profilefit.onrender.com/",
});

export default fileUploadAxios;
