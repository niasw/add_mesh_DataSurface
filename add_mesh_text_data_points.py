# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#
# Contributed to by
#   Sun Sibai <niasw@pku.edu.cn>
#   Pontiac (for Blender Addon: add_mesh_extra_objects 'create_mesh_object' methods)
#

'''
bl_info = {
  "name": "Text Data Surfaces",
  "author": "Sun Sibai (niasw) <niasw@pku.edu.cn>, Pontiac",
  "version": (1, 1),
  "blender": (2, 71, 0),
  "location": "View3D > Add > Mesh",
  "description": "Create Objects using Text Data Files",
  "warning": "",
  "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Data_Surface/Text_Data_Surface",
  "category": "Add Mesh"
}
'''

import bpy
import addon_utils
import re
from bpy.props import *

# Create a new mesh and object from verts/edges/faces.
#   verts/edges/faces ... Lists of vertices, edges, faces for the new mesh.
#   name ... Name of the new mesh and object.
def create_mesh_and_object(context, verts, edges, faces, name):

    # Create new mesh
    mesh = bpy.data.meshes.new(name)

    # Make a mesh from a list of verts/edges/faces.
    mesh.from_pydata(verts, edges, faces)

    # Update mesh geometry after adding stuff.
    mesh.update()

    from bpy_extras import object_utils
    return object_utils.object_data_add(context, mesh, operator=None)

# Load data from plain text file (in matrix format)
# Return uNum, vNum, dataList
#   filename ... plain text file of data (in matrix format)
#   uNum ... number of vertices in U direction (horizontal in matrix)
#   vNum ... number of vertices in V direction (veritical in matrix)
#   dataList ... list of float/double data parsed from text file
def loadTextData(filename):
  pNum = 0
  dataList = []
  try:
    fileHandler = open(filename,'r')
    fileHandler.seek(0)
    textLine = fileHandler.readline()
    textLine = re.sub('^(e|E)+', '', textLine) # remove confusing labels
    textLine = re.sub('[^(0-9|\.)](e|E)', '', textLine) # remove confusing labels
    textLine = re.sub('(\+|\-)[^(0-9|\.)]', '', textLine) # remove confusing labels
    textDataLine = re.split('[^(0-9|e|E|\+|\-|\.)]+', textLine) # use regular expression to split data
    try:
      while True:
        textDataLine.remove('')
    except:
      pass
    if textDataLine:
      pNum = pNum + len(textDataLine)
      dataList.extend([float(it) for it in textDataLine])
    textLine = fileHandler.readline()
    while textLine:
      textLine = re.sub('^(e|E)+', '', textLine) # remove confusing labels
      textLine = re.sub('[^(0-9|\.)](e|E)', '', textLine) # remove confusing labels
      textLine = re.sub('(\+|\-)[^(0-9|\.)]', '', textLine) # remove confusing labels
      textDataLine = re.split('[^(0-9|e|E|\+|\-|\.)]+', textLine) # use regular expression to split data
      try:
        while True:
          textDataLine.remove('')
      except:
        pass
      if textDataLine:
        pNum = pNum + len(textDataLine)
        dataList.extend([float(it) for it in textDataLine])
      textLine = fileHandler.readline()
    fileHandler.close()
  except FileNotFoundError as e:
    raise e
    return 0, []
  except Exception as e:
    raise Exception("Error loading data file: " + filename + "\n exception: " + str(e))
    return 0, []
  except: # this will never be called
    return 0, []
  return pNum, dataList

# Main Class
#   xFile ... Text File of x Coordinate Data
#   yFile ... Text File of y Coordinate Data
#   zFile ... Text File of z Coordinate Data
class AddTextDataPoints(bpy.types.Operator):
    """Add points from text data files."""
    bl_idname = "mesh.primitive_text_data_points"
    bl_label = "Add Text Data Points"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    xFile = StringProperty(name="Data File of X(index)",
        description="index: index coordinates of nodes; X: x coordinate of nodes. (Vector Text)",
        subtype="FILE_PATH")
    yFile = StringProperty(name="Data File of Y(index)",
        description="index: index coordinates of nodes; Y: y coordinate of nodes. (Vector Text)",
        subtype="FILE_PATH")
    zFile = StringProperty(name="Data File of Z(index)",
        description="index: index coordinates of nodes; Z: z coordinate of nodes. (Vector Text)",
        subtype="FILE_PATH")

    firstCall = True # some scripts should run only once
    newError = False # When configuring browser, 'execute' should be paused

    def execute(self, context):
      if (not self.newError):
        xFile = self.xFile
        yFile = self.yFile
        zFile = self.zFile

        verts = []
        faces = []
        pNum = 0

        if (self.firstCall):
          self.firstCall = False
          successFlag = False
          for it_path in addon_utils.paths():
            if (successFlag):
              break; # successfully loaded, no need to continue

            xFile = it_path+"/add_mesh_DataSurface/Xdata.txt"
            yFile = it_path+"/add_mesh_DataSurface/Ydata.txt"
            zFile = it_path+"/add_mesh_DataSurface/Zdata.txt"
            self.xFile = xFile;
            self.yFile = yFile;
            self.zFile = zFile;
            try:
              pNum, xValue = loadTextData(xFile)
              pNu2, yValue = loadTextData(yFile)
              pNu3, zValue = loadTextData(zFile)
              if (pNum!=pNu2 or pNum!=pNu3):
                raise Exception("Error: point number not match among x,y,z.", "Hint: number of vertices in each x,y,z data should be the same.")
              successFlag = True
            except FileNotFoundError as e:
              successFlag = False
            except:
              import traceback
              self.report({'ERROR'}, "Error combining coordinate data: "
                           + traceback.format_exc(limit=1))
              self.newError = True
              return {'CANCELLED'}
          if (not successFlag):
            errStr = "Fail to find example data files: \nI have searched in following paths:\n"
            for it_path in addon_utils.paths():
              errStr += "  " + it_path+"/add_mesh_DataSurface/Xdata.txt\n"
            self.report({'ERROR'}, errStr)
            self.newError = True
            return {'CANCELLED'}
        else:
          try:
            pNum, xValue = loadTextData(xFile)
            pNu2, yValue = loadTextData(yFile)
            pNu3, zValue = loadTextData(zFile)
            if (pNum!=pNu2 or pNum!=pNu3):
              raise Exception("Error: point number not match among x,y,z.", "Hint: number of vertices in each x,y,z data should be the same.")
          except:
            import traceback
            self.report({'ERROR'}, "Error combining coordinate data: "
                         + traceback.format_exc(limit=1))
            self.newError = True
            return {'CANCELLED'}

        for it in range(pNum):
            verts.append( (xValue[it],yValue[it],zValue[it]) )

        if not verts:
          newError = True
          return {'CANCELLED'}

        the_object = create_mesh_and_object(context, verts, [], faces, "TextDataPoints")

        return {'FINISHED'}
      else:
        self.newError = False
        # self.report({'INFO'}, "Edit Over? Try it again.")
        return {'FINISHED'}
