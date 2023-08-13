# Web Map Exporter Script

## Overview
This script is designed to convert a web map to various formats such as PDF, JPG, GIF, PNG, TIFF, EPS, SVG, and SVGZ. It takes parameters for layout, format, DPI, height, width, labels, and more, and creates an output file in the specified format.

## Requirements
- Python 2.7 or higher
- ArcPy library

## Usage
You can execute the script from the command line or integrate it into your existing GIS workflow. It takes parameters for the web map as JSON, output format, layout template, and other display options.

## Parameters
- Web_Map_as_JSON: The web map definition as a JSON string.
- Layout_Template: The layout template name.
- Format: Output format (pdf, jpg, gif, png32, png8, tiff, eps, svg, svgz).
- dpi: The DPI of the output image.
- width: Width of the output image.
- height: Height of the output image.
- Additional parameters for labels, copyright, author text, scale, extent, etc

## Parameters
- Handle root layers and group layers.
- Export to multiple formats including PNG32 and PNG8.
- Option to handle SVGZ format.
- Ability to set up text elements like title, copyright, and author text.
- Control the visibility of scale bar and legend.
