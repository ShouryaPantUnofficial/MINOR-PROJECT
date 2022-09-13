from flask import Flask, render_template, request, url_for, send_file, flash, redirect, make_response
import pickle
import numpy as np
import os
import json
import termcolor
import smtplib

#import CurrentStats
# import CancerModel
# import PdfConverter
# from PdfConverter import PDFPageCountError
import DiseasePred

# import warnings

app = Flask(__name__)
app.config['SECRET_KEY'] = '73a4b6ca8cb647a20b71423e31492452'

# For Coronavirus
with open("Coronavirus_logistic", "rb") as f:
    modelc = pickle.load(f)


# For Chronic kidney disease
with open("CKD_Model", "rb") as f:
    decisionTree = pickle.load(f)

# For Heart Disease
with open("HeartDisease.pkl","rb") as f:
    model = pickle.load(f)

# For Diabetes Prediction
with open("diabetesprediction.pkl","rb") as f:
    diabetes=pickle.load(f)

@app.route("/")
@app.route("/home")
def Homepage():
    # cases, cured, death = CurrentStats.currentStatus()
    return render_template("Homepage.html", feedback="False")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("PageNotFound.html")


# @app.route("/currentstats", methods=["POST", "GET"])
# def CurrentStatus():
#     cases, cured, death = CurrentStats.currentStatus()
#     scases = scured = sdeath = 0
#     state = ""
#     try:
#         if request.method == "POST":
#             # print(request.form)
#             formDict = request.form
#             state = formDict['state']
#             # print(state)
#             scases, scured, sdeath = CurrentStats.StateStatus(state)
#     except UnboundLocalError:
#         flash("The State is not Affected Yet")
#     except ValueError:
#         flash("The State is not Affected Yet")
#     return render_template("CurrentStats.html", state=state, scases=scases, scured=scured, sdeath=sdeath, cases=cases, cured=cured, death=death, title="Current Statistics", navTitle="Current Status", headText="Coronavirus Current Stats Statewise", ImagePath="/static/Virus.png")


@app.route("/about")
def About():
    return render_template("About.html")


@app.route("/contact", methods=["POST", "GET"])
def Contact():
    if request.method == "POST":
        # print(request.form)
        contactDict = request.form
        firstname = contactDict['firstname']
        lastname = contactDict['lastname']
        email = contactDict['email']
        phone = int(contactDict['phone'])
        description = contactDict['description']

        subject = "Medical Website feedback !!"
        message = f"First Name : {firstname} \nLast Name : {lastname} \nEmail : {email}\nPhone Number : {phone}\nDescription : {description}\n"
        content = f"Subject : {subject} \n\n{message}"
        sender = "intmain1221@gmail.com"
        receiver = "intmain1221@gmail.com"
        password = "intmain@11"

        print(content)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as mail:
                mail.ehlo()
                mail.starttls()
                mail.login(sender, password)
                mail.ehlo()
                mail.sendmail(sender, receiver, content)

            print("Mail Send Successfully !")
            #cases, cured, death = CurrentStats.currentStatus()
            return render_template("Homepage.html", cases=cases, cured=cured, death=death, feedback="True")

        except:
            pass
    return render_template("Contact.html")


@app.route("/infected")
def Infected():
    return render_template("Infected.htm", disease="Nothing")


@app.route("/noninfected")
def NonInfected():
    return render_template("NonInfected.htm")


@app.route("/download")
def Download():
    file = "static/Example.docx"
    return send_file(file, as_attachment=True)


