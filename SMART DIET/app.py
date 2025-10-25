from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_calories(age, gender, weight, height, activity_level, goal):
    """
    Calculates the target daily calories using the Mifflin-St Jeor equation.
    """
    # 1. Calculate BMR (Basal Metabolic Rate)
    if gender == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else: # 'female'
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
    # 2. Define activity multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    # 3. Calculate TDEE (Total Daily Energy Expenditure)
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    
    # 4. Adjust calories based on the goal
    if goal == 'lose':
        target_calories = tdee - 500  # 500 calorie deficit
    elif goal == 'gain':
        target_calories = tdee + 500  # 500 calorie surplus
    else: # 'maintain'
        target_calories = tdee
        
    return int(target_calories)

def generate_diet_plan(calories):
    """
    Generates a *sample* diet plan based on calorie target.
    This is a simple placeholder. A real app would use a database.
    """
    if calories < 1800:
        plan = """
        **Goal: Weight Loss (Low Calorie)**
        
        * **Breakfast:** Scrambled eggs (2) with spinach and 1 slice of whole-wheat toast.
        * **Lunch:** Large mixed green salad with grilled chicken breast (100g) and a light vinaigrette.
        * **Snack:** A handful of almonds or a Greek yogurt.
        * **Dinner:** Baked salmon (150g) with a side of steamed broccoli and quinoa (1/2 cup).
        """
    elif 1800 <= calories < 2500:
        plan = """
        **Goal: Maintenance (Moderate Calorie)**
        
        * **Breakfast:** Oatmeal (1 cup) cooked with milk, topped with berries and a tablespoon of peanut butter.
        * **Lunch:** Turkey and avocado wrap on a whole-wheat tortilla, with a side of carrot sticks.
        * **Snack:** Apple slices with peanut butter or a protein bar.
        * **Dinner:** Stir-fried tofu or beef (150g) with mixed vegetables (bell peppers, snap peas, carrots) and brown rice (1 cup).
        """
    else: # calories >= 2500
        plan = """
        **Goal: Weight/Muscle Gain (High Calorie)**
        
        * **Breakfast:** 3-egg omelet with cheese, 2 slices of whole-wheat toast with avocado, and a fruit smoothie.
        * **Lunch:** Large portion (1.5 cups) of pasta with chicken or lentil bolognese sauce and a side salad.
        * **Snack:** Greek yogurt with granola and a banana.
        * **Dinner:** Grilled steak (200g) or large bean burrito, with roasted sweet potatoes and green beans.
        * **Post-Workout:** Protein shake.
        """
    return plan.strip()


@app.route('/')
def index():
    """Renders the homepage with the input form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handles the form submission and displays the result."""
    if request.method == 'POST':
        # Get data from the form
        age = int(request.form['age'])
        gender = request.form['gender']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        activity_level = request.form['activity_level']
        goal = request.form['goal']
        
        # 1. Calculate the "predicted" calories
        target_calories = calculate_calories(age, gender, weight, height, activity_level, goal)
        
        # 2. Generate the sample diet plan
        diet_plan = generate_diet_plan(target_calories)
        
        # 3. Render the result page
        return render_template('result.html', calories=target_calories, plan=diet_plan)

if __name__ == '__main__':
    app.run(debug=True)