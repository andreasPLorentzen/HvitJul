from src.streamlit_app import wrapper_page
from src.svg_img import image_generation
import streamlit as st

if __name__ == "__main__":
    image_generator = image_generation([])

    for index, image in image_generator.images.items():
        st.write(image[0:100])
        st.image(image, caption=index)

    #wrapper_page()