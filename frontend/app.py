import streamlit as st
from datetime import date, timedelta
import requests
from api import predict_short , predict_future


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="RideWise",
    page_icon="🚲",
    layout="centered"
)

# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "weather": None,
    "forecast": None,
    "prediction": None,
    "future_prediction": None,
    "prediction_datetime":None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

h1{
    text-align:center;
}

div[data-testid="stCaptionContainer"]{
    text-align:center;
}

div[data-testid="stMetric"]{

    background:#f8fafc;
    border:1px solid #e5e7eb;
    border-radius:12px;
    padding:12px;

}

.stButton>button{

    width:100%;
    border-radius:10px;
    height:45px;
    font-weight:bold;

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HELPERS
# ==========================================================

def metric_card(title, value):
    st.markdown(
        f"""
        <div style="background:#111827;padding:16px 18px;border-radius:14px;border:1px solid #334155;box-shadow:0 6px 16px rgba(0,0,0,0.22);">
            <div style="font-size:0.82rem;color:#94A3B8;font-weight:600;margin-bottom:6px;">{title}</div>
            <div style="font-size:1.35rem;color:#F8FAFC;font-weight:700;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# HEADER
# ==========================================================

st.title("🚲 RideWise")
st.caption("AI-Powered Bike Demand Forecasting using XGBoost")

st.divider()

# ==========================================================
# CITY
# ==========================================================

# cities = [
#     "Bhubaneswar",
#     "Delhi",
#     "Mumbai",
#     "Bangalore",
#     "Hyderabad",
#     "Chennai",
#     "Kolkata",
#     "Pune",
#     "Ahmedabad",
#     "Lucknow",
#     "Jaipur"
# ]

# city = st.selectbox(
#     "📍 Select City",
#     cities
# )

city = st.text_input(
    "📍 Enter City",
    placeholder="e.g. Bhubaneswar"
).strip()

# Reset prediction when city changes
if "last_city" not in st.session_state:
    st.session_state.last_city = city

if city != st.session_state.last_city:

    st.session_state.weather = None
    st.session_state.prediction = None
    st.session_state.forecast = None
    st.session_state.future_prediction = None

    st.session_state.last_city = city


st.divider()

# ==========================================================
# FORECAST TYPE
# ==========================================================

forecast_type = st.radio(
    "Forecast Type",
    [
        "🚲 Short-Term Forecast",
        "📅 Future Date Forecast"
    ]
)

st.divider()

# ==========================================================
# SHORT TERM FORECAST
# ==========================================================

if forecast_type == "🚲 Short-Term Forecast":

    st.subheader("🚲 Next Hour Forecast")

    st.write(
        "Predict bike demand for the **next hour** using live weather and historical demand."
    )

    if st.button(
        "🚲 Predict Bike Demand",
        use_container_width=True
    ):
        if not city:
            st.warning("Please enter a city name.")
        else:
            with st.spinner("Fetching weather and predicting demand..."):

                data = predict_short(city)

                if "error" in data:
                    st.error(data["error"])

                else:
                    st.session_state.weather = data["weather"]
                    st.session_state.prediction = data["prediction"]
                    st.session_state.prediction_datetime = data['prediction_datetime']

    # =====================================================
    # DISPLAY WEATHER
    # =====================================================

    if st.session_state.weather:

        st.subheader("🕒 Prediction Time")

        metric_card(
            "Prediction Time",
            data["prediction_datetime"]
        )

        st.subheader("🌤 Weather")

        c1, c2 = st.columns(2)

        with c1:

            metric_card(
                "🌡 Temperature",
                st.session_state.weather["temperature"]
            )

            metric_card(
                "🌬 Wind Speed",
                st.session_state.weather["windspeed"]
            )

        with c2:

            metric_card(
                "💧 Humidity",
                st.session_state.weather["humidity"]
            )

            metric_card(
                "☁ Weather",
                st.session_state.weather["condition"]
            )

    # =====================================================
    # DISPLAY PREDICTION
    # =====================================================

    if st.session_state.prediction is not None:

        st.divider()

        st.subheader("🚲 Prediction Result")

        metric_card(
            "Predicted Bike Demand",
            f"{int(st.session_state.prediction)} Bikes"
        )

        if st.session_state.prediction < 100:

            st.error("🔴 Low Demand")

        elif st.session_state.prediction < 200:

            st.warning("🟡 Medium Demand")

        else:

            st.success("🟢 High Demand")

        st.progress(
            min(
                st.session_state.prediction / 500,
                1.0
            )
        )

# ==========================================================
# FUTURE FORECAST
# ==========================================================

else:

    st.subheader("📅 Future Date Forecast")

    st.info(
        "Predictions are available only for the next **10 days**."
    )

    today = date.today()

    col1, col2 = st.columns(2)

    with col1:

        selected_date = st.date_input(
            "Forecast Date",
            min_value=today,
            max_value=today + timedelta(days=10)
        )

    with col2:

        selected_time = st.time_input(
            "Forecast Time"
        )

    if st.button(
        "🚲 Predict Bike Demand",
        use_container_width=True
    ):
        if not city:
            st.warning("Please enter a city name.")
        else:
            with st.spinner("Fetching weather and predicting demand..."):

                data = predict_future(
                    city,
                    selected_date,
                    selected_time.hour
                )

                if "error" in data:
                    st.error(data["error"])

                else:
                    st.session_state.forecast = data["weather"]
                    st.session_state.future_prediction = data["prediction"]
                    st.session_state.prediction_datetime = data["prediction_datetime"]

    # =====================================================
    # DISPLAY WEATHER
    # =====================================================

    if st.session_state.forecast:

        st.subheader("🕒 Prediction Time")

        metric_card(
            "Prediction Time",
            st.session_state.prediction_datetime
        )

        st.subheader("🌦 Forecast Weather")

        c1, c2 = st.columns(2)

        with c1:

            metric_card(
                "🌡 Temperature",
                st.session_state.forecast["temperature"]
            )

            metric_card(
                "🌬 Wind Speed",
                st.session_state.forecast["windspeed"]
            )

        with c2:

            metric_card(
                "💧 Humidity",
                st.session_state.forecast["humidity"]
            )

            metric_card(
                "☁ Weather",
                st.session_state.forecast["condition"]
            )

    # =====================================================
    # DISPLAY PREDICTION
    # =====================================================

    if st.session_state.future_prediction is not None:

        st.divider()

        st.subheader("🚲 Prediction Result")

        metric_card(
            "Predicted Bike Demand",
            f"{int(st.session_state.future_prediction)} Bikes"
        )

        if st.session_state.future_prediction < 100:

            st.error("🔴 Low Demand")

        elif st.session_state.future_prediction < 300:

            st.warning("🟡 Medium Demand")

        else:

            st.success("🟢 High Demand")

        st.progress(
            min(
                st.session_state.future_prediction / 500,
                1.0
            )
        )