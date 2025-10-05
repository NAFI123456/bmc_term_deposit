import streamlit as st
import pandas as pd
import joblib
import imblearn
import sklearn
import category_encoders

# /opt/anaconda3/bin/python -m streamlit run home.py
st.set_page_config(layout="wide")

model = joblib.load('logreg_model.joblib')

def get_prediction(data:pd.DataFrame):
    pred = model.predict(data)
    pred_proba = model.predict_proba(data)
    return pred, pred_proba

page = st.sidebar.selectbox("Please pick your preference", ["Home", "Macro Economics", "Predict"])

if page == "Home":
    st.title("Home Page")
    st.write("Welcome to the Deposit Subscription Predictor! This program uses customer " \
    "information—such as age, job type, marital status, previous campaign outcomes, and contact method—to estimate the likelihood that a" \
    " customer will subscribe to a deposit. By analyzing these features, the model provides a probability score for each customer, helping banks"
    " and financial teams focus their efforts on high-potential clients. With this tool, you can make data-driven decisions, optimize marketing " \
    "campaigns, and better understand customer behavior, all in one interactive application.")



elif page == "Macro Economics":

    st.title("Macro Economics Information")
    st.write("Macroeconomics studies the economy as a whole, looking at things like growth," \
    " inflation, and unemployment. It helps understand trends and guide decisions to keep the economy stable and improving for everyone.")

    conf, price, employ = st.columns(3)

    conf.markdown(
        """
        <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 10px;">
            <h3>Confidence Index</h3>
            <p>measures how optimistic or pessimistic consumers feel about the overall economy, 
            including their personal financial situation, which can influence spending and saving behavior.</p>

            Value: −18.7
            Source: OECD
        </div>
        """,
    unsafe_allow_html=True
    )
    
    price.markdown(
        """
        <div style="border: 2px solid #2196F3; padding: 15px; border-radius: 10px;">
            <h3>Price Index</h3>
            <p>tracks changes in the average prices of a basket of goods and services over time,
            providing an indicator of inflation and the cost of living.</p>

            Value: 93.6
            Source: Mean of cons.price.idx in the dataset
        </div> 
        """,
    unsafe_allow_html=True
    )

    employ.markdown(
        """
        <div style="border: 2px solid #FF9800; padding: 15px; border-radius: 10px;">
            <h3>Employment Rate</h3>
            <p>represents the total number of people employed in the economy, reflecting labor market health and overall economic activity.</p>

            Value: 4,499.5
            Source: Statistics Portugal
        </div>
        """,
    unsafe_allow_html=True
    )

