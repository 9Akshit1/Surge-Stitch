Hello! This is Surge Stitch, a portable, band-aid-sized robot that stitches wounds in 10-15 minutes. 
It detects wound edges, stitches the area, and aims to prevent scarring in future versions. 
It offers a quicker, more efficient alternative to traditional hospital stitching, reducing emergency room wait times and improving access to care.

For more info, look at my Devpost: https://devpost.com/software/surge-stitch
For my video demo, look here: 

When running, the Python code will give the stitching positions using some simple OpenCV (on wound images) to detect wound edges and calculate the best stitching spots. 
Note: The wound images are numbered from 1 to 14.
The stitching postitions (x,y) are given to the Arduino, where the Arduino reads it and starts going to tepositions for stitching usingm motors.
