import AxiosInstance from '../components/axios';
import { useLocation, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import ItemList from '../components/itemsList';
import FridgeImage from '../assets/FridgeImg2.png';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import { Link } from 'react-router-dom';
import ProfileIcon from '../assets/ProfileImg.png';
import '../styles.css';

export default function Fridge() {
  const location = useLocation();
  const userId = location.state && location.state.user_id;
  const [currentFridgeContents, setCurrentFridgeContent] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [items, setItems] = useState([]);
  const navigate = useNavigate();
  const categories = [
    {label: '🥬 Vegetables', value: '🥬 Vegetables'},
    {label: '🍖 Meat', value: '🍖 Meat'},
    {label: '🍉 Fruit', value: '🍉 Fruit'},
    {label: '🧀 Dairy', value: '🧀 Dairy'},
    {label: '🥫 Miscellaneous', value: '🥫 Misc'}
  ];

  console.log(userId)

  useEffect(() => {
    if (userId) {
      getFridgeData(userId);
    }
  }, [userId]);

  function navigateToRoot() {
    navigate('/');
  };

  // Logic for getting fridge data goes here
  function getFridgeData(data) {
    // Send get request with userData body to get endpoint
    AxiosInstance.get('fridges/get/', {params: {user_id: userId}})
        .then(response => {
          // Handle successful response
          setCurrentFridgeContent(response.data);
        })
        .catch((error) => {
          // Handle error if POST request fails
          console.error('Error:', error);
        });
  }

  function getRecipes() {
    AxiosInstance.get( 'fridges/get-recipes/', { params: { user_id: userId  } })
    .then(response => {
      // Handle successful response
      console.log(response)
    })
    .catch((error) => {
      // Handle error if POST request fails
      console.error('Error:', error);
    });
    navigate('/recipes', { state: { user_id: userId } });
  }

  // function addItemToFridge() {
  //   // Check if all fields are filled
  //   if (!itemName || !itemCategory || !expiryDate) {
  //     alert("Please fill all fields before adding an item.");
  //     return;
  //   }
  // }
  function toggleForm() {
    setShowForm(!showForm);
    if (!showForm && items.length === 0) {
      addItem(); // Add first empty item automatically
    }
  }

  function handleItemChange(index, field, value) {
    const newItems = [...items];
    newItems[index][field] = value;
    setItems(newItems);
  }

  function addItem() {
    const newItem = {name: '', category: '', expiry_date: ''};
    setItems([...items, newItem]);
  }

  function addItemToFridge() {
    for (const item of items) {
      if (!item.name || !item.category || item.category === "" || !item.expiry_date) {
        alert("Please fill all fields for all items before adding.");
        return;
      }
      item.expiry_date = new Date(item.expiry_date).toISOString().slice(0, 11) + "00:00:00Z";
    }

    try {
      const token = localStorage.getItem('token');
      const requestBody = {
        token: token,
        items: items
      };
      console.log(requestBody)

    AxiosInstance.patch(`fridges/${currentFridgeContents.fridge_data._id}/add-items/`, requestBody)
        .then(response => {
          console.log(localStorage.getItem('token'));
          localStorage.setItem('token', response.data.token);
          console.log(localStorage.getItem('token'));
          setItems([]);
          setShowForm(false);
          getFridgeData(userId);
        })
        .catch(error => {
          console.error('Error adding items:', error.response.data.error);
          navigate('/');
        });
      } catch(error) {
        // Handle error if POST request fails
        console.error('Error:', error.message);
      }
  }

  function removeItem(category, itemName) {
    const fridgeId = currentFridgeContents.fridge_data._id;
    AxiosInstance.delete(`fridges/${fridgeId}/remove-items/`, {
      data: { category, name: itemName }
    })
        .then(response => {
          console.log('Item removed:', response.data);
          getFridgeData(userId); // Refresh the list to show updated items
        })
        .catch(error => {
          console.error('Error removing item:', error);
        });
  }
    
  return (
      <div className='fridge-view-container'>
        <div className='open-fridge-image-container'>
          <button onClick={navigateToRoot}>
          <ArrowBackIosNewIcon /><h1>FH</h1>
          </button>
          <div className='open-fridge-image'>
            <img src={FridgeImage} alt="Fridge"/>
          </div>
          <div className='profile-icon-container'>
             <Link to="/profile">
                <img src={ProfileIcon} alt="Profile"/>
              </Link>
            </div>
        </div>
        <div className='item-list'>
          <h1>{showForm ? 'Add Items' : "What's inside?"}</h1>
            {!showForm && (
                <>
                    <ItemList returnedFridgeData={currentFridgeContents} removeItem={removeItem}/>
                    <button onClick={toggleForm} className="fridge-form-button">Add Items</button>
                    <button onClick={getRecipes} className="fridge-form-button">Get Recipes</button>
                </>
            )}
          {showForm && (
              <>
                {items.map((item, index) => (
                    <div key={index} className="item-input-container">
                      <div className="item-input-group">
                        <select value={item.category} onChange={e => handleItemChange(index, 'category', e.target.value)}>
                          <option value="">Choose Category...</option>
                          {categories.map((option) => (
                              <option key={option.value} value={option.value}>
                                {option.label}
                              </option>
                          ))}
                        </select>
                        <input
                            type="text"
                            placeholder="Item Name"
                            value={item.name}
                            onChange={e => handleItemChange(index, 'name', e.target.value)}
                        />
                        <input
                            type="date"
                            value={item.expiry_date}
                            onChange={e => handleItemChange(index, 'expiry_date', e.target.value)}
                        />
                      </div>
                      {index === items.length - 1 &&
                          <button onClick={addItem} className="add-more-items-button">+</button>}
                    </div>
                ))}
                <button onClick={() => {
                  addItemToFridge();
                  toggleForm();
                }} className="fridge-form-button">Submit All Items
                </button>
                <button onClick={toggleForm} className="fridge-form-button">Cancel</button>
              </>
          )}
        </div>
      </div>
  );
}
