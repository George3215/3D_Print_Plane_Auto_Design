import cadquery as cq
import math
import os

try:
    from aircraft_config import *
except ImportError:
    print("❌ 错误：未找到 aircraft_config.py 配置文件！")
    exit()

print(f"✨ [APEX V8] 启动巅峰流线型气动建模 (Scale: {PRINT_SCALE})...")

# ==========================================
# 气动截面生成
# ==========================================
def get_manifold_naca_pts(chord, m=0.02, p=0.4, t=0.09, offset=0, n_pts=N_PTS):
    # V8 特性：使用更薄的翼型 (t=0.09 替代 0.12) 以获得高速滑翔性能
    upper, lower = [], []
    for i in range(n_pts + 1):
        beta = math.pi * i / n_pts
        xn = 0.5 * (1 - math.cos(beta))
        yt = 5 * t * (0.2969 * math.sqrt(xn) - 0.1260 * xn - 0.3516 * xn**2 + 0.2843 * xn**3 - 0.1036 * xn**4)
        yt_eff = max(0.001, yt - offset/chord)
        if xn < p: yc = (m / p**2) * (2*p*xn - xn**2) if p > 0 else 0
        else: yc = (m / (1-p)**2) * ((1-2*p) + 2*p*xn - xn**2) if p < 1 else 0
        upper.append((xn * chord, (yc + yt_eff) * chord))
        if i > 0: lower.insert(0, (xn * chord, (yc - yt_eff) * chord))
    return upper + lower

def make_apex_surface(chord_r, chord_t, span, sweep_max, dihedral, washout, has_spar=True):
    """V8 核心逻辑：非线性多截面放样，造就极致半椭圆流动曲线"""
    cr, ct, sp = chord_r * PRINT_SCALE, chord_t * PRINT_SCALE, span * PRINT_SCALE
    sw = sweep_max * PRINT_SCALE
    sections = 6
    wires = []
    
    for i in range(sections):
        ratio = i / (sections - 1)
        
        # 1. 半椭圆弦长衰减方程
        c_local = ct + (cr - ct) * math.sqrt(1 - ratio**2)
        
        # 2. 抛物线后掠曲线
        s_local = sw * (ratio**1.6)
        
        # 3. 线性扭转分布
        w_local = washout * ratio
        
        z_pos = sp * ratio
        pts = get_manifold_naca_pts(c_local)
        w = cq.Workplane("XY").workplane(offset=z_pos).spline(pts).close()
        
        # 横滚轴（Washout）旋转，基于重心 25% 弦长处
        w = w.rotate((c_local*0.25, 0, z_pos), (c_local*0.25, 1, z_pos), w_local)
        
        # 上反角（Dihedral）带来的 Y 轴垂直爬升
        y_dih = math.tan(math.radians(dihedral)) * z_pos
        w = w.translate((s_local, y_dih, 0))
        
        wires.append(w.toPending().objects[0])
        
    solid_surface = cq.Solid.makeLoft(wires, ruled=False)
    final_wp = cq.Workplane(solid_surface)
    
    if has_spar:
        spar_d = SPAR_DIA * PRINT_SCALE
        spar = (
            cq.Workplane("XY").workplane(offset=-2)
            .center(cr*0.25, 0).circle(spar_d/2).extrude(sp*1.2)
            # 主梁孔必须完美贴合几何上反角
            .rotate((cr*0.25,0,0), (cr*0.25+1,0,0), dihedral)
        )
        final_wp = final_wp.cut(spar)
        
    return final_wp.clean().val()

# ==========================================
# V8 总装
# ==========================================
parts = []
fs = FUSE_LENGTH * PRINT_SCALE
fw, fh = FUSE_WIDTH * PRINT_SCALE, FUSE_HEIGHT * PRINT_SCALE

print("🛩️  Apex 构建：可乐瓶曲线机身 (Area Rule Fuselage)...")
fuse_wires = []
for x, wp, hp, z_drop in FUSE_SECTIONS_V8:
    z_offset = z_drop * fh # Z轴下沉量，塑造座舱段凹凸有致
    w = (
        cq.Workplane("YZ").workplane(offset=x*fs)
        .ellipse(fw*wp/2, fh*hp/2)
        # 机身曲线重心偏移变换
        .translate((0, z_offset, 0))
        .toPending().objects[0]
    )
    fuse_wires.append(w)
solid_fuse = cq.Solid.makeLoft(fuse_wires, ruled=False)
parts.append(solid_fuse)

print("🛩️  Apex 构建：半椭圆大展翼机翼 (Semi-Elliptical Wing)...")
wing_r = make_apex_surface(CHORD_ROOT, CHORD_TIP, WING_SPAN, WING_SWEEP, WING_DIHEDRAL, WING_WASHOUT)
wing_wp = cq.Workplane(wing_r).translate((WING_POS_X*PRINT_SCALE, 0, 0))
parts.append(wing_wp.val())
parts.append(wing_wp.mirror("XY").val())

print("🛩️  Apex 构建：现代全后掠 V 尾 (Swept V-Tail)...")
vt_r = make_apex_surface(TAIL_CHORD_ROOT, TAIL_CHORD_TIP, TAIL_SPAN, TAIL_SWEEP, V_TAIL_ANGLE, 0, has_spar=False)
# 尾翼挂载于机身末段的上翘区域，通过 Y 轴上移匹配 Area Rule
tail_base_y = fh * 0.1 
vt_wp = cq.Workplane(vt_r).translate((TAIL_POS_X*PRINT_SCALE, tail_base_y, 0))
parts.append(vt_wp.val())
parts.append(vt_wp.mirror("XY").val())

# 关键修复：使用真布尔并集 (Boolean Union) 融合所有组件，彻底消除 IOU
union_model = cq.Workplane(parts[0])
for p in parts[1:]:
    union_model = union_model.union(cq.Workplane(p))

final_model = union_model.translate((-fs/2, 0, 0)).val()
output_file = 'aircraft_model_final_v8_apex.step'
cq.exporters.export(final_model, output_file)

# 更新数据报告
print(f"✅ V8 Apex 构建完成！导出体积: {int(final_model.Volume())} mm³")
print(f"📦 STEP 模型已保存至：{output_file}")
