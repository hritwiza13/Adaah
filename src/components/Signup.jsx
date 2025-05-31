import React, { useState } from 'react';
import './signup.css'; 
import { globalContext } from './globalContext';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
  const nav = useNavigate()
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confPassword, setConfPassword] = useState('');
  const [birthday, setBirthday] = useState('');

  const { setAuth } = React.useContext(globalContext)
 
  function isValidPassword(password) {
    // At least 8 characters, one uppercase, one lowercase, one number, one special character
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(password);
  }

  function handleSubmit(e){
    e.preventDefault();
    if(email && password && confPassword && name && birthday){
      if(!isValidPassword(password)) {
        alert("Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.");
        return;
      }
      if(password === confPassword){
        // Store all user details in localStorage
        window.localStorage.setItem("email", email);
        window.localStorage.setItem("password", password);
        window.localStorage.setItem("user_name", name);
        window.localStorage.setItem("user_birthday", birthday);
        window.localStorage.setItem("user_email", email);
        window.localStorage.setItem("user_password", password);
        
        setAuth(true);
        nav('/upload-photo');
      }
      else alert("Passwords don't match!")
    }
    else alert("Please fill in all details!")
  }
  return (
    <div className="signup-wrapper">
      <form onSubmit={handleSubmit} className="signup-form">
        <h1 className="signup-title">Adaah</h1>

        <label htmlFor='email'>Enter Email:</label>
        <input
          id='email'
          type='email'
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <label htmlFor='name'>Enter Name:</label>
        <input
          id='name'
          type='text'
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <label htmlFor='birthday'>Birthday:</label>
        <input
          id='birthday'
          type='date'
          value={birthday}
          onChange={(e) => setBirthday(e.target.value)}
        />

        <label htmlFor='pass'>Enter Password:</label>
        <input
          id='pass'
          type='password'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <label htmlFor='confirm'>Confirm Password:</label>
        <input
          id='confirm'
          type='password'
          value={confPassword}
          onChange={(e) => setConfPassword(e.target.value)}
        />

        <button type='submit'>Sign Up</button>
      </form>
    </div>
  );
};

export default Signup; 