from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application


@app.route('/')
def index():
    return redirect(url_for('predict_datapoint'))


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'POST':
        gender = request.form.get('gender')
        ethnicity = request.form.get('ethnicity')
        parental = request.form.get('parental_level_of_education')
        lunch = request.form.get('lunch')
        test_prep = request.form.get('test_preparation_course')
        reading = float(request.form.get('reading_score'))
        writing = float(request.form.get('writing_score'))

        data = CustomData(
            gender=gender,
            race_ethnicity=ethnicity,
            parental_level_of_education=parental,
            lunch=lunch,
            test_preparation_course=test_prep,
            reading_score=reading,
            writing_score=writing
        )

        pred_df = data.get_data_as_dataframe()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        return render_template('home.html',
         results=round(results[0], 2),
         gender=request.form.get('gender'),
         ethnicity=request.form.get('ethnicity'),
         parental=request.form.get('parental_level_of_education'),
         lunch=request.form.get('lunch'),
         test_prep=request.form.get('test_preparation_course'),
        reading=request.form.get('reading_score'),
        writing=request.form.get('writing_score')
)
        

    return render_template('home.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)