// file: frontend/src/components/signUp.js
import React, { useState } from 'react';
import AxiosInstance from './axios';
import SimpleTextField from './forms/simpleTextField';
import SimplePasswordField from './forms/simplePasswordField';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { signup } from '../services/user_services';

// Welcome page elements to be conditionally rendered on landing page
export default function SignUp({ onBackClick }) {

  // Set navigate function to be used by buttons following user input
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");

  // Set default values for submitted information
  const defaultValues = {
    email:'',
    username:'',
    password:'',
  }

  // Declare a useForm variable to handle submitting information
  const {handleSubmit, control, formState: { errors }} = useForm({defaultValues:defaultValues})  


  async function submission(data) {
    try {
      console.log('Begin submission')
      // Validate email format
      if (!data.email.match(/^[\w\.-]+@[\w\.-]+$/)) {
        setErrorMessage('Invalid email format');
        return;
      }
      console.log('Email validation pass')

      // Validate password length and special characters
      if (data.password.length < 8 || !/[!@#$%^&*()-_+={}[\]|\\:]/.test(data.password)) {
        setErrorMessage('Password must be at least 8 characters long and contain at least one special character');
        return;
      }
      console.log('Password validation pass')
      
      // Call the signup function
      const res = await signup(data.username, data.email, data.password);
      console.log('Called signup function')
      let user_id = res.user_id;
      console.log(`Assigned user_id as ${user_id}`)
      
      const today = new Date();
      function addDays(date, days) {
        var result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
      }
      
      const fridgeData = {// Set data to be sent with request when creating new fridge
        storedItems: {
          '🎁 Welcome pack':{
             'Hot sauce': addDays(today, -7),
             'White miso paste': addDays(today, 7)
          },
          '🥬 Vegetables':{ },
          '🍉 Fruit':{ },
          '🍖 Meat':{ },
          '🧀 Dairy':{ },
          '🥫 Misc':{ }
        },

        user_id : user_id

      };

      // Send post request with fridgeData body to create endpoint
      // And then on success navigate to fridge page passing on
      // User id details to get fridge on next page
      AxiosInstance.post('fridges/create/', fridgeData) // Send post request with fridgeData body to create endpoint

      AxiosInstance.post('users/login/', data)
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
      console.error('Error signing up:, error.message');
      // Handle error here, set error message, etc.
      setErrorMessage('Error signing up');
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
          <h2>Become a Fridge Hero</h2>
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

          <SimpleTextField
            label='Username'
            name='username'
            control={control}
            width={'30%'}
            >
            {errors.username && <p className="error-message">{errors.username.message}</p>}
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
            Sign up
          </button>
        </form>
        <div className="error-container">
          {errorMessage && <p className="error-message">{errorMessage}</p>}
        </div>
      </div>
    </div>
  );
}