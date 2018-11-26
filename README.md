# P.U.C.E.35 Version 0.1.0
Python Universal Cell Evaluator - Evaluates solar cell data and automatically interacts with OriginLab

This is my first larger project using Python. The motivation behind this project is to simplify the task of evaluating raw data obtained from measuring I/V curves of solar cells. Since many devices give vastly varrying output data, I hoped to create a way to easily evaluate these data files universally, hance the acronym. Since I use OriginLab to create my plots, and OriginLab has support for Python 3.5 as of OriginPro 2017, I also wanted to automate the process of creating plots and displaying the evaluated data. 

For GUI components I used PyQt, but because of the limited way in which you can use Python in OriginLab, adding external modules is difficult. The best way in which I was able to implement PyQt was to add the module files into the local folder of the puce.py file and then incorporate the module into the beginning of the puce.py file.
It is also necessary to import a special module provided by OriginLab called PyOrigin. This is what allows for the communication between Python and OriginLab, such as the use of LabTalk commands.

In order to use this with OriginLab, all that's necessary is to download all the files and open puce.opj in any OriginPro version supporting Python 3.5. From there, by clicking "Import Data", the puce.py script is launched, opening the GUI. This script was built using Python 3.5 and PyQt5.
