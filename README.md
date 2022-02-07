## KARIN
This program is part a personal tool for my personal data analysis, and part a hobby project. It comes with no warranty and no hard gaurantee for support outside of my personal gratitude. This program is licensed under the GPLv3, which in short entails the following points:
1. Anyone can copy, modify and distribute this software.
2. You have to include the license and copyright notice with each and every distribution.
3. You can use this software privately.
4. You can use this software for commercial purposes.
5. If you dare build your business solely from this code, you risk open-sourcing the whole code base.
6. If you modify it, you have to indicate changes made to the code.
7. Any modifications of this code base MUST be distributed with the same license, GPLv3.
8. This software is provided without warranty.
9. The software author or license can not be held liable for any damages inflicted by the software.
A full version of this license should have come with this program, and can otherwise be found at: https://www.gnu.org/licenses/gpl-3.0.html
-----------------------------------------------------------------------------------------------------------------------------------------
**KARIN: Keen Analysis for Reflectivity Involving Neutrons**

KARIN is a data analysis kit for Neutron- and X-Ray reflectivity. 
Note that this is a very early alpha. Development is done on Fedora so testing is mostly focused on Linux, however limited testing is done on Windows 11 as well. In time I am planning to release an installer for Windows as well as RPM and Deb packages for Linux via Fedora and Ubuntu respectively. 
 
Currently working features include:
- A fully working Sample Database (SampleDB). The SampleDB gets its information from the included csv file. Both specular and off-specular measurements of the selected Samples are loaded automatically when closing the SampleDB. The shortkey Ctrl+D opens SampleDB.
- Normalizatin of measurements for easy comparison
- When loading multiple measurements simultaniously, it is possible to shift them vertically in the SampleDB for easy comparison.
- A vertical line can be inserted in order to compare vertically shifted plots. This line can be dragged around by the mouse pointer
- Automated peak detection, peak positions can be adjusted by dragging them using the mouse pointer while in drag mode.
- Manual peak insertion or removal while in Add peak mode or in Remove Peak mode respectively. 
- Manual settings for wavelength, graph theme and style and attributes displayed in legend.

Features that are planned in the semi-short term include, but are not limited to:
- Ability to switch between X-ray and Neutron data
- Conversion from theta to q-space and vice-versa
- Simulations (both specular and full 2D maps) using the BornAgain code-base
- Data manipulation tools such as shift in x-data, and cutting selected parts of the measurement (e.g. direct beam)
- Footprint correction for specular data
- A simple sample builder for reflectivity simulations
- Support for 2D maps as obtained at SuperAdam at ILL
- In the longer term: simple fitting features, at least for specular data.