@app.route('/DiabetesPrediction', methods=['POST','GET'])
def Diabetes_prediction():
    if request.method == 'POST':
        preg = int(request.form['pregnancies'])
        glucose = int(request.form['glucose'])
        bp = int(request.form['bloodpressure'])
        st = int(request.form['skinthickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        age = int(request.form['age'])
        
        data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
        prediction = diabetes.predict(data)
        
        if prediction:
            return render_template("Infected.htm",disease="Diabetes")
        else:
            return render_template("NonInfected.htm")
        
    return render_template("Diabetes.html", title="Diabetes Detector", navTitle="Diabetes Detector", headText="Diabetes Predictor", ImagePath="/static/diabetes.jpg")

@app.route("/HeartDisease", methods=["POST", "GET"])
def Heart_disease():
    if request.method == 'POST':

        age = int(request.form['age'])
        sex = request.form.get('sex')
        cp = request.form.get('cp')
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs = request.form.get('fbs')
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])
        exang = request.form.get('exang')
        oldpeak = float(request.form['oldpeak'])
        slope = request.form.get('slope')
        ca = int(request.form['ca'])
        thal = request.form.get('thal')
        
        data = np.array([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
        prediction = model.predict(data)

        if prediction:
            return render_template("Infected.htm", disease="Heart Disease")
        else:
            return render_template("NonInfected.htm")

    return render_template("HeartDisease.html", title="Heart Disease Detector", navTitle="Heart Disease Detector", headText="Heart Disease Probabilty Detector", ImagePath="/static/HeartPulse.png")


@app.route("/diseaseprediction", methods=["POST", "GET"])
def Disease():
    symptoms = []
    if request.method == "POST":
        rf = request.form
        # print(rf)
        for key, value in rf.items():
            # print(key)
            symptoms.append(value)
        print(symptoms)

        if len(symptoms) < 5 or len(symptoms) > 8:
            flash("Please Select symptoms only between 5 and 8 Inclusive")
        else:
            prediction = DiseasePred.predicts(symptoms)
            if prediction:
                return render_template("Infected.htm", disease=prediction)
            else:
                return render_template("NonInfected.htm")
    return render_template("dp.html")


@app.route("/ChronicKidneyDiseasePrediction", methods=["POST", "GET"])
def CKD():
    if request.method == "POST":
        submitted_values = request.form
        sg = str(float(submitted_values["sg"].strip()))
        albumin = str(float(submitted_values["albumin"].strip()))
        hemoglobin = str(float(submitted_values["hemoglobin"].strip()))
        pcv = str(float(submitted_values["pcv"].strip()))
        hypertension = str(float(submitted_values["hypertension"].strip()))
        sc = str(float(submitted_values["sc"].strip()))

        ckd_inputs1 = [sg, albumin, sc, hemoglobin, pcv, hypertension]
        prediction = decisionTree.predict([ckd_inputs1])
        # print("**************             ", prediction)
        if not prediction:
            return render_template("Infected.htm", disease="Chronic Kidney Disease")
        else:
            return render_template("NonInfected.htm")

    return render_template("ChronicKidney.html", title="Chronic Kidney Disease", navTitle="Chronic Kidney Disease", headText="Chronic Kidney Disease Detector", ImagePath="/static/Chronic_Kidney.png")


@app.route("/CoronavirusPrediction", methods=["POST", "GET"])
def Coronavirus():
    if request.method == "POST":
        # print(request.form)
        submitted_values = request.form
        temperature = float(submitted_values["temperature"].strip())
        age = int(submitted_values["age"])
        cough = int(submitted_values["cough"])
        cold = int(submitted_values["cold"])
        sore_throat = int(submitted_values["sore_throat"])
        body_pain = int(submitted_values["body_pain"])
        fatigue = int(submitted_values["fatigue"])
        headache = int(submitted_values["headache"])
        diarrhea = int(submitted_values["diarrhea"])
        difficult_breathing = int(submitted_values["difficult_breathing"])
        travelled14 = int(submitted_values["travelled14"])
        travel_covid = int(submitted_values["travel_covid"])
        covid_contact = int(submitted_values["covid_contact"])

        age = 2 if (age > 50 or age < 10) else 0
        temperature = 1 if temperature > 98 else 0
        difficult_breathing = 2 if difficult_breathing else 0
        travelled14 = 3 if travelled14 else 0
        travel_covid = 3 if travel_covid else 0
        covid_contact = 3 if covid_contact else 0

        model_inputs = [cough, cold, diarrhea,
                        sore_throat, body_pain, headache, temperature, difficult_breathing, fatigue, travelled14, travel_covid, covid_contact, age]
        prediction = modelc.predict([model_inputs])[0]
        # print("**************             ", prediction)
        if prediction:
            return render_template("Infected.htm", disease="Coronavirus")
        else:
            return render_template("NonInfected.htm")

    return render_template("Coronavirus.htm", title="Coronavirus Prediction", navTitle="COVID-19 Detector", headText="Coronavirus Probability Detector", ImagePath="/static/VirusImage.png")
    

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
