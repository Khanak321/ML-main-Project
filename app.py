from flask import Flask, request, render_template
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Initialize Flask application
application = Flask(__name__)
app = application

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html') 

# Route for prediction
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            # Fetching input data from form
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )
            
            # Convert data to DataFrame
            pred_df = data.get_data_as_data_frame()
            print(f"Input DataFrame: \n{pred_df}")

            # Initialize prediction pipeline and make predictions
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            print(f"Prediction Results: {results}")

            # Render results on the home page
            return render_template('home.html', results=results[0])

        except Exception as e:
            # Handle exceptions and display error on the page
            print(f"Error during prediction: {e}")
            return render_template('home.html', error=f"An error occurred: {e}")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
