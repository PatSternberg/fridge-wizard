//file: fridge-hero/frontend/src/services/user_services.js
export const signup = async (username, email, password) => {
  console.log('Access user_services.signup()')
  const requestData = {
    username: username,
    email: email,
    password: password
  };
  console.log(`Access user_services.signup():Request Data complete, current data=${username}`)



  const BACKEND_URL = `${process.env.REACT_APP_BACKEND_URI}users/signup/`;
  console.log(`Backend URL is ${BACKEND_URL}`);

  
  const requestOptions = {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  };
  console.log(`Request options are`, JSON.stringify(requestOptions));

  const response = await fetch(BACKEND_URL, requestOptions);
  console.log(`Fetch request pass`);

  if (!response.ok) {
    const data = await response.json(); // Parse response JSON
    throw new Error(data.message); // Throw an Error object with the message from the response
  }

  const data = await response.json();
  console.log(`Response is: ${response}`);
  return data;
};