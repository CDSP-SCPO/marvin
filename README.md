# Marvin
digitisation control utility (jpeg2000) / utilitaire de contrôle de numérisation (jpeg2000)

This program uses python 2.7 and it is not compatible with python 3.

## How to use it ?

### As a script

Marvin can be used with any system compatible with python 2.7 by invoking the command

`python path/to/marvin path/to/images/folder path/to/outputs`

*example (with an Unix system)*

`python marvin /home/cdsp/img/ /home/cdsp/resports/img_report`

### As a program (Windows only)

#### Installation

With a Windows system you can use the installer (marvin_installer.exe) and follow this process :

- Download and install [python 2.7](https://www.python.org/downloads/release/python-279/)

- install marvin by executing the Marvin installer marvin_installer.exe

- Add the path to marvin exec to the environment variables

	* Go to computer

	* Right click -> properties

	* Left column -> advanced system parameters

	* Environment variable

	* Find "path" in the "system variable" cell and click on it

	* Modify (or edit)

	* At the end on the value add ";C:\Program Files (x86)\cdsp\Marvin\exec" (in the case you have installed the program with default value, in the oser case adapt this path)

	* Click on ok

Congrats, Marvin is now installed !

#### Use

* Open your jpeg2000 images folder

* Type "cmd" in the path bar of the explorer

* A terminal should prompt

* Type "marvin" in the prompt