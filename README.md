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
