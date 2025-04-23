from flask import Flask, render_template, request

app = Flask(__name__)

# Sample recipes dictionary with more detailed information
recipes = {
    'Chicken Bowl': {'ingredients': ['Chicken', 'Rice'], 'time': '30 minutes', 'instructions': 'Cook rice, grill chicken, and combine.'},
    'Broccoli Sticks': {'ingredients': ['Broccoli', 'Cheese'], 'time': '20 minutes', 'instructions': 'Steam broccoli and melt cheese on top.'},
    'Spinach Potato Bites': {'ingredients': ['Spinach', 'Potato'], 'time': '25 minutes', 'instructions': 'Boil potatoes, sauté spinach, and combine.'},
    'Garlic Tomato': {'ingredients': ['Garlic', 'Tomato'], 'time': '15 minutes', 'instructions': 'Sauté garlic, add tomatoes, and cook for 10 minutes.'},
    'Vegetable Stir Fry': {'ingredients': ['Broccoli', 'Spinach', 'Carrot', 'Onion', 'Zucchini'], 'time': '40 minutes', 'instructions': 'Stir fry all veggies in olive oil.'},
    'Potato Soup': {'ingredients': ['Potato', 'Onion', 'Garlic', 'Carrot'], 'time': '50 minutes', 'instructions': 'Boil vegetables and blend them into a smooth soup.'},
}

# Sample list of ingredients and possible substitutions
ingredients_list = ['Chicken', 'Rice', 'Broccoli', 'Cheese', 'Spinach', 'Tomato', 'Onion', 'Carrot', 'Potato', 'Garlic', 'Eggplant', 'Zucchini']
substitutions = {
    'Chicken': ['Tofu', 'Mushrooms'],
    'Cheese': ['Vegan Cheese', 'Nutritional Yeast'],
    'Spinach': ['Kale', 'Lettuce'],
    'Rice': ['Quinoa', 'Cauliflower Rice'],
    'Broccoli': ['Cauliflower', 'Brussels Sprouts'],
}

# Sample dietary restrictions
dietary_restrictions = ['Vegan', 'Gluten-Free']

# Backtracking function to explore substitutions
def backtrack(recipe, dietary_restrictions, current_ingredients, index=0):
    if index == len(recipe['ingredients']):
        return current_ingredients

    ingredient = recipe['ingredients'][index]
    options = substitutions.get(ingredient, [ingredient])  # Get substitution options for the ingredient

    for option in options:
        # Check if the option meets dietary restrictions
        if meets_dietary_restrictions(option, dietary_restrictions):
            # Recursively explore the next ingredient with the current option
            result = backtrack(recipe, dietary_restrictions, current_ingredients + [option], index + 1)
            if result:
                return result

    return None  # No valid combination found

# Function to check if an ingredient meets dietary restrictions
def meets_dietary_restrictions(ingredient, dietary_restrictions):
    # If no dietary restrictions are selected, allow all ingredients
    if not dietary_restrictions:
        return True

    # Example logic for dietary restrictions
    if 'Vegan' in dietary_restrictions and ingredient == 'Chicken':
        return False
    if 'Gluten-Free' in dietary_restrictions and ingredient == 'Rice':  # Example case for gluten
        return False
    return True

# Greedy function to rank recipes based on maximum ingredient matches
def greedy_find_recipes(selected_ingredients):
    recipe_scores = []

    for recipe, details in recipes.items():
        # Count how many ingredients in the recipe match the selected ingredients
        match_count = sum(1 for ingredient in details['ingredients'] if ingredient in selected_ingredients)
        recipe_scores.append((recipe, match_count, details))

    # Sort recipes by match count in descending order (greedy approach)
    recipe_scores.sort(key=lambda x: x[1], reverse=True)

    return [recipe for recipe, _, details in recipe_scores if _ > 0]  # Filter out recipes with no matches

@app.route('/')
def home():
    return render_template('home.html', ingredients=ingredients_list)

@app.route('/results', methods=['POST'])
def results():
    selected_ingredients = request.form.getlist('ingredients')
    dietary_restrictions_selected = request.form.getlist('dietary_restrictions')

    if not dietary_restrictions_selected:
        dietary_restrictions_selected = []

    # Use greedy to find recipes with the most matching ingredients
    matched_recipes = greedy_find_recipes(selected_ingredients)

    final_recipes = []

    for recipe_name in matched_recipes:
        recipe_details = recipes[recipe_name]

        # Apply backtracking only if dietary restrictions are selected
        if dietary_restrictions_selected:
            modified_ingredients = backtrack(recipe_details, dietary_restrictions_selected, [])
        else:
            modified_ingredients = recipe_details['ingredients']

        if modified_ingredients:
            final_recipes.append({
                'name': recipe_name,
                'ingredients': modified_ingredients,
                'time': recipe_details['time'],
                'instructions': recipe_details['instructions'],
            })

    return render_template('result.html', recipes=final_recipes, selected_ingredients=selected_ingredients)

@app.route('/customize', methods=['GET', 'POST'])
def customize():
    if request.method == 'POST':
        selected_recipe = request.form['recipe']
        recipe_details = recipes.get(selected_recipe, {})
        
        # Generate customization options (example substitutions)
        substitutions = {
            'Chicken': ['Tofu', 'Mushrooms'],
            'Cheese': ['Vegan Cheese', 'Nutritional Yeast'],
            'Spinach': ['Kale', 'Lettuce']
        }

        return render_template('customize.html', recipe=recipe_details, substitutions=substitutions)
    
    return "No recipe selected!"

if __name__ == "__main__":
    app.run(debug=True)
