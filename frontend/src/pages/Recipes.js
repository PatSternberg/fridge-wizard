import React from 'react';
import AxiosInstance from '../components/axios';
import { useLocation, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import '../styles.css';
import '../App.css';

export default function Recipes() {
    const location = useLocation();
    const navigate = useNavigate();
    const userId = location.state && location.state.user_id;
    
    console.log(userId)
    
    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        if (true) {
            getRecipes();
        }
    }, [userId]);


    function getRecipes() {
        AxiosInstance.get( 'fridges/get-recipes/', { params: { user_id: userId  } })
        .then(response => {
        console.log(response)
        setRecipes(response.data.message)
        })
        .catch((error) => {
          // Handle error if POST request fails
          console.error('Error:', error);
        });
      }

    function navigateToFridge() {
        navigate('/fridge/');
    };

    // console.log(recipes)
    return [
    <div key="recipes-list-container" className='recipes-list-container'>
        <h2>My recipes</h2>
        <button onClick={navigateToFridge}>
            <ArrowBackIosNewIcon /><h1>FH</h1>
        </button>
        {recipes.map((recipe, index) => (
            <div class="recipe-container">
                <div class="recipe-box">
                    <h1 class="recipe-headers">{recipe.title}</h1>
                    <div class="recipe-image">
                        <img src={recipe.image} alt=""></img>
                    </div>
                    <h2 class="recipe-headers">Required Ingredients:</h2>
                    <ul>
                    {recipe.ingredients.map((ingredient, index) => (
                        <li class="list-padding" key={index}>{ingredient}</li>
                    ))}
                    </ul>
                </div>
                <div class="recipe-box">
                    <h2 class="recipe-headers">Instructions:</h2>
                    {recipe.instructions.map((instruction, index) => (
                        <ol key={index}>
                            {instruction.steps.map((step, index) => (    
                                <li class="list-padding">{step.step}</li>
                            ))}
                        </ol>
                    ))}
                </div>
            </div>
        ))}
    </div>
]
}