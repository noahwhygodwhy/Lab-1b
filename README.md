# A* Pathfinding on a map

This is a program written in python for my Intro to AI class. It involves using a* pathfinding to search for the best way to navigate a map of Mendon Ponds Park taking into acount terrain type, elevation, and season.

![The Map](https://i.imgur.com/wcs51Ys.png)

It's a little difficult to see due to the way we were required to represent the nodes and path, but on the right image you can see a purple line scattered with green waypoints. The path follows the footpaths for the most part, and when optimal, crosses a field. It avoids steep uphill and downhill portions and water.

To test if out for yourself, the usage is: python lab1.py [terrainImage] [elevationFile] [pathFile] [season] [outputFileName]

[terrainImage] is the terrain image. terrain.png was the given one, but any image can be used. The colorings are as follows.

<table border="1">

<tbody>

<tr>

<td>Terrain type</td>

<td>Color on map</td>

<td>Photo ([legend](http://cs.rit.edu/~zjb/courses/331/proj1/photo-legend.jpg))</td>

</tr>

<tr>

<td>Open land</td>

<td bgcolor="#f89412">#F89412 (248,148,18)</td>

<td>[A](http://cs.rit.edu/~zjb/courses/331/proj1/photos/A.jpg)</td>

</tr>

<tr>

<td>Rough meadow</td>

<td bgcolor="#ffc000">#FFC000 (255,192,0)</td>

<td> [B](http://cs.rit.edu/~zjb/courses/331/proj1/photos/B.jpg)</td>

</tr>

<tr>

<td>Easy movement forest</td>

<td bgcolor="#ffffff">#FFFFFF (255,255,255)</td>

<td> [C](http://cs.rit.edu/~zjb/courses/331/proj1/photos/C.jpg) · [D](http://cs.rit.edu/~zjb/courses/331/proj1/photos/D.jpg)</td>

</tr>

<tr>

<td>Slow run forest</td>

<td bgcolor="#02d03c">#02D03C (2,208,60)</td>

<td>[E](http://cs.rit.edu/~zjb/courses/331/proj1/photos/E.jpg)</td>

</tr>

<tr>

<td>Walk forest</td>

<td bgcolor="#028828">#028828 (2,136,40)</td>

<td>[F](http://cs.rit.edu/~zjb/courses/331/proj1/photos/F.jpg)</td>

</tr>

<tr>

<td>Impassible vegetation</td>

<td bgcolor="#054918"><font color="#FFFFFF">#054918 (5,73,24)</font></td>

<td>[G](http://cs.rit.edu/~zjb/courses/331/proj1/photos/G.jpg)</td>

</tr>

<tr>

<td>Lake/Swamp/Marsh</td>

<td bgcolor="#0000ff"><font color="#FFFFFF">#0000FF (0,0,255)</font></td>

<td>[H](http://cs.rit.edu/~zjb/courses/331/proj1/photos/H.jpg) · [I](http://cs.rit.edu/~zjb/courses/331/proj1/photos/I.jpg) · [J](http://cs.rit.edu/~zjb/courses/331/proj1/photos/J.jpg)</td>

</tr>

<tr>

<td>Paved road</td>

<td bgcolor="#473303"><font color="#ffffff">#473303 (71,51,3)</font></td>

<td>[K](http://cs.rit.edu/~zjb/courses/331/proj1/photos/K.jpg) · [L](http://cs.rit.edu/~zjb/courses/331/proj1/photos/L.jpg)</td>

</tr>

<tr>

<td>Footpath</td>

<td bgcolor="#000000"><font color="#ffffff">#000000 (0,0,0)</font></td>

<td>[M](http://cs.rit.edu/~zjb/courses/331/proj1/photos/M.jpg) · [N](http://cs.rit.edu/~zjb/courses/331/proj1/photos/N.jpg)</td>

</tr>

<tr>

<td>Out of bounds</td>

<td bgcolor="#cd0065"><font color="#ffffff">#CD0065 (205,0,101)</font></td>

<td></td>

</tr>

</tbody>

</table>

[elevationFile] is a file with x*y floats describing the elevation of the terrain. The actual elevation doesn't relaly matter, it just has to be relative. See mpp.txt for the given one.

[pathFile] is a text file with 2 ints per line. These set the waypoints in pixels to pathfind between. There must be at least two points.

[season] changes a couple settings within the pathfinding. "summer" is the default, but "spring", "fall", and "winter" are also available. Spring is muddy, fall has leaves covering the path making it harder, and winter acounts for ice.

[outputFileName] is the file to save the output to. This will be the original terrain image, but with the path superimposed on it, and with any of the seasonal effects present. ex: winter will have the water near the land frozen over, represented as a ligher blue color.




