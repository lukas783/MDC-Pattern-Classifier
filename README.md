::Authors::
Lucas Carpenter
Joey Brown

::Date::
September 22, 2017

::Program Description::
Pattern Classification using Minimum Distance Classification
This program reads in a CSV file and groups each class into a 
list of features mapped in a N-dimensional plane. Once all data
has been read in to 'train' the program the final entry will be entered
and the closest distance to the centroid of an already known class will
be used as the new entry's class type.
The CSV file format must follow a pattern similar to below
TITLE, #=CLASSNAME1, #=CLASSNAME2, ..., #=CLASSNAMEX
SAMPLE, CLASS, FEATURE1, FEATURE2, ..., FEATUREX
DATA1, DATA2, ...

::Usage::
$> python3.6 mdc.py <input .CSV file>