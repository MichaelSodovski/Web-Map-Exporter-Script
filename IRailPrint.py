
# ///////////////////////////////////////////////////////////////////////////
# // Copyright © 2023. All Rights Reserved to Mishka.                      
# ///////////////////////////////////////////////////////////////////////////

import sys
import arcpy
import os
import uuid
import json
import traceback
import gzip
import shutil

# Esri start of added variables
g_ESRI_variable_1 = u'\\\\michaelwin2012'
g_ESRI_variable_2 = u'\\\\michaelwin2012\\c$\\Templates'
# Esri end of added variables

# The template location in the server data store
templatePath = os.path.join(g_ESRI_variable_1, '\c$\Templates')

Web_Map_as_JSON = arcpy.GetParameterAsText(0)

dpi = arcpy.GetParameterAsText(11)
arcpy.AddMessage("dpi: " + str(dpi))

height = arcpy.GetParameterAsText(12)
arcpy.AddMessage("height: " + str(height))

width = arcpy.GetParameterAsText(13)
arcpy.AddMessage("width: " + str(width))

Format = arcpy.GetParameterAsText(1).lower()
arcpy.AddMessage("Format: " + str(Format))

label = arcpy.GetParameterAsText(5)
arcpy.AddMessage("label: " + str(label))

Layout_Template = arcpy.GetParameterAsText(2)
arcpy.AddMessage("Layout_Template: " + str(Layout_Template))

authorText = arcpy.GetParameterAsText(7)
arcpy.AddMessage("authorText: " + str(authorText))

copyrightText = arcpy.GetParameterAsText(8)
arcpy.AddMessage("copyrightText: " + str(copyrightText))

legendLayers = arcpy.GetParameterAsText(9)
arcpy.AddMessage("legendLayers: " + str(legendLayers))

titleText = arcpy.GetParameterAsText(6)
arcpy.AddMessage("titleText: " + str(titleText))

preserveScale = arcpy.GetParameterAsText(4)
arcpy.AddMessage("preserveScale: " + str(preserveScale))

isScaleBarVisible = arcpy.GetParameterAsText(14)
arcpy.AddMessage("isScaleBarVisible: " + str(isScaleBarVisible))

printFlag = arcpy.GetParameterAsText(10)
arcpy.AddMessage("printFlag: " + str(printFlag))

scale = arcpy.GetParameterAsText(15)
arcpy.AddMessage("scale: " + str(scale))

extent = arcpy.GetParameterAsText(16)
arcpy.AddMessage("extent: " + str(extent))


def handleRootLayers():
    for df in arcpy.mapping.ListDataFrames(mxd):
        for lyr in arcpy.mapping.ListLayers(mxd, "*", df):
            if lyr.isGroupLayer:
                if not any(sub_lyr.visible for sub_lyr in lyr):
                    # If all sub-layers are off, turn off the group layer.
                    lyr.visible = False
            elif not lyr.isGroupLayer and not lyr.visible:
                # It's a root layer and it's off.
                lyr.visible = False


def handleSVGZformat(Output_File_Name):
    # Open the source file.
    f_in = open(Output_File_Name, 'rb')
    # Open the destination file.
    f_out = gzip.open(Output_File_Name + 'z', 'wb')
    # Copy the source file content to destination file.
    shutil.copyfileobj(f_in, f_out)
    # Close both files.
    f_in.close()
    f_out.close()
    # Delete the source file.
    os.remove(Output_File_Name)
    # Update the output file name to be the SVGZ file.
    Output_File_Name += 'z'
    return Output_File_Name


def EXPORT_TO_PNG32_MAP_ONLY(mxd, Output_File_Name, df, resolution=None, df_export_width=None, df_export_height=None):
    arcpy.mapping.ExportToPNG(mxd, Output_File_Name, df, resolution, df_export_width, df_export_height, 
                              world_file=False, color_mode='24-BIT_TRUE_COLOR', background_color='255,255,255', transparent_color='NONE', interlaced=False)

def EXPORT_TO_PNG8_MAP_ONLY(mxd, Output_File_Name, df, resolution, df_export_width, df_export_height):
    arcpy.mapping.ExportToPNG(mxd, Output_File_Name, df, resolution, df_export_width, df_export_height, 
                              world_file=False, color_mode='8-BIT_PALETTE', background_color='255,255,255', transparent_color='NONE', interlaced=False)

def EXPORT_TO_PNG32(mxd, Output_File_Name):
    arcpy.mapping.ExportToPNG(mxd, Output_File_Name, world_file=False, color_mode='24-BIT_TRUE_COLOR', background_color='255,255,255', transparent_color='NONE', interlaced=False)

