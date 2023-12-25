from .snow_data import SnowData
import streamlit as st

class image_generation:
    '''
    Creates an svg image in a grid. Uses pre-defined svg strings
    '''
    def __init__(self, list_of_years=[SnowData]) -> str:

        # loads svg_data_from files:
        self.images = self._load_svg()






    def _load_svg(self):
        filenames = [
            "INFO",
            "TOP",
            "SNOW_LEVEL_ERROR",
            "SNOW_LEVEL_NONE",
            "SNOW_LEVEL_TRACE",
            "SNOW_LEVEL_LOW",
            "SNOW_LEVEL_MODERATE",
            "SNOW_LEVEL_TRACE",
            "SNOW_LEVEL_HEAVY",
            "SNOW_LEVEL_SEVERE",
        ]

        image_dict = {}

        for file in filenames:
            image_dict[file] = self._load_svg_file(file_path=f"Graphics/svg_parts/{file}.svg")

        # print(image_dict)

        return image_dict

    def _load_svg_file(self,file_path):
        try:
            with open(file_path, 'r') as file:
                svg_content = file.read()
            return svg_content
        except FileNotFoundError:
            st.write(f"Error: File '{file_path}' not found.")
            return None
        except Exception as e:
            st.write(f"Error: Unable to load SVG file. {e}")
            return None

    def _alter_text_in_image(self, svg_str, title=None, sub_title=None, info=None, year=None, snow_depth=None):
        return_svg = svg_str

        if title is not None:
            return_svg.replace("TITLE_TEXT", title)

        if sub_title is not None:
            return_svg.replace("SUB_TEXT", sub_title)

        if info is not None:
            return_svg.replace("INFO_TEXT", info)

        if year is not None:
            return_svg.replace("YEAR_TEXT", year)

        if year is not None:
            return_svg.replace("SNOW_DEPTH_TEXT", snow_depth)

        return return_svg