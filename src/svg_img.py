from .snow_data import SnowData

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
            print(f"Error: File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error: Unable to load SVG file. {e}")
            return None