def EXPORT_TO_PNG8(mxd, Output_File_Name):
    arcpy.mapping.ExportToPNG(mxd, Output_File_Name, world_file=False, color_mode='8-BIT_PALETTE', background_color='255,255,255', transparent_color='NONE', interlaced=False)


def scaleBarHandler(mapsurround_elements): 
    elementNames = ["scaleBar", "scaleBarMi", "scaleElement"]
    filtered_elements = [e for e in mapsurround_elements if e.name in elementNames]
    for elm in filtered_elements:
        elm.elementPositionX = 10000
        elm.elementPositionY = 10000

def legentHandler(legend_elements):
    legend_elements[0].elementPositionX = 10000
    legend_elements[0].elementPositionY = 10000

def textElementsHandler():
    text_elements = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
    text_dict = {"author": authorText, "copyright": copyrightText, "title": titleText}
    for elm in text_elements:
        if elm.name in text_dict:
            elm.text = text_dict[elm.name] if text_dict[elm.name].strip() != "" else " "


# layoutOptions:
JsonMapToObject = json.loads(Web_Map_as_JSON)
layoutOptions = JsonMapToObject["layoutOptions"]
titleText = layoutOptions.get("titleText")
arcpy.AddMessage(u"titleText: " + unicode(titleText))
copyrightText = layoutOptions.get("copyrightText")
arcpy.AddMessage(u"copyrightText: " + unicode(copyrightText))
authorText = layoutOptions.get("authorText")
arcpy.AddMessage(u"authorText: " + unicode(authorText))

# exportOptions:
exportOptions = JsonMapToObject["exportOptions"]
dpi = exportOptions.get("dpi")
arcpy.AddMessage(u"dpi: " + str(dpi))
outputSize = exportOptions.get("outputSize")
width, height = map(int, outputSize)
arcpy.AddMessage(u"width: " + str(width))
arcpy.AddMessage(u"height: " + str(height))


if Layout_Template == "MAP_ONLY":
    # The template location in the server data store.
    templateMxd = os.path.join(g_ESRI_variable_2, "MAP_ONLY.mxd")
    # Set the workspace.
    arcpy.env.workspace = arcpy.env.scratchFolder
    # Convert the WebMap to a map document.
    arcpy.AddMessage("converting webmap to map document object.")
    result = arcpy.mapping.ConvertWebMapToMapDocument(Web_Map_as_JSON, templateMxd)
    mxd = result.mapDocument
    # Reference the data frame that contains the webmap.
    df = arcpy.mapping.ListDataFrames(mxd, 'Webmap')[0]

    format_suffix_mapping = {
        'pdf': 'pdf',
        'jpg': 'jpg',
        'gif': 'gif',
        'png32': 'png',
        'png8': 'png',
        'tiff': 'tif',
        'eps': 'eps',
        'svg': 'svg',
        'svgz': 'svg'
    }

    # Use the uuid module to generate a GUID as part of the output name,
    # This will ensure a unique output name.
    outputName = 'WebMap_{}.{}'.format(str(uuid.uuid1()), format_suffix_mapping[Format])
    Output_File_Name = os.path.join(arcpy.env.workspace, outputName)

    export_format_function_mapping = {
        'pdf': arcpy.mapping.ExportToPDF,
        'jpg': arcpy.mapping.ExportToJPEG,
        'gif': arcpy.mapping.ExportToGIF,
        'png32': EXPORT_TO_PNG32_MAP_ONLY,
        'png8': EXPORT_TO_PNG8_MAP_ONLY, 
        'tiff': arcpy.mapping.ExportToTIFF,
        'eps': arcpy.mapping.ExportToEPS,
        'svg': arcpy.mapping.ExportToSVG,
        'svgz': arcpy.mapping.ExportToSVG
    }

    # RootLayer\ GroupLayer fix, otherwise the script fails with "java.lang.Exception: Could not service request error.
    handleRootLayers()

    # Export the WebMap according to the choosen format:
    try:
        export_function = export_format_function_mapping[Format]
        export_function(mxd, Output_File_Name, df, resolution=int(dpi), df_export_width=int(width), df_export_height=int(height))
        arcpy.SetParameterAsText(3, Output_File_Name)
    except Exception as Ex:
        arcpy.AddError("An error of type {} occurred. Arguments:\n{}".format(type(Ex).__name__, str(Ex.args)))
        arcpy.AddError("Here is the full traceback: {}".format(traceback.format_exc()))
        if hasattr(Ex, '__context__') and Ex.__context__ is not None:
            arcpy.AddError("The previous exception was: {}".format(str(Ex.__context__)))
            if hasattr(Ex.__context__, '__traceback__'):
                exc_type = type(Ex.__context__)
                exc_value = Ex.__context__
                exc_traceback = Ex.__context__.__traceback__
                traceback_string = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                message = "Here is the traceback for the previous exception: {}".format(traceback_string)
                arcpy.AddError(message)

    # Clean up - delete the map document reference.
    filePath = mxd.filePath
    del mxd, result
    arcpy.AddMessage("Removing file path...")
    os.remove(filePath)
