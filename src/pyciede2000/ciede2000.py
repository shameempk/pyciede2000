'''
This cie_de_2000 implementation is based on the papers: 
1. 
@article{Sharma2005TheObservations,
    title = {{The CIEDE2000 color-difference formula: Implementation notes, supplementary test data, and mathematical observations}},
    year = {2005},
    journal = {Color Research {\&} Application},
    author = {Sharma, Gaurav and Wu, Wencheng and Dalal, Edul N},
    number = {1},
    month = {2},
    pages = {21--30},
    volume = {30},
    publisher = {Wiley Subscription Services, Inc., A Wiley Company},
    url = {http://dx.doi.org/10.1002/col.20070},
    doi = {10.1002/col.20070},
    issn = {1520-6378},
    keywords = {CIE, CIE94, CIEDE2000, CIELAB, CMC, color-difference metrics}
}

2. 
@article{Luo2001TheCIEDE2000,
    title = {{The development of the CIE 2000 colour-difference formula: CIEDE2000}},
    year = {2001},
    journal = {Color Research {\&} Application},
    author = {Luo, M R and Cui, G and Rigg, B},
    number = {5},
    month = {10},
    pages = {340--350},
    volume = {26},
    publisher = {John Wiley {\&} Sons, Inc.},
    url = {http://dx.doi.org/10.1002/col.1049},
    doi = {10.1002/col.1049},
    issn = {1520-6378},
    keywords = {BFP, CIE, CIE94, CIEDE2000, CIELAB, CMC, LCD, color difference metrics}
}
    
'''

from math import sqrt, pow, atan2, degrees, fabs, radians, exp, sin, cos
from typing import Dict, Tuple

class InvalidColorValues(Exception):
    """Exception raised for invalid color values.

    Attributes:
        _tuple -- input tuple which caused the error
        message -- explanation of the error
    """

    def __init__(self, _tuple, message="Tuple not in valid (L*, a*, b*) format"):
        self._tuple = _tuple
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self._tuple} -> {self.message}'

class InvalidLabValues(Exception):
    """Exception raised for invalid L*a*b* values.

    Attributes:
        lab -- input lab which caused the error
        message -- explanation of the error
    """

    def __init__(self, lab, message="Value not in valid L*a*b* color space. L*: 0..100 a*: -128..127 b*: -128..127"):
        self.lab = lab
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.lab} -> {self.message}'

def ciede2000(lab1: Tuple, lab2: Tuple, k_L: int = 1, k_C: int = 1, k_H: int = 1) -> Dict[str, float]:
	"""
	This function return calculated CIEDE2000 color difference value of two input Lab color space elements. 

		:param lab1: Lab representation of colour 1 as a tuple.
		:param lab2: Lab representation of colour 2 as a tuple.
		:param k_L: Para-metric  weighting  factor kL.
		:param k_C: Para-metric  weighting  factor kC.
		:param k_H: Para-metric  weighting  factor kH.
		:returns: CIEDE2000 color difference of provided colors.
	"""

	# Error handling
	for color in (lab1, lab2):
		# Check for length of input
		if(len(color) != 3):
			raise InvalidColorValues(color)
		# Make sure L* value is in range 0 to 100
		if color[0] < 0 or color[0] > 100:
			raise InvalidLabValues(color[0])
		# Make sure a* and b* is in range -128 to 127
		for ab in color[1:]:
			if ab < -128 or ab > 127:
				raise InvalidLabValues(ab)

	L_1_star,a_1_star,b_1_star=lab1
	L_2_star,a_2_star,b_2_star=lab2
	C_1_star=sqrt(pow(a_1_star,2)+pow(b_1_star,2))
	C_2_star=sqrt(pow(a_2_star,2)+pow(b_2_star,2))
	C_bar_star=(C_1_star+C_2_star)/2
	
	G=0.5*(1-sqrt(pow(C_bar_star,7)/(pow(C_bar_star,7)+pow(25,7))))
	
	a_1_dash=(1+G)*a_1_star
	a_2_dash=(1+G)*a_2_star
	C_1_dash=sqrt(pow(a_1_dash,2)+pow(b_1_star,2))
	C_2_dash=sqrt(pow(a_2_dash,2)+pow(b_2_star,2))
	h_1_dash=degrees(atan2(b_1_star,a_1_dash))
	h_1_dash += (h_1_dash < 0) * 360
	h_2_dash=degrees(atan2(b_2_star,a_2_dash))
	h_2_dash += (h_2_dash < 0) * 360
	
	delta_L_dash=L_2_star-L_1_star
	delta_C_dash=C_2_dash-C_1_dash
	delta_h_dash=0.0
	
	if(C_1_dash*C_2_dash):
		if(fabs(h_2_dash-h_1_dash)<=180):
			delta_h_dash=h_2_dash-h_1_dash
		elif(h_2_dash-h_1_dash>180):
			delta_h_dash=(h_2_dash-h_1_dash)-360
		elif(h_2_dash-h_1_dash)<-180:
			delta_h_dash=(h_2_dash-h_1_dash)+360
	
	delta_H_dash=2*sqrt(C_1_dash*C_2_dash)*sin(radians(delta_h_dash)/2.0)
	
	L_bar_dash=(L_1_star+L_2_star)/2
	C_bar_dash=(C_1_dash+C_2_dash)/2
	h_bar_dash=h_1_dash+h_2_dash
	
	if(C_1_dash*C_2_dash):
		if(fabs(h_1_dash-h_2_dash)<=180):
			h_bar_dash=(h_1_dash+h_2_dash)/2
		else:
			if(h_1_dash+h_2_dash)<360:
				h_bar_dash=(h_1_dash+h_2_dash+360)/2
			else:
				h_bar_dash=(h_1_dash+h_2_dash-360)/2

	T=1-0.17*cos(radians(h_bar_dash-30))+0.24*cos(radians(2*h_bar_dash))\
	+0.32*cos(radians(3*h_bar_dash+6))-0.20*cos(radians(4*h_bar_dash-63))
	
	delta_theta=30 * exp(- pow( (h_bar_dash-275) / 25, 2))
	
	R_c=2*sqrt( pow(C_bar_dash,7) / (pow(C_bar_dash,7)+pow(25,7)) )
	
	S_L=1+((0.015*pow(L_bar_dash-50,2))/sqrt(20+pow(L_bar_dash-50,2)))
	S_C=1+0.045*C_bar_dash
	S_H=1+0.015*C_bar_dash*T
	R_T=-R_c * sin(2*radians(delta_theta))
	
	delta_E_00 = sqrt(pow(delta_L_dash/(k_L*S_L),2)+\
		pow(delta_C_dash/(k_C*S_C),2)+\
		pow(delta_H_dash/(k_H*S_H),2)+\
		R_T*(delta_C_dash/(k_C*S_C))*(delta_H_dash/(k_H*S_H))\
		)
	res = {
			"a_1_dash": a_1_dash,
			"a_2_dash": a_2_dash,
			"C_1_dash": C_1_dash,
			"C_2_dash": C_2_dash,
			"h_1_dash": h_1_dash,
			"h_2_dash": h_2_dash,
			"h_bar_dash": h_bar_dash,
			"G": G,
			"T": T,
			"S_L": S_L,
			"S_H": S_H,
			"S_C": S_C,
			"R_T": R_T,
			"delta_E_00": delta_E_00
	}
	return res