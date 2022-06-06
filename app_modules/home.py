import streamlit as st
from model.inference import Inference
from model.preprocess import COLUMNS
import pandas as pd
from time import sleep
from .static_html import render, home_version_display

def main_title():
    st.markdown(f"<h1 style='text-align: Center;'>🫀HeartDisease Prediction</h1>", True)

    with st.spinner('Loading Model...'):
        infr = Inference()
        render(home_version_display, 29, v = infr.version)
        sleep(1)
    st.write('---')
    return infr

def form_section(form):
    data = {}
    with form.form("section1"):
            col1, col2 = st.columns(2)

            with col1:
                name_ = st.text_input("Enter You're Name 🦸‍♂️", value="User")
                height = st.number_input("Your Height(cm)🧍", min_value=4)
            with col2:
                age = st.selectbox("Choose Age Group 👩‍🦲", ('18-24','25-29','30-34','35-39', '40-44','45-49',
                                                '50-54','55-59','60-64','65-69','70-74', '75-79',
                                                '80 or older'))
                weight = st.number_input("Your Weight(kg)🚶‍♂️", min_value=5)
                bmi_ = 0 if height == 0 or weight == 0 else round(weight / (height/100)**2, 2)
            
            col1_, col2_ = st.columns(2)

            with col1_:
                drink = st.selectbox("Do You Drink 🍾",('No', 'Yes'))
                asthma = st.selectbox("Do You Have Asthma🫁",('No', 'Yes'))
                diabetics = st.selectbox("Are You Diabetic 🍬", ('Yes', 'No'))
                sleeptime = st.number_input("Your avg sleep time 😴", min_value=3)
                mental_health = st.number_input("You're Mental Health❤️‍🩹", min_value=0, max_value=30)
                skin_cancer = st.selectbox("Do You Have Skin Cancer🤚",('No', 'Yes'))
            with col2_:
                smoke = st.selectbox("Do You Smoke 🚭",('Yes', 'No'))
                stroke = st.selectbox("Do You Have Stroke💔",('No', 'Yes'))
                diffwalking = st.selectbox("Do You Have DiffWalking 🚶", ('Yes', 'No'))
                kidney_disease = st.selectbox("Do You Have Kindney Diseases🤚",('No', 'Yes'))
                physical_health = st.number_input("You're Physical Health ❤️‍🩹🏃‍♀️", max_value=30)
                physical_activity = st.selectbox("Are You PhysicalActivity 🏃‍♀️",('Yes', 'No'))

            health_status = st.selectbox("You're Health Status 🧑‍⚕️❤️‍🩹", 
                                    ('Excellent','Very good',
                                    'Good', 'Fair', 'Poor'))
            warning = st.empty()
            if st.form_submit_button("Get Result"):
                if bmi_ != 0:
                    data["Name"] = name_
                    data["BMI"] = [bmi_]
                    data["AgeCategory"] = [age]
                    data['AlcoholDrinking'] = [drink]
                    data['Asthma'] = [asthma]
                    data['Diabetic'] = [diabetics]
                    data['Smoking'] = [smoke]
                    data['Stroke'] = [stroke]
                    data['DiffWalking'] = [diffwalking]
                    data['SleepTime'] = [sleeptime]
                    data['MentalHealth'] = [mental_health]
                    data['PhysicalHealth'] = [physical_health]
                    data['SkinCancer'] = [skin_cancer]
                    data['KidneyDisease'] = [kidney_disease]
                    data['PhysicalActivity'] = [physical_activity]
                    data['GenHealth'] = [health_status]
                    return True, data
                else: warning.warning("Please fill all details...")

    return False, False     


def collect_data():
    data = {}
    status = False
    form_head = st.empty()
    form_head.markdown(f"<h4 style='text-align: center;'>Enter Details to Check HeartDisease</h4>", True)
    form = st.empty()
    status, data = form_section(form)
    if status:
        form_head.empty()
        form.empty()
    return status, data

def write_prediction(rslt, data, infr):
    rslt.warning("Getting Predition")
    sleep(1)
    username = data['Name']
    data.pop('Name')
    df = pd.DataFrame(data)
    pred = infr.predict(df[COLUMNS])
    st.write(pred)
    predictions = pred['predictions']
    if pred['predicted'] == 'Yes':
        st.snow()
        rslt.subheader(f"{username}! There is an {round(predictions['Yes'] * 100)}% Chance you have Heart Disease😔 Please ping with doctor🧑‍⚕️")
    else:
        rslt.subheader(f"Hurray💕, {round(predictions['No'] * 100)}% Sure You Don't Have HeartDiseases😊Stay Healthy🏃‍♀️")
        st.balloons()

def home():
    infr = main_title()
    prediciton_rslt = st.empty()
    status, data = collect_data()
    if status:
        write_prediction(prediciton_rslt, data, infr)
        if st.button("Show Form"):
            home()
        
    