else:
    cleaned_layout_template = Layout_Template.strip("'\"")
    # Get the requested layout template pagx file.
    templateMxd = os.path.join(g_ESRI_variable_2, cleaned_layout_template + '.mxd')
    # Convert the WebMap to a map document.
    result = arcpy.mapping.ConvertWebMapToMapDocument(Web_Map_as_JSON, templateMxd)
    mxd = result.mapDocument
    # Reference the map that contains the webmap.
    df = arcpy.mapping.ListDataFrames(mxd, 'Webmap')[0]
    # handle scale bar visibility:
    if str(isScaleBarVisible) == 'false':
        mapsurround_elements = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT")
        scaleBarHandler(mapsurround_elements)
    # handle legend visibility:
    if str(legendLayers) != "null":
       legend_elements = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "*Legend*") # returns a list of elements, even if there is only one match. 
       legentHandler(legend_elements)
    # handle text elements:
    textElementsHandler()
    # handle spatial reference:
    df.spatialReference = arcpy.SpatialReference(102100)
    # configure workspace: 
    arcpy.env.workspace = arcpy.env.scratchFolder

    format_suffix_mapping = {
        'pdf': 'pdf',
        'jpg': 'jpg',
        'gif': 'gif',
        'png32': 'png',
        'png8': 'png',
        'tiff': 'tif',
        'eps': 'eps',
        'svg': 'svg',
        'svgz': 'svg'
    }

    # Use the uuid module to generate a GUID as part of the output name,
    # This will ensure a unique output name.
    arcpy.AddMessage("start setting outputname..")
    outputName = 'WebMap_{}.{}'.format(str(uuid.uuid1()), format_suffix_mapping[Format])
    Output_File_Name = os.path.join(arcpy.env.workspace, outputName)
    arcpy.AddMessage("end setting outputname..")

    export_format_function_mapping = {
        'pdf': arcpy.mapping.ExportToPDF,
        'jpg': arcpy.mapping.ExportToJPEG,
        'gif': arcpy.mapping.ExportToGIF,
        'png32': EXPORT_TO_PNG32,
        'png8': EXPORT_TO_PNG8, 
        'tiff': arcpy.mapping.ExportToTIFF,
        'eps': arcpy.mapping.ExportToEPS,
        'svg': arcpy.mapping.ExportToSVG,
        'svgz': arcpy.mapping.ExportToSVG
    }

    # RootLayer\ GroupLayer bug fix, otherwise the script fails with "java.lang.Exception: Could not service request error."
    handleRootLayers()

    # Export the WebMap according to the chosen format:
    try:
        export_function = export_format_function_mapping[Format]
        export_function(mxd, Output_File_Name)
        # If the format is 'svgz', compress the SVG file to generate SVGZ file. 
        if Format == 'svgz':
           Output_File_Name = handleSVGZformat(Output_File_Name)

        # Set the output parameter to be the output file of the server job.
        arcpy.SetParameterAsText(3, Output_File_Name)

    except Exception as Ex:
        arcpy.AddError("An error of type {} occurred. Arguments:\n{}".format(type(Ex).__name__, str(Ex.args)))
        arcpy.AddError("Here is the full traceback: {}".format(traceback.format_exc()))
        if hasattr(Ex, '__context__') and Ex.__context__ is not None:
            arcpy.AddError("The previous exception was: {}".format(str(Ex.__context__)))
            if hasattr(Ex.__context__, '__traceback__'):
                exc_type = type(Ex.__context__)
                exc_value = Ex.__context__
                exc_traceback = Ex.__context__.__traceback__
                traceback_string = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                message = "Here is the traceback for the previous exception: {}".format(traceback_string)
                arcpy.AddError(message)

    # Clean up - delete the map document reference
    filePath = mxd.filePath
    del mxd, result
    os.remove(filePath)