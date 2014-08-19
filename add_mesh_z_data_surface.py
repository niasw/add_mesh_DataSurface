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
#   Pontiac (for Blender Addon: add_mesh_extra_objects 'create_mesh_object' and 'createFaces' methods)
#

'''
bl_info = {
  "name": "Z Data Surfaces",
  "author": "Sun Sibai (niasw) <niasw@pku.edu.cn>, Pontiac",
  "version": (1, 1),
  "blender": (2, 71, 0),
  "location": "View3D > Add > Mesh",
  "description": "Create Objects using Z Data Files",
  "warning": "",
  "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Data_Surface/Z_Data_Surface",
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
#   xList ... list of float/double data for x vector
#   yList ... list of float/double data for y vector
#   dataList ... list of float/double data for z matrix
def loadZData(filename):
  uNum = 0 # x=x(u)
  vNum = 0 # y=y(v)
  xList = []
  yList = []
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
      uNum = len(textDataLine)
      xList=[float(it) for it in textDataLine]
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
        if (uNum!=0):
          vNum = vNum + 1
          if (uNum!=len(textDataLine) - 1):
            raise Exception("Error: Raw data matrix!",
                            "Hint: Horizontal length of each line should be the same. ("
                            +str(uNum)+"!="+str(len(textDataLine)-1)+")")
          yList.append(float(textDataLine.pop(0)))
          dataList.append([float(it) for it in textDataLine])
        else:
          uNum = len(textDataLine)
          xList=[float(it) for it in textDataLine]
      textLine = fileHandler.readline()
    fileHandler.close()
  except FileNotFoundError as e:
    raise e
    return 0, 0, []
  except Exception as e:
    raise Exception("Error loading data file: " + filename + "\n exception: " + str(e))
    return 0, 0, []
  except: # this will never be called
    return 0, 0, []
  return uNum, vNum, dataList, xList, yList

# Main Class
#   zFile ... Text File of z=f(x,y) Data
class AddZDataSurface(bpy.types.Operator):
    """Add a z=f(x,y) surface from table data files."""
    bl_idname = "mesh.primitive_z_data_surface"
    bl_label = "Add Z(X,Y) Table Surface"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    zFile = StringProperty(name="Data File of Z(X,Y)",
        description="Z=z(X,Y). (Table Text)",
        subtype="FILE_PATH")
    loop = BoolProperty(name="Loop in X Direction",
        description="Loop in X direction or not?",
        default=False)
    flip = BoolProperty(name="Flip Normal Vector",
        description="Flip the normal vector of surfaces or not?",
        default=False)
    tran = BoolProperty(name="Switch X <-> Y vec",
        description="Switch x <-> y, same with transposing matrix",
        default=False)

    firstCall = True # some scripts should run only once

    def execute(self, context):
        zFile = self.zFile
        loop = self.loop
        flip = self.flip
        tran = self.tran

        verts = []
        faces = []
        uNum = 0
        vNum = 0

        if (self.firstCall):
          self.firstCall = False
          successFlag = False
          for it_path in addon_utils.paths():
            if (successFlag):
              break; # successfully loaded, no need to continue

            zFile = it_path+"/add_mesh_DataSurface/csvdata.csv"
            self.zFile = zFile;

            try:
              uNum, vNum, zValue, xValue, yValue = loadZData(zFile)
              successFlag = True
            except FileNotFoundError as e:
              successFlag = False
            except:
              import traceback
              self.report({'ERROR'}, "Error parsing coordinate data: "
                           + traceback.format_exc(limit=1))
              return {'CANCELLED'}
          if (not successFlag):
            errStr = "Fail to find example data files: \nI have searched in following paths:\n"
            for it_path in addon_utils.paths():
              errStr += "  \t" + it_path+"/add_mesh_DataSurface/csvdata.csv\n"
            self.report({'ERROR'}, errStr)
            return {'CANCELLED'}
        else:
          try:
            uNum, vNum, zValue, xValue, yValue = loadZData(zFile)
            successFlag = True
          except FileNotFoundError as e:
            successFlag = False
          except:
            import traceback
            self.report({'ERROR'}, "Error parsing coordinate data: "
                         + traceback.format_exc(limit=1))
            return {'CANCELLED'}

        itVertIdsPre = []
        if tran:
          for itV in range(vNum):
            itVertIdsCur = []
            for itU in range(uNum):
              itVertIdsCur.append(len(verts))
              verts.append( (yValue[itV],xValue[itU],zValue[itV][itU]) )
            if len(itVertIdsPre)>0:
              faces.extend(makeFaces(itVertIdsPre,itVertIdsCur,loop,flip))
            itVertIdsPre = itVertIdsCur
        else:
          for itU in range(uNum):
            itVertIdsCur = []
            for itV in range(vNum):
              itVertIdsCur.append(len(verts))
              verts.append( (xValue[itU],yValue[itV],zValue[itV][itU]) )
            if len(itVertIdsPre)>0:
              faces.extend(makeFaces(itVertIdsPre,itVertIdsCur,loop,flip))
            itVertIdsPre = itVertIdsCur

        if not verts:
          return {'CANCELLED'}

        the_object = create_mesh_and_object(context, verts, [], faces, "ZDataSurface")

        return {'FINISHED'}

