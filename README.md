# Marvin
digitisation control utility (jpeg2000) / utilitaire de contrôle de numérisation (jpeg2000)

This program uses python 2.7 and it is not compatible with python 3.

## Installation
You can use this program by two different ways

### Using Marvin as a script
Marvin can be used with any system compatible with python 2.7 by invoking the command

python "path to marvin" "path to the folder to analyse" "path to the reports"

example (with an Unix system):

python marvin /home/cdsp/img/ /home/cdsp/resports/img_report

### Using marvin as a program (Windows only)
With a Windows system you can use the installer (marvin_installer.exe) and follow this process :

-install python 2.7

-install marvin

-add the path to marvin exec to the path

	-go to computer

	-right click -> properties

	-left column -> advanced system parameters

	-environement variable

	-find "path" in the "system variable" cell and click on it

	-modify (or edit)

	-at the end on the value add ";C:\Program Files (x86)\cdsp\marvin\exec" (in the case you have installed the program with default value, in the oser case adapt this path)

	-click on ok

marvin is now installed.

to use it simply go to the folder you want to scan, type "cmd" in the path bar of the explorer and type marvin in the prompt
