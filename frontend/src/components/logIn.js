// file: frontend/src/components/logIn.js
import React, { useState } from 'react';
import AxiosInstance from './axios';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import SimpleTextField from './forms/simpleTextField';
import SimplePasswordField from './forms/simplePasswordField';
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'

// Welcome page elements to be conditionally rendered on landing page
export default function LogIn({ onBackClick }) {
  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  // Set default values for submitted information
  const defaultValues = {
    email:'',
    password:'',
  }

  // Declare a useForm variable to handle submitting information
  const {handleSubmit, control, formState: { errors }} = useForm({defaultValues:defaultValues})

  // Logic for submitting the form goes here
  async function submission(data) {
    try {
      let userInfo = {
        email: data.email,
        password: data.password
      }

      AxiosInstance.post('users/login/', userInfo)
      .then((res) => {
        console.log(res.data.user_id);
        localStorage.setItem("token", res.data.token);
        navigate(
          '/fridge/',
          { state:{
            user_id: res.data.user_id}
          }
      )})
      .catch((error) => {// Handle error if POST request fails
        console.error('Error:', error);
      });
    } catch (error) {
      console.log('Error logging in:', error.message);
    }
  }

  return (
    <div>
      <div className='welcome-container'>
        <div className='welcome-header'>
          <div className='back-button'>
            <button onClick={( onBackClick )}>
                  <ArrowBackIosNewIcon />
            </button>
          </div>
          <h2>Log in to Fridge Hero</h2>
        </div>
      <form onSubmit={handleSubmit(submission)}>
      
        <SimpleTextField
          label='Email'
          name='email'
          control={control}
          width={'30%'}
          >
        {errors.email && <p className="error-message">{errors.email.message}</p>}
        </SimpleTextField>

        <SimplePasswordField
          label='Password'
          name='password'
          control={control}
          width={'30%'}
          >
          {errors.password && <p className="error-message">{errors.password.message}</p>}
        </SimplePasswordField>

        <button className='login-buttons' type='submit'> 
          Log in
        </button>
      </form>
      <div className="error-container">
          {errorMessage && <p className="error-message">{errorMessage}</p>}
        </div>
      </div>
    </div>
  )
}