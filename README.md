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

* Download and install [python 2.7](https://www.python.org/downloads/release/python-279/)

* install marvin by executing the Marvin installer marvin_installer.exe

* Add the path to marvin exec to the environment variables

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

#### Outputs

Here are some [jpylyzer](https://github.com/openpreserve/jpylyzer/blob/master/doc/jpylyzerUserManual.md) explanations for the generated file *sampledetails.csv* :

* **fileName** : return the value of the property /jpylyzer/fileInfo/fileName (ie. Name of the analysed file without its path).
* **hRescInPixelsPerMeter** : check that the property /jpylyzer/properties/jp2HeaderBox/resolutionBox/captureResolutionBox/hRescInPixelsPerMeter (ie. Horizontal grid resolution, expressed in pixels per meter) exists and is not null.
* **compressionRatio** : check that the property /jpylyzer/properties/compressionRatio (ie. Compression ratio) is included between 6 and 6.1.
* **transformation** : check that the property /jpylyzer/properties/contiguousCodestreamBox/cod/transformation (ie. Wavelet transformation: "9-7 irreversible" or "5-3 reversible") is set to '9-7 irreversible'.
* **isValidJP2** : check that the property /jpylyzer/isValidJP2 (ie. Outcome of the JPEG2000 validation) is set to 'True'.
* **iccDescription** : check that the property /jpylyzer/properties/jp2HeaderBox/colourSpecificationBox/icc/description (ie. Profile description, extracted from 'desc' tag) is set to 'ICC Adobe 98'.
* **colourSpecificationBoxMeth** : check that the property /jpylyzer/properties/jp2HeaderBox/colourSpecificationBox/meth (ie. Specification method. Indicates whether colourspace of this image is defined as an enumerated colourspace or using a (restricted) ICC profile.) is set to 'Restricted ICC'.
* **vRescInPixelsPerMeter** : check that the property /jpylyzer/properties/jp2HeaderBox/resolutionBox/captureResolutionBox/vRescInPixelsPerMeter (ie. Vertical grid resolution, expressed in pixels per meter) exists and is not null.
* **imageHeaderBoxc** : check that the property /jpylyzer/properties/jp2HeaderBox/imageHeaderBox/c (ie. Compression type) is set to 'jpeg2000'.