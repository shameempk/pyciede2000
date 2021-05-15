**About**

Python implementation of CIEDE2000 color difference calculation based on this paper:

[The CIEDE2000 Color-Difference Formula: Implementation Notes, Supplementary Test Data, and Mathematical Observations](http://www2.ece.rochester.edu/~gsharma/ciede2000/ciede2000noteCRNA.pdf).

More info: http://www2.ece.rochester.edu/~gsharma/ciede2000/

Use this BibTeX to cite:
```BibTeX
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
```

**Install**

`pip install pyciede2000`

**Usage**

```python
from pyciede2000 import ciede2000

res = ciede2000((50.0000,2.6772,-79.7751), (50.0000,0.0000,-82.7485))

print(res)
```

`ciede2000` accepts two color values as tuples in _Lab_ representation. Also supports optional keyword parameters for para-metric weighting factor `k_L`, `k_C` and `k_H`.

**Output format**

`ciede2000()` returns a dict with all significant fields in CIEDE2000 calculation.

```python
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
```

You might be only interested in the final delta value, `delta_E_00`.

```
print(res['delta_E_00'])
```
