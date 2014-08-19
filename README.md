#DataSurface

--- Create 3D Surfaces from Data Files
=====

DataSurface is a Blender Addon to create Object using Data Files.

wiki <http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Data_Surface>

Copyleft (*) 2014 Sun Sibai (niasw) <niasw@pku.edu.cn>, Pontiac

("create_mesh_and_object" and "makeFaces" methods are from Blender addon: add extra objects -> 'create_mesh_object' method. Inferred from author declarations in scripts there, it might be from Pontiac. If I made a mistake here, please tell me.)

>This program is free software; you can redistribute it and/or
>modify it under the terms of the GNU General Public License
>as published by the Free Software Foundation; either version 2
>of the License, or (at your option) any later version.

## Introduction

In engineering and science, numerical data sometimes are more common than analytical expressions. Analytical expressions are accurate and easy to accept, but for numerical algorithms (such as self-adapting optimizing) and real experiments (such as measurements with instruments), numerical data are more suitable and more convenient.


If you want to transfer data from numerical algorithms or real experiments into Blender to visualize them, this addon may be your proper choice. In the example I will show below, I turned text data of x,y and z coordinates into a mesh surface.


If you are seeking for addons for analytical expressions, please go to the addon [3D Function Surface](http://wiki.blender.org/index.php/Extensions:2.5/Py/Scripts/Add_Mesh/Add_3d_Function_Surface).


## Installation

To install this addon, please copy all the scripts and data files to the addon path.
* Download the source file from [here](https://github.com/niasw/add_mesh_DataSurface/archive/master.zip) and extract to a folder `add_mesh_DataSurface`
* or use `git clone https://github.com/niasw/add_mesh_DataSurface`.

Then copy directory `add_mesh_DataSurface` to Blender addon path. If you don't know where is the addon path, please open your Blender, and run scripts below in the Python Console:

    import addon_utils
    print(addon_utils.paths())

To enable this addon, please open your Blender.
* Click `Files` > `User Preferences ...` > `Addons` > `Add Mesh`.
* Find ![File:niasw_add_mesh_DataSurface07.png‎](http://wiki.blender.org/uploads/0/0f/Niasw_add_mesh_DataSurface07.png) <html><br/></html> and click the right checkbox

## Instructions
There are two modules in this addon:

* `Text Data Surface` can create all mesh surface in 3D space. But it needs 3 matrices data:

    x=x(u,v)
    y=y(u,v)
    z=z(u,v)

where x,y,z are coordinates in space and u,v are column and row indices.

* `Z Data Surface` can create a subset mesh surface of above. It is convenient for only 1 table data needed:

    z=f(x,y)

where x,y data are in form of vector and z data are in form of matrix.

To show how to use this addon, I will give examples.

### example for Text Data Surface
* In the `3D View` block, press `Shift+A` > `Mesh` > `Data Surface` > `Text Data Surface`.
<html><br/></html> Then a twisted ribbon-like mesh shows.

![File:niasw_add_mesh_DataSurface01.png|340px|](http://wiki.blender.org/uploads/thumb/e/ef/Niasw_add_mesh_DataSurface01.png/340px-Niasw_add_mesh_DataSurface01.png) ![File:niasw_add_mesh_DataSurface02.png‎|340px|](http://wiki.blender.org/uploads/thumb/9/9a/Niasw_add_mesh_DataSurface02.png/340px-Niasw_add_mesh_DataSurface02.png)


The coordinates of vertices are from data files `Xdata.txt`, `Ydata.txt` and `Zdata.txt`.

These data can be generated from Octave/Matlab script `example.m`.

To change the data files, clicking the browsing buttons.

![File:niasw_add_mesh_DataSurface0A.png](http://wiki.blender.org/uploads/6/63/Niasw_add_mesh_DataSurface0A.png)


As for the `loop` and `flip` checkbox, try them to know what they represent.
* After clicking `loop`, you should see the figure closed in each Z slice. Yes, the ribbon becomes a tube.
* After clicking `flip`, you should see the light effect changed a little. Yes, the normal direction flipped.

<table>
 <tr>
  <th><img alt="File:niasw_add_mesh_DataSurface03_1.png‎" src="http://wiki.blender.org/uploads/a/a9/Niasw_add_mesh_DataSurface03_1.png"/></th>
  <th><img alt="File:niasw_add_mesh_DataSurface04_1.png‎" src="http://wiki.blender.org/uploads/7/72/Niasw_add_mesh_DataSurface04_1.png"/></th>
  <th><img alt="File:niasw_add_mesh_DataSurface05_1.png‎" src="http://wiki.blender.org/uploads/e/e7/Niasw_add_mesh_DataSurface05_1.png"/></th>
 </tr><tr>
  <td><img alt="File:niasw_add_mesh_DataSurface03_2.png‎|142px|" src="http://wiki.blender.org/uploads/thumb/e/e0/Niasw_add_mesh_DataSurface03_2.png/142px-Niasw_add_mesh_DataSurface03_2.png"/></td>
  <td><img alt="File:niasw_add_mesh_DataSurface04_2.png‎|142px|" src="http://wiki.blender.org/uploads/thumb/c/c3/Niasw_add_mesh_DataSurface04_2.png/142px-Niasw_add_mesh_DataSurface04_2.png"/></td>
  <td><img alt="File:niasw_add_mesh_DataSurface05_2.png‎|142px|" src="http://wiki.blender.org/uploads/thumb/f/f2/Niasw_add_mesh_DataSurface05_2.png/142px-Niasw_add_mesh_DataSurface05_2.png"/></td>
 </tr>
</table>

### example for Z Data Surface
* In the `3D View` block, press `Shift+A` > `Mesh` > `Data Surface` > `Z(X,Y) Table Surface`.
<html><br/></html> Then a floating ribbon-like mesh shows.

![File:niasw_add_mesh_DataSurface0B.png|340px|](http://wiki.blender.org/uploads/thumb/d/da/Niasw_add_mesh_DataSurface0B.png/340px-Niasw_add_mesh_DataSurface0B.png) ![File:niasw_add_mesh_DataSurface0C.png‎|340px|](http://wiki.blender.org/uploads/thumb/7/7a/Niasw_add_mesh_DataSurface0C.png/340px-Niasw_add_mesh_DataSurface0C.png)


The coordinates of vertices are from table data file `csvdata.csv`.

To change the data files, clicking the browsing button.

Plain text table is also OK.

![File:niasw_add_mesh_DataSurface12.png](http://wiki.blender.org/uploads/3/37/Niasw_add_mesh_DataSurface12.png)

The .csv file can be exported from spreadsheet programs such as Excel and LibreOffice Calc.

The structure of the table in .csv file is shown below:

![File:niasw_add_mesh_DataSurface13.png|680px](http://wiki.blender.org/uploads/thumb/d/d6/Niasw_add_mesh_DataSurface13.png/680px-Niasw_add_mesh_DataSurface13.png)

There are 3 boolean options in Z Data Surface. `loop` and `flip` are like those in Text Data Surface.

<table>
 <tr>
  <th><img alt="File:niasw_add_mesh_DataSurface0D_1.png‎" src="http://wiki.blender.org/uploads/1/1c/Niasw_add_mesh_DataSurface0D_1.png"/></th>
  <th><img alt="File:niasw_add_mesh_DataSurface0E_1.png‎" src="http://wiki.blender.org/uploads/4/4b/Niasw_add_mesh_DataSurface0E_1.png"/></th>
  <th><img alt="File:niasw_add_mesh_DataSurface0F_1.png‎" src="http://wiki.blender.org/uploads/9/92/Niasw_add_mesh_DataSurface0F_1.png"/></th>
 </tr><tr>
  <td><img alt="File:niasw_add_mesh_DataSurface0D_2.png‎|140px|" src="http://wiki.blender.org/uploads/thumb/8/87/Niasw_add_mesh_DataSurface0D_2.png/140px-Niasw_add_mesh_DataSurface0D_2.png"/></td>
  <td><img alt="File:niasw_add_mesh_DataSurface0E_2.png‎|140px|" src="http://wiki.blender.org/uploads/thumb/9/90/Niasw_add_mesh_DataSurface0E_2.png/140px-Niasw_add_mesh_DataSurface0E_2.png"/></td>
  <td><img alt="File:niasw_add_mesh_DataSurface0F_2.png‎|140px|" src="http://wiki.blender.org/uploads/thumb/8/8f/Niasw_add_mesh_DataSurface0F_2.png/140px-Niasw_add_mesh_DataSurface0F_2.png"/></td>
 </tr>
</table>

The `tran` option is to switch x axis with y axis. It is the same with transposing the whole data table. By combining `tran` function and `loop` function, we can close the surface mesh either in x direction or y direction.

<table>
 <tr>
  <th><img alt="File:niasw_add_mesh_DataSurface10_1.png‎" src="http://wiki.blender.org/uploads/b/b4/Niasw_add_mesh_DataSurface10_1.png"/></th>
  <th><img alt="File:niasw_add_mesh_DataSurface11_1.png‎" src="http://wiki.blender.org/uploads/6/64/Niasw_add_mesh_DataSurface11_1.png"/></th>
 </tr><tr>
  <td><img alt="File:niasw_add_mesh_DataSurface10_2.png‎|140px|" src="http://wiki.blender.org/uploads/thumb/e/e3/Niasw_add_mesh_DataSurface10_2.png/140px-Niasw_add_mesh_DataSurface10_2.png"/></td>
  <td><img alt="File:niasw_add_mesh_DataSurface11_2.png‎|140px|" src="http://wiki.blender.org/uploads/thumb/4/43/Niasw_add_mesh_DataSurface11_2.png/140px-Niasw_add_mesh_DataSurface11_2.png"/></td>
 </tr><tr>
  <td><img alt="File:niasw_add_mesh_DataSurface10_3.png‎|140px|" src="http://wiki.blender.org/uploads/thumb/8/86/Niasw_add_mesh_DataSurface10_3.png/140px-Niasw_add_mesh_DataSurface10_3.png"/></td>
  <td><img alt="File:niasw_add_mesh_DataSurface11_3.png‎|140px|" src="http://wiki.blender.org/uploads/thumb/8/8b/Niasw_add_mesh_DataSurface11_3.png/140px-Niasw_add_mesh_DataSurface11_3.png"/></td>
 </tr>
</table>

## Notes
If you have further requirements, you can fork the source codes and develop your own one. To know how this addon works, please go to page [Text Data Surface](http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Data_Surface/Text_Data_Surface) and [Z Data Surface](http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Data_Surface/Z_Data_Surface).

## Compatibility
This addon has been tested on Ubuntu 12.04, Blender 2.71a, Python 3.2 (bundled), 32-bit.

It may also work with Blender versions &lt; 2.71, but not tested yet.

## Troubleshooting
* "Add-on does not appear on the list."

Check if you have installed this addon. Make sure the ".py" files are in the addon path properly. Make sure you have enabled this addon in `User Preferences`.

* "Error combining coordinate data: Traceback (most recent call last):"
* " ... "
* "FileNotFoundError: [Errno 2] No such file or directory: '.../add_mesh_Surface/Xdata.txt' "

or

* "Fail to find example data files:"
* "I have searched in following paths:"
* "  .../add_mesh_DataSurface/Xdata.txt"

These messages mean Blender did not find the data files. When you downloaded it as a zip file, did you extract the folder as `add_mesh_DataSurface` instead of the default `add_mesh_DataSurface-master`? If not, please rename this folder under addon path as `add_mesh_DataSurface`.

* "Browser Button fails to work ... "

Reset it: Delete the current object and re-add it please.

## Support
To raise a bug report, you may issue it on [here(github-issues)](https://github.com/niasw/add_mesh_DataSurface/issues), or [here(developer.blender.org-task)](https://developer.blender.org/T41352).

To contact with me, please write an email to <niasw@pku.edu.cn>.

## Thanks
"create_mesh_and_object" and "makeFaces" methods in `add_mesh_text_data_surface.py` and `add_mesh_z_data_surface.py` were from Blender addon [add_mesh_extra_objects](http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Add_Extra). Thank Pontiac.

Thank Noel Stoutenburg for suggestions about .csv files and Z Data Surface.

Thank @squarednob for issue reporting and testing.

And thank you.

Best regards,

Sun Sibai
