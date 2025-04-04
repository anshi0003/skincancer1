# Demo feature

import PIL
import streamlit as st
import tensorflow as tf

st.set_page_config(
    page_title="Diagnose Demo",
    page_icon="♋",
    layout="centered",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("pages/model.h5")
    return model


st.title("Skin Cancer Detection")

pic = st.file_uploader(
    label="Upload a picture",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False,
    help="Upload a picture of your skin to get a diagnosis",
)

if st.button("Predict"):
    if pic != None:
        st.header("Results")

        cols = st.columns([1, 2])
        with cols[0]:
            st.image(pic, caption=pic.name, use_column_width=True)

        with cols[1]:
            labels = [
                "actinic keratosis",
                "basal cell carcinoma",
                "dermatofibroma",
                "melanoma",
                "nevus",
                "pigmented benign keratosis",
                "seborrheic keratosis",
                "squamous cell carcinoma",
                "vascular lesion",
            ]

            model = load_model()

            with st.spinner("Predicting..."):
                img = PIL.Image.open(pic)
                img = img.resize((180, 180))
                img = tf.keras.preprocessing.image.img_to_array(img)
                img = tf.expand_dims(img, axis=0)

                prediction = model.predict(img)
                prediction = tf.nn.softmax(prediction)

                score = tf.reduce_max(prediction)
                score = tf.round(score * 100, 2)

                prediction = tf.argmax(prediction, axis=1)
                prediction = prediction.numpy()
                prediction = prediction[0]

                disease = labels[prediction].title()
                st.write(f"**Prediction:** `{disease}`")
                st.write(f"**Confidence:** `{score:.2f}%`")
                # st.info(f"The model predicts that the lesion is a **{prediction}** with a confidence of {score}%")

        st.warning(
            ":warning: This is not a medical diagnosis. Please consult a doctor for a professional diagnosis."
        )
    else:
        st.error("Please upload an image")
