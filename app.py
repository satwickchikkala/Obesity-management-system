from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Function to calculate BMI
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# Function to calculate Waist-to-Hip Ratio (WHR)
def calculate_whr(waist, hip):
    return round(waist / hip, 2)

# Function to calculate Basal Metabolic Rate (BMR)
def calculate_bmr(weight, height, age, gender):
    if gender == 'Male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * age)
    return round(bmr, 2)

# Function to predict health risk based on BMI and WHR
def predict_health_risk(bmi, whr, gender):
    # Determine BMI risk
    if bmi >= 30:
        bmi_risk = "Obesity"
    elif bmi >= 25:
        bmi_risk = "Overweight"
    else:
        bmi_risk = "Healthy Weight"
    
    # Determine WHR risk based on gender
    if gender == 'Male':
        if whr >= 1.0:
            whr_risk = "Obesity Risk"
        elif whr >= 0.90:
            whr_risk = "Overweight"
        else:
            whr_risk = "Healthy Weight"
    else:  # Female
        if whr >= 0.85:
            whr_risk = "Obesity Risk"
        elif whr >= 0.80:
            whr_risk = "Overweight"
        else:
            whr_risk = "Healthy Weight"
    
    # Determine the overall health risk based on both BMI and WHR
    if bmi_risk == "Obesity" or whr_risk == "Obesity Risk":
        return "Risk of Obesity"
    elif bmi_risk == "Overweight" or whr_risk == "Overweight":
        return "Overweight"
    elif bmi_risk == "Healthy Weight" and whr_risk == "Healthy Weight":
        return "Healthy Weight"
    else:
        return "Mixed Risk"  # In case BMI and WHR fall into different categories, we can label it as "Mixed Risk"

# Route to render the input form (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and show results
@app.route('/', methods=['POST'])
def results():
    # Retrieve form data
    name = request.form['name']
    age = int(request.form['age'])
    gender = request.form['gender']
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    waist = float(request.form['waist'])
    hip = float(request.form['hip'])

    # Calculate BMI, WHR, and BMR
    bmi = calculate_bmi(weight, height)
    whr = calculate_whr(waist, hip)
    bmr = calculate_bmr(weight, height, age, gender)
    prediction = predict_health_risk(bmi, whr, gender)

    # Create patient data dictionary
    patient = {
        'name': name,
        'age': age,
        'gender': gender,
        'height': height,
        'weight': weight,
        'waist': waist,
        'hip': hip,
        'bmi': bmi,
        'whr': whr,
        'bmr': bmr,
        'prediction': prediction
    }

    # Render result.html and pass patient data to it
    return render_template('result.html', patient=patient)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5002)