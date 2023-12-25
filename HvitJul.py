# from src.streamlit_app import wrapper_page
from src.svg_img import image_generation
import streamlit as st

if __name__ == "__main__":
    image_generator = image_generation([])
    st.write(image_generator)
    for index, image in image_generator.images.items():
        st.write(image)
        st.image(image, caption=index)

    #wrapper_page()