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

bl_info = {
  "name": "3D Surfaces from Data Files",
  "author": "Sun Sibai (niasw) <niasw@pku.edu.cn>",
  "version": (1, 0),
  "blender": (2, 71, 0),
  "location": "View3D > Add > Mesh",
  "description": "Create Object using Data Files.",
  "wiki_url": "https://github.com/niasw/add_mesh_DataSurface",
  "category": "Add Mesh"
}

if "bpy" in locals():
  import imp
  imp.reload(add_mesh_text_data_surface)
else:
  from . import add_mesh_text_data_surface

import bpy

class INFO_MT_mesh_data_surface_add(bpy.types.Menu):
# Define the "Data Surface" menu
  bl_idname = "INFO_MT_mesh_data_surface_add"
  bl_label = "Data Surface"

  def draw(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout.operator("mesh.primitive_text_data_surface",
           text="Text Data Surface")

# Register Function

def menu_func(self, context):
  self.layout.menu("INFO_MT_mesh_data_surface_add", icon="PLUGIN")

def register():
  bpy.utils.register_module(__name__)
  bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
  bpy.utils.unregister_module(__name__)
  bpy.types.INFO_MT_mesh_add.remove(menu_func)

# For build-in python usage
if __name__ == "__main__":
  register()
