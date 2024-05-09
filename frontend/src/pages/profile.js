import React, { useState, useEffect } from 'react';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import { useNavigate } from 'react-router-dom';
import FridgeImage from '../assets/FridgeImg1.png';
import '../styles.css';

const UserProfile = () => {
  const [userData, setUserData] = useState(null);
  const [userId, setUserId] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = JSON.parse(atob(token.split('.')[1]));
      setUserId(decodedToken.user_id);

      fetch(`${process.env.REACT_APP_BACKEND_URI}users/get-user/?user_id=${decodedToken.user_id}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.user_data) {
          setUserData(data.user_data);
          setUsername(data.user_data.username);
          setEmail(data.user_data.email);
        } else {
          console.error('User data not found');
        }
      })
      .catch(error => {
        console.error('Error fetching user data:', error);
      });
    } else {
      console.error('Token not found');
    }
  }, []);

  const navigateToRoot = () => {
    navigate('/');
  };

  const handleSave = () => {
    const token = localStorage.getItem('token');
    const requestBody = { user_id: userId, username, email, password };

    fetch(`${process.env.REACT_APP_BACKEND_URI}user_profile/update_profile/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Handle success or error response
      if (data.message) {
        setMessage('Updated successfully.');
        setUserData(prevUserData => ({
          ...prevUserData,
          username,
          email,
          password
        }));
      } else {
        setMessage('Failed to update data.');
      }
    })
    .catch(error => {
      console.error('Error updating profile:', error);
      setMessage('Failed to update data.');
    });
  };

  return (
    <div className="profile-container">
      <div className='back-button'>
        <button onClick={navigateToRoot}>
          <ArrowBackIosNewIcon /><h1>FH</h1>
        </button>
      </div>
      {userData ? (
        <div className="profile-content">
        <div className='image-container'>
          <img className='fridge-image' src={FridgeImage} alt="Fridge" />
        </div>
          <div className="user-details">
            <h2>{username ? `${username}'s Profile` : 'User Profile'}</h2>
            <div>
              <input type="text" placeholder="username" value={username} onChange={e => setUsername(e.target.value)} />
            </div>
            <div>
              <input type="email" placeholder="email" value={email} onChange={e => setEmail(e.target.value)} />
            </div>
            <div>
              <input type="password" placeholder="password" value={password} onChange={e => setPassword(e.target.value)} />
            </div>
            <div>
              <button onClick={handleSave}>Save</button>
            </div>
          </div>
          {message && <p className={message.includes('success') ? 'success-message' : 'error-message'}>{message}</p>}
        </div>
      ) : (
        <p>Loading user profile...</p>
      )}
    </div>
  );
};

export default UserProfile;
