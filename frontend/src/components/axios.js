// file: axios.js
import axios from 'axios';

const baseURL = process.env.REACT_APP_BACKEND_URI

const AxiosInstance = axios.create({
  baseURL:baseURL,
  timeout:5000,
  headers:{
    'Content-Type':'application/json',
    accept:'application/json',
  }
});

export default AxiosInstance