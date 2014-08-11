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
#
# Referrence
#   Blender Addon: add_mesh_extra_objects (thank them for 'create_mesh_and_object' and 'makeFace' methods)
#

'''
bl_info = {
  "name": "Text Data Surfaces",
  "author": "Sun Sibai (niasw) <niasw@pku.edu.cn>",
  "version": (1, 0),
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


# Link two lines of vertices
# Returns the list of the new faces
#   verts1 ... 1st Line.
#   verts2 ... 2nd Line.
#   loop ... Link the final with the start.
#   flip ... Flip the normal side of faces.
def makeFaces(verts1, verts2, loop=False, flip=False):
    faces = []

    if not verts1 or not verts2:
        return None

    if len(verts1) < 2 and len(verts2) < 2:
        return None

    # use single vertice in 1st Line for Fan Shape
    fanShape = False
    if (len(verts1) != len(verts2)):
      if (len(verts1)==1):
        fanShape = True
      else:
        return None

    # number of vertices in a line
    vnum = len(verts2)

    # Link the final and the start
    if loop:
        if flip:
          extface = [
            verts1[0],
            verts2[0],
            verts2[vnum-1]
          ]
          if not fanShape:
            extface.append(verts1[vnum-1])
          faces.append(extface)
        else:
          extface = [
            verts2[0],
            verts1[0]
          ]
          if not fanShape:
            extface.append(verts1[vnum-1])
            extface.append(verts2[vnum-1])
          faces.append(extface)

    # Link the rest
    for it in range(vnum-1):
        if flip:
            if fanShape:
                extface = [verts2[it], verts1[0], verts2[it+1]]
            else:
                extface = [verts2[it], verts1[it], verts1[it+1], verts2[it+1]]
            faces.append(extface)
        else:
            if fanShape:
                extface = [verts1[0], verts2[it], verts2[it+1]]
            else:
                extface = [verts1[it], verts2[it], verts2[it+1], verts1[it+1]]
            faces.append(extface)

    return faces

# Load data from plain text file (in matrix format)
# Return uNum, vNum, dataList
#   filename ... plain text file of data (in matrix format)
#   uNum ... number of vertices in U direction (horizontal in matrix)
#   vNum ... number of vertices in V direction (veritical in matrix)
#   dataList ... list of float/double data parsed from text file
def loadTextData(filename):
  uNum = 0
  vNum = 0
  dataList = []
  try:
    fileHandler = open(filename,'r')
    fileHandler.seek(0)
    textLine = fileHandler.readline()
    textDataLine = re.split('[^(\w|\+|\-|\.)]+', textLine) # use regular expression to split data
    try:
      while True:
        textDataLine.remove('')
    except:
      pass
    if textDataLine:
      vNum = vNum + 1
      uNum = len(textDataLine)
      dataList.append([float(it) for it in textDataLine])
    while textLine:
      textDataLine = re.split('[^(\w|\+|\-|\.)]+', textLine) # use regular expression to split data
      try:
        while True:
          textDataLine.remove('')
      except:
        pass
      if textDataLine:
        vNum = vNum + 1
        if (uNum!=len(textDataLine)):
          raise Exception("Error: Raw data matrix!",
                          "Hint: Horizontal length of each line should be the same. ("
                          +str(uNum)+"!="+str(len(textDataLine))+")")
        dataList.append([float(it) for it in textDataLine])
      textLine = fileHandler.readline()
    fileHandler.close()
  except:
    import traceback
    self.report({'ERROR'}, "Error loading data file: "
                + filename + " traceback: " + traceback.format_exc(limit=1))
    return 0, 0, []
  return uNum, vNum, dataList

# Main Class
#   xFile ... Text File of x Coordinate Data
#   yFile ... Text File of y Coordinate Data
#   zFile ... Text File of z Coordinate Data
class AddTextDataSurface(bpy.types.Operator):
    """Add a surface from text data files."""
    bl_idname = "mesh.primitive_text_data_surface"
    bl_label = "Add Text Data Surface"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    xFile = StringProperty(name="Data File of X(U,V)",
        description="U,V: index coordinates of nodes; X: x coordinate of nodes. (Matrix Text)",
        default=addon_utils.paths()[0]+"/add_mesh_DataSurface/Xdata.txt", subtype="FILE_PATH")
    yFile = StringProperty(name="Data File of Y(U,V)",
        description="U,V: index coordinates of nodes; Y: y coordinate of nodes. (Matrix Text)",
        default=addon_utils.paths()[0]+"/add_mesh_DataSurface/Ydata.txt", subtype="FILE_PATH")
    zFile = StringProperty(name="Data File of Z(U,V)",
        description="U,V: index coordinates of nodes; Z: z coordinate of nodes. (Matrix Text)",
        default=addon_utils.paths()[0]+"/add_mesh_DataSurface/Zdata.txt", subtype="FILE_PATH")
    loop = BoolProperty(name="Loop in U Direction",
        description="Loop in U direction or not?",
        default=False)
    flip = BoolProperty(name="Flip Normal Vector",
        description="Flip the normal vector of surfaces or not?",
        default=False)

    def execute(self, context):
        xFile = self.xFile
        yFile = self.yFile
        zFile = self.zFile
        loop = self.loop
        flip = self.flip

        verts = []
        faces = []
        uNum = 0
        vNum = 0

        try:
          uNum, vNum, xValue = loadTextData(xFile)
          uNu2, vNu2, yValue = loadTextData(yFile)
          if (uNum!=uNu2):
            raise Exception("Error: U number not match between x and y.", "Hint: number of vertices in each x,y,z data should be the same.")
          if (vNum!=vNu2):
            raise Exception("Error: V number not match between x and y.", "Hint: number of vertices in each x,y,z data should be the same.")
          uNu3, vNu3, zValue = loadTextData(zFile)
          if (uNum!=uNu3):
            raise Exception("Error: U number not match between x and z.", "Hint: number of vertices in each x,y,z data should be the same.")
          if (vNum!=vNu3):
            raise Exception("Error: V number not match between x and z.", "Hint: number of vertices in each x,y,z data should be the same.")
        except:
          import traceback
          self.report({'ERROR'}, "Error combining coordinate data: "
                       + traceback.format_exc(limit=1))
          return {'CANCELLED'}

        itVertIdsPre = []
        for itU in range(uNum):
          itVertIdsCur = []
          for itV in range(vNum):
            itVertIdsCur.append(len(verts))
            verts.append( (xValue[itV][itU],yValue[itV][itU],zValue[itV][itU]) )
          if len(itVertIdsPre)>0:
            faces.extend(makeFaces(itVertIdsPre,itVertIdsCur,loop,flip))
          itVertIdsPre = itVertIdsCur

        if not verts:
          return {'CANCELLED'}

        the_object = create_mesh_and_object(context, verts, [], faces, "TextDataSurface")

        return {'FINISHED'}

