=== Script Detail ===

This page is to explain how Z Data Surface addon works.

The key file is the python scripts: <b>add_mesh_z_data_surface.py</b>.
This page only points out the unique informations, others are similar with [http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Data_Surface/Text_Data_Surface Text Data Surface].

=== add_mesh_z_data_surface.py ===

The input parameters are different from Text Data Surface.
<source lang="python">
class AddZDataSurface(bpy.types.Operator):
    ...

    zFile = StringProperty(name="Data File of Z(X,Y)",
        description="Z=z(X,Y). (Table Text)",
        default=addon_utils.paths()[0]+"/add_mesh_DataSurface/csvdata.csv", subtype="FILE_PATH")
    loop = BoolProperty(name="Loop in X Direction",
        description="Loop in X direction or not?",
        default=False)
    flip = BoolProperty(name="Flip Normal Vector",
        description="Flip the normal vector of surfaces or not?",
        default=False)
    tran = BoolProperty(name="Switch X <-> Y vec",
        description="Switch x <-> y, same with transposing matrix",
        default=False)

    ...
</source>
There is only table data in one file. This gives convenience to one have data in a table form.

Since table forms are different from common matrices, the parsing method should be modified.

In <b>execute()</b>, I use
<source lang="python">
    uNum, vNum, zValue, xValue, yValue = loadZData(zFile)
</source>
to acquire all coordinate information needed to create mesh.

In <b>loadZData()</b>, try to read the 1st line as x vector
<source lang="python">
    textLine = fileHandler.readline()
    textDataLine = re.split('[^(0-9|e|E|\+|\-|\.)]+', textLine) # use regular expression to split data
    try:
      while True:
        textDataLine.remove('')
    except:
      pass
    if textDataLine:
      uNum = len(textDataLine)
      xList=[float(it) for it in textDataLine]
</source>
Then loop reading the rest lines as (y element + z element vector). Due to y elements in the beginning of these lines, the length of data list is one more than the 1st line.
<source lang="python">
    textLine = fileHandler.readline()
    while textLine:
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
</source>
The <b>if (uNum!=0)</b> condition ensures that empty lines or text comments will not influence data reading process.

These are how it is different from Text Data Surface module.

=== Thanks ===

Same with Text Data Surface, "makeFaces" method and "create_mesh_and_object" method are from Blender addon [http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Add_Extra add extra objects]. Thank Pontiac.

If you are still not satisfied, please go to the source scripts.

------
* back to [http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Data_Surface Data Surface]

