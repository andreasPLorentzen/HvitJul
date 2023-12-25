from .snow_data import SnowData
import streamlit as st


from xml.etree.ElementTree import Element, fromstring, tostring, SubElement

class image_generation:
    '''
    Creates an svg image in a grid. Uses pre-defined svg strings
    '''
    def __init__(self, list_of_years=[SnowData], title="unknown", sub_title="Meh") -> str:

        # loads svg_data_from files:
        self.images = self._load_svg()

        # create svg strings
        svg_list = []
        for year_obj in list_of_years:
            year = year_obj.date.year
            condition = year_obj.snow_level()
            depth = f"{year_obj.sd} cm"  # cm
            # alter the svg
            svg_list.append(self._alter_text_in_image( self.images[condition.name], year=year,snow_depth=depth))


        # alter top and info
        top = self._alter_text_in_image(self.images["TOP"],title=title, sub_title=sub_title)
        info = self._alter_text_in_image(self.images["INFO"], info="Generert ved bruk av API til Kartverket og NVE, Utviklet av Andreas og Johannes Lorentzen")

        # generate image:
        self.result_image = self._create_svg_grid_str(svg_list,top,info,images_per_row=5)

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


    def _create_svg_grid_str(self, svg_strings, top_svg_string, info_svg_string, images_per_row=10):

        if svg_strings == []:
            return ""

        top_height = 75
        # Assume the viewBox dimensions represent svg_width and svg_height (fallback default size)
        svg_width, svg_height = 100, 150

        # Try to extract width and height from the first SVG string's viewBox for later use
        first_svg = fromstring(svg_strings[0])
        viewbox = first_svg.get('viewBox')
        if viewbox:
            _, _, svg_width, svg_height = map(float, viewbox.split())

        # Parse additional SVG elements for the top and info areas
        top_svg = fromstring(top_svg_string)
        info_svg = fromstring(info_svg_string)

        # Calculate new canvas width and height based on image per row and number of rows needed
        output_width = svg_width * images_per_row
        rows_needed = ((len(svg_strings) + images_per_row - 1) // images_per_row)
        output_height = svg_height * rows_needed + top_height

        # Create the root <svg> element for the output SVG
        output_svg = Element("svg", xmlns="http://www.w3.org/2000/svg", version="1.1")
        output_svg.set("width", str(output_width))
        output_svg.set("height", str(output_height))

        # Set top_svg position at the top center of the grid
        top_svg.set('x', str(output_width / 2 - float(top_svg.get('width', '100')) / 2))
        top_svg.set('y', '0')  # Assuming top SVG's height is less than `svg_height`

        # Set info_svg position at the bottom right of the grid
        info_svg.set('x', str(output_width - float(info_svg.get('width', '100'))))
        info_svg.set('y', str(output_height - float(info_svg.get('height', '50'))))

        # Draw border around the entire grid
        border_width=5
        # border_rect = SubElement(output_svg, "rect", {
        #     "x": str(border_width / 2),
        #     "y": str(border_width / 2 + top_height),
        #     "width": str(output_width),
        #     "height": str(output_height),
        #     "fill": "none",
        #     "stroke": "black",
        #     "stroke-width": str(border_width)
        # })

        # Create alternating background rectangles
        # colors = ["#D1EBE1"]
        # for i in range(2):
        background_rect = SubElement(output_svg, "rect", {
            "x": str(border_width / 2),
            "y": str(border_width / 2 + top_height),
            "width": str(output_width),
            "height": str(output_height),
            "fill": "#F0F5FC",
            "stroke": "#D1EBE1",
            "stroke-width": str(border_width)
            })


        # Append the top SVG element
        output_svg.append(top_svg)

        # Iterate over SVG strings, update the year text and calculate their positions
        # Include them starting from the second row to leave space for the top SVG at first row
        for idx, svg_string in enumerate(svg_strings):
            svg = fromstring(svg_string)

            # Update the year text
            for text in svg.iter():
                if text.text and 'YEAR_TEXT' in text.text:
                    text.text = text.text.replace('YEAR_TEXT', '2023')

            # Calculate new x, y positions based on the grid position
            x = (idx % images_per_row) * svg_width
            y = (idx // images_per_row) * svg_height + float(top_svg.get('height', '50'))  # Offset by top_svg's height
            svg.set('x', str(x))
            svg.set('y', str(y))

            # Append updated SVG directly to the root SVG container
            output_svg.append(svg)

        # Append the info SVG element last so it renders on top of other elements (if there are overlapping issues)
        output_svg.append(info_svg)

        # Convert output SVG element tree back to a string and return it
        return tostring(output_svg, encoding='unicode')