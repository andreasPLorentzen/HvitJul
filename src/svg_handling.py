import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree, fromstring, tostring, SubElement

def update_year_in_svg(svg_element, year="2023"):
    # Iterate through all text elements and replace YEAR_TEXT with the specified year
    for elem in svg_element.iter():
        if elem.text and "YEAR_TEXT" in elem.text:
            elem.text = elem.text.replace("YEAR_TEXT", year)
    return svg_element

def create_svg_grid(svg_paths, output_filename="output_2.svg", images_per_row=10):
    # Assume the viewBox dimensions represent svg_width and svg_height
    # svg_width and svg_height will be extracted from the first SVG in the list for simplicity
    first_tree = ET.parse(svg_paths[0])
    first_svg = first_tree.getroot()
    viewbox = first_svg.get('viewBox')
    if viewbox:
        # Extract width and height from the viewBox attribute
        _, _, svg_width, svg_height = map(float, viewbox.split())
    else:
        # Fallback if no viewBox is provided (not recommended)
        svg_width = 150
        svg_height = 150

    # Create the root <svg> element for the output SVG
    output_svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", version="1.1")
    output_svg.set("width", str(svg_width * images_per_row))  # Dynamic width based on number of images per row and their width
    rows_needed = ((len(svg_paths) + images_per_row - 1) // images_per_row)
    output_svg.set("height", str(svg_height * rows_needed))  # Dynamic height based on rows needed and height of SVGs

    # Iterate over SVG paths, update the year text, and calculate their positions
    for idx, svg_path in enumerate(svg_paths):
        tree = ET.parse(svg_path)
        svg = tree.getroot()

        # Update the year text
        for text in svg.iter():
            if text.text and 'YEAR_TEXT' in text.text:
                text.text = text.text.replace('YEAR_TEXT', '2023')

        # Calculate new x, y positions based on the grid position
        x = (idx % images_per_row) * svg_width
        y = (idx // images_per_row) * svg_height
        svg.set('x', str(x))
        svg.set('y', str(y))

        # Append updated SVG directly to the root SVG container
        output_svg.append(svg)

    # Write the output SVG file
    ET.ElementTree(output_svg).write(output_filename)
    print(output_filename)

# Sample usage:


def create_svg_grid_str(svg_strings, images_per_row=10):
    # Assume the viewBox dimensions represent svg_width and svg_height
    svg_width, svg_height = 100, 150  # fallback default size

    # Try to extract width and height from the first SVG string's viewBox for later use
    first_svg = fromstring(svg_strings[0])
    viewbox = first_svg.get('viewBox')
    if viewbox:
        _, _, svg_width, svg_height = map(float, viewbox.split())

    # Create the root <svg> element for the output SVG
    output_svg = Element("svg", xmlns="http://www.w3.org/2000/svg", version="1.1")
    output_svg.set("width", str(svg_width * images_per_row))  # Dynamic width based on number of images per row and their width
    rows_needed = ((len(svg_strings) + images_per_row - 1) // images_per_row)
    output_svg.set("height", str(svg_height * rows_needed))  # Dynamic height based on rows needed and height of SVGs

    # Iterate over SVG strings, update the year text, and calculate their positions
    for idx, svg_string in enumerate(svg_strings):
        svg = fromstring(svg_string)

        # Update the year text
        for text in svg.iter():
            if text.text and 'YEAR_TEXT' in text.text:
                text.text = text.text.replace('YEAR_TEXT', '2023')

        # Calculate new x, y positions based on the grid position
        x = (idx % images_per_row) * svg_width
        y = (idx // images_per_row) * svg_height
        svg.set('x', str(x))
        svg.set('y', str(y))

        # Append updated SVG directly to the root SVG container
        output_svg.append(svg)

    # Convert the output SVG element tree back to a string and return it
    return tostring(output_svg, encoding='unicode')

def create_svg_grid_str_v2(svg_strings, top_svg_string, info_svg_string, images_per_row=10):
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
    output_height = svg_height * rows_needed + 50

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

def create_svg_grid_test():
    top = '''
    <svg viewBox="0 0 200.337 81.65" width="200.337" height="81.65" xmlns="http://www.w3.org/2000/svg">
      <text style="fill: rgb(51, 51, 51); font-family: Arial, sans-serif; font-size: 24px; font-weight: 700; text-anchor: middle; white-space: pre;" x="79.124" y="37.224" transform="matrix(1.248075008392334, 0, 0, 1.375, -0.27718898653983715, -5.751928806304932)">TITLE_TEXT</text>
      <text style="fill: rgb(51, 51, 51); font-family: Arial, sans-serif; font-size: 11.6364px; font-style: italic; text-anchor: middle; white-space: pre;" transform="matrix(1.248075008392334, 0, 0, 1.375, -2.8451161384582484, 19.80634307861328)" x="79.124" y="37.224">SUB_TEXT</text>
    </svg>
    '''

    info = '''
    <svg viewBox="0 0 132.155 16.835" width="132.155" height="16.835" xmlns="http://www.w3.org/2000/svg">
      <text style="fill: rgb(183, 183, 183); font-family: Arial, sans-serif; font-size: 9px; font-style: italic; text-anchor: end; white-space: pre;" x="125" y="11.363" transform="matrix(1, 0, 0, 1, 3.552713678800501e-15, 0)">INFO_TEXT</text>
    </svg>
    '''
    list_of_strings = []
    for i in range(2000,2023).__reversed__():
        list_of_strings.append(moderate.replace("YEAR_TEXT", str(i)).replace("SNOW_DEPTH_TEXT", "23 cm"))
    # list_of_strings = [
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    #     moderate,
    # ]
    # return_string = create_svg_grid_str(list_of_strings,images_per_row=7)
    top = top.replace("TITLE_TEXT", "Oslo").replace("SUB_TEXT", "Lokasjon bla bla bla")
    info = info.replace("INFO_TEXT", "Laget av Andreas Lorentzen")
    return_string = create_svg_grid_str_v2(list_of_strings, images_per_row=7,top_svg_string=top, info_svg_string=info)

    return return_string

def add_title_to_svg(svg_string, title_text):
    # Parse the SVG string
    svg_tree = fromstring(svg_string)

    # Get width from viewBox or width attribute
    viewbox = svg_tree.get('viewBox')
    if viewbox:
        _, _, width, _ = map(float, viewbox.split())
    else:
        width = float(svg_tree.get('width', '200'))  # Default fallback if neither viewBox nor width are present

    # Define the title element
    title_element = f'<text x="{width / 2}" y="20" text-anchor="middle" font-size="14" font-weight="bold">{title_text}</text>'

    # Prepend the title element to the SVG content
    # fromstring does not parse multiple top level elements, so here we insert into the first element after the opening tag
    svg_content = tostring(svg_tree, encoding='unicode')
    print(svg_content)
    svg_with_title = svg_content.replace('>','>' + title_element, 1)

    return svg_with_title

def enhance_svg(svg_string, title, subtitle, info, border_color="red", border_width=2):
    # Parse the SVG string
    svg_tree = fromstring(svg_string)
    width = svg_tree.get("width", "200")  # default fallback width
    height = svg_tree.get("height", "200")  # default fallback height

    # These offsets will be used to position elements; they are arbitrary and may need adjusting
    title_offset = 50  # Additional space at the top for the title
    info_offset = 20  # Additional space at the bottom for info text
    border_offset = float(border_width) / 2  # Adjust the border to sit nicely within view

    # Convert to float for calculations
    width = float(width)
    height = float(height) + title_offset + info_offset

    # Update the SVG's width and height to make room for the title, subtitle, and info text
    svg_tree.set("width", str(width))
    svg_tree.set("height", str(height))

    # Update any existing content to shift it down by title_offset
    for element in svg_tree:
        if 'transform' in element.attrib:
            transform = element.attrib['transform']
            # Extract and update existing translate values in the transform if needed
            # This part assumes a transform already exists with a translate command
        else:
            element.set("transform", f"translate(0,{title_offset})")

    # Create a red border rectangle
    # border_rect = SubElement(svg_tree, "rect", {
    #     "x": str(border_offset),
    #     "y": str(border_offset + title_offset),
    #     "width": str(width - border_width),
    #     "height": str(height - title_offset - info_offset - border_width),
    #     "fill": "none",
    #     "stroke": border_color,
    #     "stroke-width": str(border_width)
    # })

    # Add title
    title_text = SubElement(svg_tree, "text", {
        "x": str(width / 2),
        "y": str(title_offset / 2),
        "text-anchor": "middle",
        "font-size": "14",
        "font-weight": "bold",
        "fill": border_color
    })
    title_text.text = title

    # Add subtitle
    subtitle_text = SubElement(svg_tree, "text", {
        "x": str(width / 2),
        "y": str(3 * title_offset / 4),
        "text-anchor": "middle",
        "font-size": "10",
        "fill": border_color
    })
    subtitle_text.text = subtitle

    # Add info in the lower right corner
    info_text = SubElement(svg_tree, "text", {
        "x": str(width - 5),
        "y": str(height - 5),
        "text-anchor": "end",
        "font-size": "8",
        "fill": border_color
    })
    info_text.text = info

    # Return the updated SVG as a string
    return tostring(svg_tree, xml_declaration=True, encoding='utf-8', method='xml').decode()

def add_marginalia_to_svg(svg_string, title, subtitle, info_text):
    svg = fromstring(svg_string)

    # Get width and height from viewBox or width/height attributes
    viewbox = svg.get('viewBox')
    if viewbox:
        _, _, width, _ = map(float, viewbox.split())
    else:
        width = float(svg.get('width', '200'))  # Default fallback width if no viewBox present
        height = float(svg.get('height', '200'))  # Default fallback height

    # Transformation to consider title and subtitle height
    title_height = 40
    subtitle_height = 20

    # Update SVG height to add space for title and subtitle
    if viewbox:
        svg.set('viewBox', f'0 0 {width} {height + title_height + subtitle_height}')
    else:
        svg.set('height', str(height + title_height + subtitle_height))

    # Append title text
    title_text = Element('text', {
        'x': str(width / 2),
        'y': str(title_height),
        'font-family': 'Arial',
        'font-size': '40',
        'font-weight': 'bold',
        'text-anchor': 'middle',
        'fill': 'black'  # Adjust as needed
    })
    title_text.text = title

    # Append subtitle text
    subtitle_text = Element('text', {
        'x': str(width / 2),
        'y': str(title_height + subtitle_height),
        'font-family': 'Arial',
        'font-size': '20',
        'text-anchor': 'middle',
        'fill': 'black'  # Adjust as needed
    })
    subtitle_text.text = subtitle

    # Info text
    info_text_element = Element('text', {
        'x': str(width),
        'y': str(height + title_height + subtitle_height - 10),  # 10 is the arbitrary margin
        'font-family': 'Arial',
        'font-size': '10',
        'text-anchor': 'end',
        'fill': 'gray'
    })
    info_text_element.text = info_text

    # Insert the new elements into the existing SVG
    svg.insert(0, info_text_element)
    svg.insert(0, subtitle_text)
    svg.insert(0, title_text)

    # Return updated SVG as a string
    return tostring(svg, encoding='unicode')



moderate = '''
<svg viewBox="0.399 2.635 100.195 124.401" width="100.195" height="124.401" xmlns="http://www.w3.org/2000/svg" xmlns:bx="https://boxy-svg.com">
  <defs>
    <linearGradient gradientUnits="userSpaceOnUse" x1="204.604" y1="218.348" x2="204.604" y2="225.014" id="gradient-0" gradientTransform="matrix(1, 0, 0, 1, 41.965297, 18.514101)">
      <stop offset="0" style="stop-color: rgb(69.02% 10.196% 10.196%)"/>
      <stop offset="1" style="stop-color: rgb(47.617% 0% 0%)"/>
    </linearGradient>
    <linearGradient gradientUnits="userSpaceOnUse" x1="204.604" y1="218.348" x2="204.604" y2="225.014" id="gradient-1" gradientTransform="matrix(1, 0, 0, 1, -4.81343, 8.022452)">
      <stop offset="0" style="stop-color: rgb(69.02% 10.196% 10.196%)"/>
      <stop offset="1" style="stop-color: rgb(47.617% 0% 0%)"/>
    </linearGradient>
    <linearGradient gradientUnits="userSpaceOnUse" x1="204.604" y1="218.348" x2="204.604" y2="225.014" id="gradient-2" gradientTransform="matrix(1, 0, 0, 1, 36.046196, -2.852014)">
      <stop offset="0" style="stop-color: rgb(69.02% 10.196% 10.196%)"/>
      <stop offset="1" style="stop-color: rgb(47.617% 0% 0%)"/>
    </linearGradient>
    <linearGradient gradientUnits="userSpaceOnUse" x1="204.604" y1="218.348" x2="204.604" y2="225.014" id="gradient-3" gradientTransform="matrix(1, 0, 0, 1, 1.357937, -20.118983)">
      <stop offset="0" style="stop-color: rgb(69.02% 10.196% 10.196%)"/>
      <stop offset="1" style="stop-color: rgb(47.617% 0% 0%)"/>
    </linearGradient>
    <linearGradient gradientUnits="userSpaceOnUse" x1="204.604" y1="218.348" x2="204.604" y2="225.014" id="gradient-4" gradientTransform="matrix(1, 0, 0, 1, 25.549698, -43.076468)">
      <stop offset="0" style="stop-color: rgb(69.02% 10.196% 10.196%)"/>
      <stop offset="1" style="stop-color: rgb(47.617% 0% 0%)"/>
    </linearGradient>
    <linearGradient gradientUnits="userSpaceOnUse" x1="204.604" y1="218.348" x2="204.604" y2="225.014" id="gradient-5" gradientTransform="matrix(1, 0, 0, 1, 14.934944, -6.295119)">
      <stop offset="0" style="stop-color: rgb(69.02% 10.196% 10.196%)"/>
      <stop offset="1" style="stop-color: rgb(47.617% 0% 0%)"/>
    </linearGradient>
    <linearGradient gradientUnits="userSpaceOnUse" x1="253.358" y1="209.091" x2="253.358" y2="215.757" id="gradient-6" gradientTransform="matrix(1, 0, 0, 1, -47.29071, 28.037297)">
      <stop offset="0" style="stop-color: rgb(0% 21.569% 88.627%)"/>
      <stop offset="1" style="stop-color: rgb(0% 11.861% 64.277%)"/>
    </linearGradient>
    <linearGradient gradientUnits="userSpaceOnUse" x1="253.358" y1="209.091" x2="253.358" y2="215.757" id="gradient-7" gradientTransform="matrix(1, 0, 0, 1, -16.292206, -9.627989)">
      <stop offset="0" style="stop-color: rgb(0% 21.569% 88.627%)"/>
      <stop offset="1" style="stop-color: rgb(0% 11.861% 64.277%)"/>
    </linearGradient>
    <linearGradient gradientUnits="userSpaceOnUse" x1="253.358" y1="209.091" x2="253.358" y2="215.757" id="gradient-8" gradientTransform="matrix(1, 0, 0, 1, -37.02737, -21.970437)">
      <stop offset="0" style="stop-color: rgb(0% 21.569% 88.627%)"/>
      <stop offset="1" style="stop-color: rgb(0% 11.861% 64.277%)"/>
    </linearGradient>
  </defs>
  <g transform="matrix(0.7148779630661011, 0, 0, 0.7191610336303711, -108.24022674560547, -93.4969940185547)" style="">
    <title>Tree</title>
    <g style="" transform="matrix(1.030324, 0, 0, 1, -7.692257, 0)">
      <rect x="215.095" y="238.59" width="13.824" height="13.824" style="stroke: rgb(0, 0, 0); fill: rgb(133, 76, 10);"/>
      <path d="M 222.468 187.856 L 253.666 239.77 L 191.27 239.77 L 222.468 187.856 Z" style="stroke: rgb(0, 0, 0); fill: rgb(20, 128, 46);" bx:shape="triangle 191.27 187.856 62.396 51.914 0.5 0 1@fc359b9c"/>
      <path d="M 221.983 172.106 L 245.624 218.658 L 198.342 218.658 L 221.983 172.106 Z" style="stroke: rgb(0, 0, 0); fill: rgb(20, 128, 46);" bx:shape="triangle 198.342 172.106 47.282 46.552 0.5 0 1@c3972894"/>
      <path d="M 222.08 160.42 L 241.264 201.602 L 202.896 201.602 L 222.08 160.42 Z" style="stroke: rgb(0, 0, 0); fill: rgb(20, 128, 46);" bx:shape="triangle 202.896 160.42 38.368 41.182 0.5 0 1@8c72c351"/>
      <path style="fill: none; stroke-linecap: round; stroke: rgba(216, 213, 213, 0.87);" d="M 217.07 173.421 C 216.533 174.496 218.839 177.658 219.539 178.358 C 220.65 179.469 221.144 181.197 222.254 182.307 C 224.075 184.128 227.933 184.53 229.907 186.504 C 231.176 187.774 233.512 189.466 235.585 189.466"/>
      <path style="stroke: rgb(209, 209, 209); fill: none; stroke-linecap: round;" d="M 207.781 190.766 C 209.379 193.225 210.015 195.637 211.808 197.476 C 214.442 200.177 219.375 200.589 221.876 203.155 C 222.632 203.928 224.645 203.413 225.4 204.187 C 226.393 205.205 228.217 206.663 229.427 207.283 C 230.569 207.869 230.947 210.133 231.693 210.897 C 233.597 212.85 238.647 217.608 241.509 217.608"/>
      <path style="stroke: rgb(209, 209, 209); fill: none;" d="M 203.987 219.089 C 205.859 222.833 210.614 223.494 213.368 226.247 C 214.273 227.153 216.412 226.823 217.317 227.729 C 218.648 229.059 222.225 228.439 223.489 229.703 C 224.809 231.023 230.353 228.668 231.635 229.95 C 234.021 232.337 237.642 233.489 240.028 235.875 C 241.55 237.397 244.183 237.809 245.706 239.331 C 245.891 239.516 247.187 239.549 247.187 239.825"/>
      <path style="stroke: rgb(209, 209, 209); fill: none;" d="M 194.853 234.147 C 198.669 236.055 199.194 239.825 205.221 239.825"/>
      <ellipse style="fill: url('#gradient-0'); stroke: rgb(0, 0, 0); stroke-width: 0.1px;" cx="246.57" cy="240.195" rx="3.086" ry="3.333"/>
      <ellipse style="fill: url('#gradient-1'); stroke: rgb(0, 0, 0); stroke-width: 0.1px;" cx="199.791" cy="229.703" rx="3.086" ry="3.333"/>
      <ellipse style="fill: url('#gradient-2'); stroke: rgb(0, 0, 0); stroke-width: 0.1px;" cx="240.65" cy="218.829" rx="3.086" ry="3.333"/>
      <ellipse style="fill: url('#gradient-3'); stroke: rgb(0, 0, 0); stroke-width: 0.1px;" cx="205.962" cy="201.562" rx="3.086" ry="3.333"/>
      <ellipse style="fill: url('#gradient-4'); stroke: rgb(0, 0, 0); stroke-width: 0.1px;" cx="230.154" cy="178.605" rx="3.086" ry="3.333"/>
      <ellipse style="fill: url('#gradient-5'); stroke: rgb(0, 0, 0); stroke-width: 0.1px;" cx="219.539" cy="215.387" rx="3.086" ry="3.333"/>
      <ellipse style="fill: url('#gradient-6'); stroke: rgb(0, 0, 0); stroke-width: 0.1px;" cx="206.067" cy="240.462" rx="3.086" ry="3.333"/>
      <ellipse style="fill: url('#gradient-7'); stroke: rgb(0, 0, 0); stroke-width: 0.1px;" cx="237.065" cy="202.796" rx="3.086" ry="3.333"/>
      <ellipse style="fill: url('#gradient-8'); stroke: rgb(0, 0, 0); stroke-width: 0.1px;" cx="216.33" cy="190.454" rx="3.086" ry="3.333"/>
    </g>
    <path d="M 221.154 146.688 L 223.658 153.892 L 231.283 154.047 L 225.206 158.654 L 227.414 165.954 L 221.154 161.598 L 214.894 165.954 L 217.102 158.654 L 211.025 154.047 L 218.65 153.892 Z" style="stroke: rgb(0, 0, 0); fill: rgb(255, 241, 0); stroke-width: 0.3px;" bx:shape="star 221.154 157.338 10.65 10.65 0.4 5 1@1c040528"/>
  </g>
  <g transform="matrix(0.7148779630661011, 0, 0, 0.7191610336303711, -107.44784545898438, -94.24443817138673)" style="">
    <title>Text</title>
    <text style="fill: rgb(51, 51, 51); font-family: Arial, sans-serif; font-size: 22px; font-weight: 700; text-anchor: middle; white-space: pre;" x="219.039" y="280.789"><title>YEAR</title>YEAR_TEXT</text>
    <text style="fill: rgb(51, 51, 51); font-family: Arial, sans-serif; font-size: 12px; font-style: italic; text-anchor: middle; white-space: pre;" x="219.955" y="295.841"><title>SNOW_DEPTH</title>SNOW_DEPTH_TEXT</text>
  </g>
  <path d="M 42.869 81.518 C 46.044 81.388 52.526 81.029 55.907 81.804 C 58.51 82.399 60.129 84.249 62.001 84.798 C 63.578 85.258 65.436 84.96 66.395 85.224 C 66.994 85.391 67.348 85.512 67.599 85.867 C 67.87 86.249 67.493 87.152 67.882 87.506 C 68.368 87.947 70.226 87.477 70.717 87.934 C 71.124 88.312 71.112 89.224 71.001 89.716 C 70.902 90.152 70.638 90.505 70.221 90.786 C 69.681 91.149 68.828 91.362 67.812 91.498 C 66.448 91.68 64.442 91.756 62.568 91.498 C 60.46 91.208 58.555 90.025 55.766 89.645 C 52.153 89.151 46.252 89.102 42.303 89.359 C 38.935 89.579 34.872 91.037 33.374 90.786 C 32.66 90.665 32.833 90.016 32.241 89.929 C 31.286 89.791 28.548 91.193 27.705 91.07 C 27.249 91.004 27.083 90.725 26.926 90.429 C 26.753 90.101 26.68 89.536 26.784 89.146 C 26.89 88.751 27.054 88.428 27.564 88.076 C 28.445 87.468 31.296 87.165 32.453 86.294 C 33.424 85.562 33.48 84.208 34.366 83.514 C 35.312 82.774 36.702 82.42 38.051 82.088 C 39.515 81.728 40.732 81.606 42.869 81.518 Z M 71.425 74.104 C 71.589 74.308 71.58 74.221 71.709 74.319 C 71.909 74.47 72.381 74.787 72.559 74.961 C 72.674 75.071 72.648 75.115 72.772 75.245 C 72.997 75.484 73.729 75.874 73.977 76.315 C 74.223 76.754 74.359 77.432 74.26 77.882 C 74.168 78.301 73.876 78.704 73.481 78.952 C 73.011 79.248 72.397 79.571 71.497 79.38 C 69.954 79.052 66.334 76.679 64.765 75.459 C 63.637 74.582 63.07 73.594 62.426 72.964 C 61.95 72.497 61.569 72.533 61.222 71.895 C 60.651 70.848 59.782 67.577 59.946 66.478 C 60.044 65.823 60.558 65.511 60.867 65.266 C 61.046 65.125 61.15 65.051 61.35 65.011 C 61.125 64.674 60.911 64.301 60.681 63.889 C 60.007 62.68 59.538 60.294 58.808 59.324 C 58.287 58.631 57.464 58.675 57.08 58.093 C 56.668 57.469 56.362 56.449 56.504 55.629 C 56.658 54.734 57.427 53.567 58.16 52.949 C 58.859 52.36 59.856 51.968 60.753 51.935 C 61.678 51.9 62.83 52.372 63.633 52.804 C 64.362 53.195 64.814 53.495 65.434 54.325 C 66.373 55.585 67.421 59.211 68.386 60.338 C 68.994 61.049 69.812 60.878 70.186 61.425 C 70.577 61.996 70.774 62.96 70.619 63.743 C 70.444 64.624 69.574 65.826 68.962 66.424 C 68.472 66.903 67.986 67.121 67.378 67.293 C 67.347 67.303 67.315 67.311 67.283 67.32 C 68.575 68.908 70.869 73.417 71.425 74.104 Z M 52.931 25.346 C 53.4 25.351 54.127 25.611 54.703 26.131 C 55.487 26.839 56.634 28.606 56.97 29.694 C 57.239 30.566 57 31.412 56.97 32.118 C 56.945 32.713 56.805 33.165 56.829 33.687 C 56.852 34.211 56.857 34.663 57.112 35.256 C 57.457 36.055 58.492 37.429 59.025 38.035 C 59.379 38.438 59.766 38.469 59.946 38.819 C 60.139 39.193 60.201 39.825 60.088 40.245 C 59.979 40.653 59.673 41.065 59.309 41.314 C 58.913 41.584 58.246 41.834 57.75 41.742 C 57.228 41.645 56.522 40.888 56.262 40.672 C 56.135 40.568 56.172 40.622 56.049 40.459 C 55.683 39.971 54.009 37.985 53.569 36.539 C 53.122 35.067 53.335 32.309 53.427 31.691 C 53.459 31.483 53.605 31.58 53.569 31.405 C 53.47 30.936 51.771 29.11 51.443 28.269 C 51.221 27.7 51.188 27.264 51.301 26.844 C 51.411 26.436 51.788 26.028 52.081 25.775 C 52.339 25.552 52.579 25.344 52.931 25.346 Z M 39.076 64.613 C 39.364 65.179 39.526 66.15 39.55 67.198 C 39.868 66.676 40.155 66.173 40.588 65.844 C 41.346 65.272 42.284 64.815 43.18 64.83 C 44.128 64.846 45.58 65.376 46.134 66.062 C 46.645 66.695 46.684 67.63 46.565 68.67 C 46.407 70.056 45.541 72.164 44.693 73.741 C 43.84 75.328 42.646 77.037 41.453 78.16 C 40.39 79.161 38.948 79.994 37.995 80.334 C 37.318 80.577 36.875 80.6 36.267 80.479 C 35.566 80.341 34.502 79.962 34.034 79.392 C 34.016 79.37 33.999 79.346 33.983 79.322 C 33.85 79.471 33.702 79.616 33.53 79.754 C 32.551 80.544 30.364 81.728 29.353 82.073 C 28.726 82.286 28.447 82.321 27.913 82.218 C 27.252 82.089 26.145 81.594 25.681 81.131 C 25.31 80.761 25.212 80.371 25.105 79.827 C 24.967 79.135 24.809 78.448 25.105 77.22 C 25.626 75.053 28.234 69.286 29.425 67.366 C 30.107 66.268 30.36 66.004 31.226 65.41 C 31.343 65.329 31.474 65.246 31.617 65.161 C 31.145 64.356 30.917 62.95 31.154 61.859 C 31.444 60.528 33.197 59.114 33.746 57.803 C 34.225 56.661 33.946 55.555 34.467 54.47 C 35.05 53.254 36.278 51.68 37.276 50.92 C 38.098 50.294 38.986 49.885 39.868 49.906 C 40.785 49.929 42.147 50.477 42.676 51.138 C 43.164 51.747 43.271 52.727 43.109 53.601 C 42.916 54.638 41.716 55.755 41.236 56.934 C 40.753 58.121 40.821 59.399 40.228 60.701 C 39.794 61.654 39.144 62.91 38.426 63.94 C 38.684 64.09 38.91 64.288 39.076 64.613 Z" style="fill: rgb(235, 235, 235); stroke: rgb(147, 147, 147); stroke-width: 0.3px;" transform="matrix(1, 0, 0, 1, 7.105427357601002e-15, 0)">
    <title>MODERATE</title>
  </path>
</svg>
'''

if __name__ == "__main__":

    print(create_svg_grid_test())

    # file_paths = [r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_MODERATE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_TRACE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_NONE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_MODERATE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_TRACE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_NONE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_MODERATE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_TRACE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_NONE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_MODERATE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_TRACE.svg', r'C:\00_GIT\HvitJul\Graphics/svg_parts/SNOW_LEVEL_NONE.svg'] # Replace with your actual file paths
    # create_svg_grid(file_paths,images_per_row=4)