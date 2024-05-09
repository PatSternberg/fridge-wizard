import AxiosInstance from '../components/axios';
import { useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import '../styles.css';
import '../App.css';

export default function Recipes() {
    const location = useLocation();
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

    // console.log(recipes)
    return [
    <div key="recipes-list-container">
        {recipes.map((recipe, index) => (
            <div class="recipe-container">
                <h1 class="recipe-headers">{recipe.title}</h1>
                <img src={recipe.image} alt="" width="500" height="400"></img>
                <h2 class="recipe-headers">Required Ingredients:</h2>
                <ul>
                {recipe.ingredients.map((ingredient, index) => (
                    <li class="list-padding" key={index}>{ingredient}</li>
                ))}
                </ul>
                <h2 class="recipe-headers">Instructions:</h2>
                {recipe.instructions.map((instruction, index) => (
                    <ol key={index}>
                        {instruction.steps.map((step, index) => (    
                            <li class="list-padding">{step.step}</li>
                        ))}
                    </ol>
                ))}
            </div>
        ))}
    </div>
]
}