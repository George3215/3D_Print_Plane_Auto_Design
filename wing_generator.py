import cadquery as cq
import math

# ==========================================
# 1. 核心参数 (Manifold Design Parameters)
# ==========================================
chord_root = 200.0
chord_tip = 140.0
wing_span = 400.0
rib_thickness = 1.6
rib_spacing = 60.0
skin_thickness = 1.6           # 蒙皮厚度 (mm)
cap_thickness = 2.0            # 端面封盖厚度 (mm) -> 确保实体闭合的关键
spar_dia = 8.2
spar_pos_x = 0.25

print(f"🚀 [INIT] 正在构建“高度水密性”机翼实体 (V2.2)...")

# ==========================================
# 2. 稳健的翼型生成 (钝化后缘版)
# ==========================================
def get_naca_pts(chord, offset=0, n_pts=30):
    m, p, t = 0.02, 0.4, 0.12
    upper_pts, lower_pts = [], []
    for i in range(n_pts + 1):
        beta = math.pi * i / n_pts
        xn = 0.5 * (1 - math.cos(beta))
        yt = 5 * t * (0.2969 * math.sqrt(xn) - 0.1260 * xn - 0.3516 * xn**2 + 0.2843 * xn**3 - 0.1015 * xn**4)
        yt_eff = max(0, yt - offset/chord)
        if xn < p:
            yc = (m / p**2) * (2*p*xn - xn**2)
        else:
            yc = (m / (1-p)**2) * ((1-2*p) + 2*p*xn - xn**2)
        xu, yu = (xn * chord), (yc + yt_eff) * chord
        xl, yl = (xn * chord), (yc - yt_eff) * chord
        if i == 0: upper_pts.append((0.0, 0.0))
        else:
            upper_pts.append((xu, yu))
            lower_pts.insert(0, (xl, yl))
    return lower_pts, upper_pts

def make_airfoil_wire(chord, offset=0, z=0):
    lower, upper = get_naca_pts(chord, offset)
    return (
        cq.Workplane("XY").workplane(offset=z)
        .spline(lower).lineTo(*upper[0]).spline(upper[1:]).close()
        .toPending().objects[0]
    )

# ==========================================
# 3. 构造主体
# ==========================================
print("📐 [STEP 1] 正在生成放样实体...")
root_outer_w = make_airfoil_wire(chord_root, 0, 0)
tip_outer_w = make_airfoil_wire(chord_tip, 0, wing_span)
wing_outer_solid = cq.Solid.makeLoft([root_outer_w, tip_outer_w], ruled=False)

root_inner_w = make_airfoil_wire(chord_root, skin_thickness, cap_thickness)
tip_inner_w = make_airfoil_wire(chord_tip, skin_thickness, wing_span - cap_thickness)
wing_inner_solid = cq.Solid.makeLoft([root_inner_w, tip_inner_w], ruled=False)

# ==========================================
# 4. 内部肋板生成 (Grouped as Compound)
# ==========================================
print("🏗️ [STEP 2] 正在构建内部肋板结构...")
num_ribs = int(wing_span / rib_spacing) + 1
ribs_list = []

for i in range(num_ribs):
    z_pos = min(i * rib_spacing, wing_span - rib_thickness)
    rib = (
        cq.Workplane("XY").workplane(offset=z_pos)
        .rect(chord_root * 2.5, chord_root)
        .extrude(rib_thickness)
        .faces(">Z").workplane()
        .center(chord_root * 0.45, 0).circle(18.0/2).cutThruAll()
        .center(chord_root * 0.25, 0).circle(11.0/2).cutThruAll()
    ).val()
    ribs_list.append(rib)

# 使用 Compound 组合所有肋板，避免 .union() 在不连续实体上的报错
all_ribs_compound = cq.Compound.makeCompound(ribs_list)

# ==========================================
# 5. 负空间建模
# ==========================================
print("🔗 [STEP 3] 正在通过负空间逻辑执行合并...")
# 内部空气 = 空腔 - 肋板
air_vol = wing_inner_solid.cut(all_ribs_compound)
# 机翼 = 外部主体 - 内部空气
wing_structure = wing_outer_solid.cut(air_vol)

# 主梁贯穿孔
final_model = cq.Workplane(wing_structure).center(chord_root * spar_pos_x, 0).circle(spar_dia/2).cutThruAll().clean()

# ==========================================
# 6. 验证与导出
# ==========================================
is_closed = final_model.val().Closed()
print(f"💎 实体水密性检查 (Closed): {is_closed}")

output_file = 'wing_model_watertight_final.step'
print(f"📦 [EXPORT] 正在导出模型至 {output_file}...")
cq.exporters.export(final_model, output_file)
print(f"✅ 完成！请检查 {output_file}")