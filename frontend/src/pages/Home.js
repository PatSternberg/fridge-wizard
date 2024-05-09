// file: frontend/src/pages/Home.js
import Welcome from '../components/welcome';
import LogIn from '../components/logIn';
import SignUp from '../components/signUp';
import { useState } from 'react';
import FridgeImage from '../assets/FridgeImg1.png';
import '../styles.css';

// Home page conditionally renders welcome, login or signup elements
export default function Home() {

  // Set state for the home page to handle which elements will render
  const [ homePage, setHomePage ] = useState('welcome')

  // Handle sign up button click
  const handleSignUpClick = () => {
    setHomePage('signUp');
  };

    // Handle log in button click
  const handleLogInClick = () => {
    setHomePage('logIn');
  };

  // Handle log in button click
  const handleBackClick = () => {
    setHomePage('welcome');
  };

  let componentToRender = 'welcome';

  if (homePage === 'signUp') {
    componentToRender = 
      <SignUp 
        onBackClick={handleBackClick}
      />;
  } else if (homePage === 'logIn') {
    componentToRender = 
      <LogIn 
        onBackClick={handleBackClick}
      />;
  } else {
    componentToRender = 
      <Welcome 
        onLogInClick={handleLogInClick}
        onSignUpClick={handleSignUpClick}
      />
  }
  
  return (
    <div>
      <div style={{ width: '100vw', height: '8vh', backgroundColor: 'var(--primary-color)', borderBottomColor: 'black', borderBottomWidth: '2px', borderBottomStyle: 'solid' }}></div>
      <div className='home-container'>
        <div className='image-container'>
          <img className='fridge-image' src={FridgeImage} alt="Fridge" />
        </div>
        <div className='home-element-container'>
          {componentToRender}
        </div>
      </div>
      <div style={{ width: '100vw', height: '8vh', backgroundColor: 'var(--primary-color)', borderTopColor: 'black', borderTopWidth: '2px', borderTopStyle: 'solid' }}></div>
    </div>
  )
}