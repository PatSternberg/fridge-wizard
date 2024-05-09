// file: frontend/src/App.js

import './App.css';
import {Routes, Route} from 'react-router-dom';
import Home from './pages/Home';
import Fridge from './pages/Fridge';
import Recipes from './pages/Recipes';
import Profile from './pages/profile';

function App() {
  return (
    <div className="App">
      <div>
        <Routes>
          <Route path='' element={<Home />} />
          <Route path='/fridge' element={<Fridge />} />
          <Route path='/recipes' element={<Recipes />} />
          <Route path='/profile' element={<Profile />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
