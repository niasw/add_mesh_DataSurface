=== Script Detail ===

This page is to explain how Data Surface addon works.

The key files to this addon are two python scripts: <b>__init__.py</b> and <b>add_mesh_text_data_surface.py</b>.

=== __init__.py ===

In <b>__init__.py</b>, these scripts declare the information of this addon.
<source lang="python">
bl_info = {
  "name": "3D Surfaces from Data Files",
  "author": "Sun Sibai (niasw) <niasw@pku.edu.cn>, Pontiac",
  "version": (1, 0),
  "blender": (2, 71, 0),
  "location": "View3D > Add > Mesh",
  "description": "Create Object using Data Files.",
  "wiki_url": "https://github.com/niasw/add_mesh_DataSurface",
  "category": "Add Mesh"
}
</source>

these scripts define the menu shown in <b>3D View</b> when pressing {{Shortcut|Shift+A}}.
<source lang="python">
class INFO_MT_mesh_data_surface_add(bpy.types.Menu):
  bl_idname = "INFO_MT_mesh_data_surface_add"
  bl_label = "Data Surface"

  def draw(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout.operator("mesh.primitive_text_data_surface",
           text="Text Data Surface")

def menu_func(self, context):
  self.layout.menu("INFO_MT_mesh_data_surface_add", icon="PLUGIN")
</source>

=== add_mesh_text_data_surface.py ===

In <b>add_mesh_text_data_surface.py</b>, this is the main class.
<source lang="python">
class AddTextDataSurface(bpy.types.Operator):
    bl_idname = "mesh.primitive_text_data_surface"
    bl_label = "Add Text Data Surface"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    ...

    def execute(self, context):
        ...
</source>
When adding the mesh object or editing parameters, <b>execute</b> method will be called for each operation.

The input parameters are also defined in this class.
<source lang="python">
class AddTextDataSurface(bpy.types.Operator):
    ...

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

    ...
</source>

When calling the <b>execute</b>, several auxiliary methods will be called in <b>execute</b>.

The 1st aux-method is to acquire matrix data from text files. The <b>Xdata.txt</b> in the previous example (on [http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Data_Surface Data Surface wikipage]) is an instance of these text data files.
<source lang="python">
# Load data from plain text file (in matrix format)
# Return uNum, vNum, dataList
#   filename ... plain text file of data (in matrix format)
#   uNum ... number of vertices in U direction (horizontal in matrix)
#   vNum ... number of vertices in V direction (veritical in matrix)
#   dataList ... list of float/double data parsed from text file
def loadTextData(filename):
    ...
</source>
Coordinates will be loaded in after calling <b>loadTextData</b>

The 2nd aux-method is to make series of faces line by line. (This method is from Blender addon: add extra objects -> 'createFaces' method. Inferred from author declarations in scripts there, it might be written by Pontiac. If I made a mistake here, please tell me.) We have obtained coordinates of vertices. To make vertices, just append the tuple (x,y,z) to the variable <b>verts</b>. To get <b>faces</b>, containing the list of indices of faces, this aux-method is really helpful.
<source lang="python">
# Link two lines of vertices
# Returns the list of the new faces
#   verts1 ... 1st Line.
#   verts2 ... 2nd Line.
#   loop ... Link the final with the start.
#   flip ... Flip the normal side of faces.
def makeFaces(verts1, verts2, loop=False, flip=False):
    ...
</source>

After we get <b>verts</b> and <b>faces</b>, we can call <b>create_mesh_and_object</b> to create the target mesh. <b>edges</b> is not necessary. (This method is from Blender addon: add extra objects -> 'create_mesh_object' method. Inferred from author declarations in scripts there, it might be written by Pontiac. If I made a mistake here, please tell me.)
<source lang="python">
def create_mesh_and_object(context, verts, edges, faces, name):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, edges, faces)
    mesh.update()

    from bpy_extras import object_utils
    return object_utils.object_data_add(context, mesh, operator=None)
</source>

Once we created this mesh, work finished!

=== Thanks ===

"makeFaces" method and "create_mesh_and_object" method are from Blender addon [http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Add_Extra add extra objects]. Thank Pontiac.

If you are still not satisfied, please go to the source scripts.

------
* back to [http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Data_Surface Data Surface]

