# Web Map Exporter Script

## Overview
This script is designed to convert a web map to various formats such as PDF, JPG, GIF, PNG, TIFF, EPS, SVG, and SVGZ. It takes parameters for layout, format, DPI, height, width, labels, and more, and creates an output file in the specified format.

## Requirements
- Python 2.7 or higher.
- ArcPy library.
- ArcGIS Desktop, Server, or Portal.
- Appropriate permissions to execute scripts.
- A series of mxd's (map exchange document) for the layout templates.

## Usage
This script is intended to be used within an Esri environment, such as ArcGIS. To execute the script, follow these steps:
1. Create a custom toolbox in ArcGIS.
2. Add the script to the toolbox and define the parameters as described above.
3. Execute the script through the toolbox, either within ArcGIS Desktop or by publishing and executing it through ArcGIS Server or Portal for ArcGIS.

### Integration in ArcGIS
- Open ArcToolbox and right-click to create a new toolbox.
- Right-click on the new toolbox and choose 'Add Script...'.
- Follow the wizard to define script properties and parameters.

Once integrated, you can execute the script by double-clicking it in the toolbox and filling in the required parameters.


## Parameters
- `Web_Map_as_JSON`: The web map definition as a JSON string.
- `Layout_Template`: The layout template name.
- `Format`: Output format (pdf, jpg, gif, png32, png8, tiff, eps, svg, svgz).
- `label`: Additional label information.
- `authorText`: Author text to be added to the output.
- `copyrightText`: Copyright text to be added to the output.
- `titleText`: Title text for the web map.
- `preserveScale`: Preserve the scale of the web map.
- `isScaleBarVisible`: Controls the visibility of the scale bar.
- `scale`: Scale information for the web map.
- `extent`: Extent information for the web map.
- `dpi`: The DPI of the output image (e.g., 300).
- `height`: Height of the output image.
- `width`: Width of the output image.
- `legendLayers`: Legend layers information.

## Features
- Handle root layers and group layers.
- Export to multiple formats including PNG32 and PNG8.
- Option to handle SVGZ format.
- Ability to set up text elements like title, copyright, and author text.
- Control the visibility of scale bar and legend.
- Control the size and resolution of the template. (map only option) 
