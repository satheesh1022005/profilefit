import axios from "axios";

const axiosHeader = axios.create({
  baseURL: "https://profilefit.onrender.com/",
  headers: {
    "Content-Type": "application/json"
  }
});


// // Add a request interceptor
// axiosHeader.interceptors.request.use(
//   (config) => {
//     const user = JSON.parse(localStorage.getItem("user"));
//     if (user && user.token) {
//       config.headers["x-auth-token"] = user.token;
//     }
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

export default axiosHeader;