elif page == "Predict":


    st.title("Predict Page")
    st.write("Please Input Feature Values To Predict an Output")

    cus_info, offers , prev_cont= st.columns(3, gap='large')

    cus_info.subheader("Customer's Info")
    input_age = cus_info.number_input("Customer's Age: ", min_value=0, max_value=100, value=20, step=10)
    select_marital = cus_info.selectbox('Marital Status: ', ['Married', 'Single', 'Divorced'])
    select_job = cus_info.selectbox('Occupancy: ', ['Housemaid', 'Services', 'Administrative', 'Blue-collar', 'Technician', 'Retired', 'Management',
                                                   'Unemployed', 'Self-Employed', 'Entrepreneur', 'Student'])
    select_education = cus_info.selectbox('Education Status: ', ['Basic 4 Years', 'High School', 'Basic 6 Years', 'Basic 9 Years', 'Professional Course',
                                                                'Other', 'University Degree', 'Illiterate'])
    
    offers.subheader('Offers To Customer')
    input_previous = offers.number_input('Previous Contacts Done: ', min_value=0, max_value=10, value=0, step=1)
    input_campaign = offers.number_input('Campaign Offered: ', min_value=1, max_value=20, value=1, step=1)

    offers.write('')
    contact_meth = offers.radio('Contact Method: ', ['Cellular', 'Telephone'])

    offers.write('')
    default = offers.radio('Credit Default: ', ['Yes', 'No', 'Unknown'])

    prev_cont.subheader('Contacts Information')

    month = prev_cont.selectbox('Last Contact Month: ', ['March', 'April', 'May', 'June', 'July', 'August', 'September'
                                                         , 'October', 'November', 'December'])
    day = prev_cont.selectbox('Last Contact Day: ', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

    # Macro Economic Values
    confidence_index = -18.7
    inflation_index = 93.6
    number_employed = 4499.5

    input_data = {
        'age': [input_age],
        'marital': [select_marital],
        'job': [select_job],
        'education': [select_education],

        'previous':[input_previous],
        'campaign':[input_campaign],

        'contact': [contact_meth],

        'default': [default],

        'month': [month],
        'day_of_week': [day],

        'cons.conf.idx':[confidence_index],
        'cons.price.idx':[inflation_index],
        'nr.employed':[number_employed]
    }

    data = pd.DataFrame(input_data)

    data_display = data.copy()

    display_columns = {
    "age": "Customer's Age",
    "marital": "Marital Status",
    "education": "Education",
    "previous": "Previous Contacts",
    "campaign": "Campaigns Offered",
    "contact": "Contact Method",
    "default": "Has Unpaid Credit",
    "month": "Last Contact Month",
    "day_of_week": "Last Contact Day",
    "cons.conf.idx": "Confidence Index",
    "cons.price.idx": "Inflation Index",
    "nr.employed": "Number Employed"
    }

    formatters = {
    "Confidence Index": lambda x: f"{x:,.1f}",
    "Inflation Index": lambda x: f"{x:,.1f}",
    "Number Employed": lambda x: f"{x:,.1f}",
}

    data_display = data_display.rename(columns=display_columns)

    styled = (
    data_display.style
    .format(formatters)
    .set_table_styles(
        [
            {"selector": "th", "props": [("text-align", "center !important")]},
            {"selector": "td", "props": [("text-align", "center !important")]}
        ]
    )
)
    st.markdown(
    styled.to_html(index=False).replace(
        '<table border="1" class="dataframe">',
        '<table style="margin-left:auto;margin-right:auto;text-align:center;border-collapse:collapse;" border="1" class="dataframe">'
    ),
    unsafe_allow_html=True
)
    

    pred_data = pd.DataFrame({
        'age': [input_age],
        'marital': [select_marital.lower()],
        'job': [select_job.lower()],
        'education': [select_education.replace(' Years', 'y').replace(' ', '.').lower()],

        'previous':[input_previous],
        'campaign':[input_campaign],

        'contact': [contact_meth.lower()],

        'default': [default.lower()],

        'month': [month[:3].lower()],
        'day_of_week': [day[:3].lower()],

        'cons.conf.idx':[confidence_index],
        'cons.price.idx':[inflation_index],
        'nr.employed':[number_employed]
    })

    # Predict Button
    st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    if st.button("Predict Customer Churn"):
        # Drop Surname from prediction

        # Predict
        pred, pred_proba = get_prediction(pred_data)
        label_map = {0: "No Deposit", 1: "Deposit"}

        label_pred = label_map[pred[0]]
        proba_no_deposit = pred_proba[0][0]
        proba_deposit = pred_proba[0][1]

        # Show result
        st.subheader("Prediction Result")
    

        if pred[0] == 1:
            st.success("The customer is likely to **Deposit**")
        else:
            st.error("The customer is likely to **Not Deposit**")

        # Show probabilities
        st.write("### Prediction Probabilities")
        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="No Subscribe Probability", value=f"{proba_no_deposit:.0%}")
            st.progress(int(proba_no_deposit * 100))

        with col2:
            st.metric(label="Subscribe Probability", value=f"{proba_deposit:.0%}")
            st.progress(int(proba_deposit * 100))

