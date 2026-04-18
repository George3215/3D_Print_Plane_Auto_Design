import cadquery as cq
import math

chord_root = 180.0
chord_tip = 120.0
wing_span = 400.0
skin_thickness = 1.5
cap_thickness = 2.0
rib_thickness = 1.6
rib_spacing = 60.0

def get_naca_pts(chord, m=0.02, p=0.4, t=0.12, offset=0, n_pts=60):
    upper_pts, lower_pts = [], []
    for i in range(n_pts + 1):
        beta = math.pi * i / n_pts
        xn = 0.5 * (1 - math.cos(beta))
        yt = 5 * t * (0.2969 * math.sqrt(xn) - 0.1260 * xn - 0.3516 * xn**2 + 0.2843 * xn**3 - 0.1015 * xn**4)
        
        yt_eff = yt - offset/chord
        if yt_eff <= 0.001:
            continue
            
        if xn < p: yc = (m / p**2) * (2*p*xn - xn**2) if p > 0 else 0
        else: yc = (m / (1-p)**2) * ((1-2*p) + 2*p*xn - xn**2) if p < 1 else 0
            
        xu, yu = xn * chord, (yc + yt_eff) * chord
        xl, yl = xn * chord, (yc - yt_eff) * chord
        
        upper_pts.append((xu, yu))
        lower_pts.insert(0, (xl, yl))
    return lower_pts, upper_pts

def make_capped_wing(chord_r, chord_t, span, m=0.02, want_ribs=False):
    def make_wire(c, off, z):
        low, upp = get_naca_pts(c, m=m, offset=off)
        return cq.Workplane("XY").workplane(offset=z).spline(low).lineTo(*upp[0]).spline(upp[1:]).close().toPending().objects[0]
        
    w_out1 = make_wire(chord_r, 0, 0)
    w_out2 = make_wire(chord_t, 0, span)
    solid_outer = cq.Solid.makeLoft([w_out1, w_out2], ruled=False)
    
    taper = (chord_r - chord_t) / span
    c_in1 = chord_r - taper * cap_thickness
    c_in2 = chord_r - taper * (span - cap_thickness)
    
    w_in1 = make_wire(c_in1, skin_thickness, cap_thickness)
    w_in2 = make_wire(c_in2, skin_thickness, span - cap_thickness)
    solid_inner = cq.Solid.makeLoft([w_in1, w_in2], ruled=False)
    
    if want_ribs:
        ribs_list = []
        num_ribs = int(span / rib_spacing) + 1
        for i in range(num_ribs):
            z_pos = min(i * rib_spacing, span - rib_thickness)
            chr_local = chord_r - taper * z_pos
            rib = cq.Workplane("XY").workplane(offset=z_pos).rect(chr_local*2.5, chr_local).extrude(rib_thickness).val()
            ribs_list.append(rib)
        all_ribs_compound = cq.Compound.makeCompound(ribs_list)
        air_vol = cq.Workplane(solid_inner).cut(all_ribs_compound)
        final_wing = cq.Workplane(solid_outer).cut(air_vol).val()
    else:
        final_wing = cq.Workplane(solid_outer).cut(cq.Workplane(solid_inner)).val()
        
    return final_wing

print("Generating wing...")
test_wing = make_capped_wing(chord_root, chord_tip, wing_span, want_ribs=True)
print("Volume:", test_wing.Volume())
print("Closed:", test_wing.Closed())

