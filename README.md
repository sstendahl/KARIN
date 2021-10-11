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

Simulations are done using the BornAgain code-base, which is covered by the same license. 

-----------------------------------------------------------------------------------------------------------------------------------------
**KARIN: Keen Analysis for Reflectivity Involving Neutrons**

KARIN is a data analysis kit for Neutron- and X-Ray reflectivity. 
Note that this is a very early alpha. Currently working features include:

- A fully working sample database. One can add samples and store all relevant details (including location to measurement files). All measurement files of a specific sample can simultaniously be loaded from the Sample Database. 
- Automated peak detection, peak positions can be adjusted by dragging them using the mouse pointer. The peak list is sorted automatically. (Manually adding or removing new peaks will be added in the near future)
- Normalization of data
- Centering off-specular graphs 
- Exporting the edited data to a txt file
- Simulating scattering from multilayers in 2D. (This is still very bare-bones and more of a working prototype)

Features that are planned in the semi-short term can be found in Issues on Gitlab (https://gitlab.com/SjoerdB93/karin/-/issues). These include, but are not limited to:
- Edit existing sample from Sample DB
- Possibility to add and remove peaks manually
- Footprint correction for specular data
- More data modification (shift peak, normalise or multiply by given number)
- Thickness calculations for single-layered films 
- Fully functional specular reflectivity simulations
- A simple sample builder for reflectivity simulations
- Support for 2D maps as obtained at SuperAdam at ILL
- More features for 2D simulations
- In the longer term: simple fitting features, at least for specular data.
