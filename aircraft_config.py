# aircraft_config.py
# ==========================================
# 航模 V8 Apex - 巅峰全流线竞技级配置
# ==========================================
import math

# 1. 基础环境
PRINT_SCALE = 0.3      
N_PTS = 25              

# 2. 核心气动面尺寸 (mm)
CHORD_ROOT = 180.0
CHORD_TIP = 60.0       # V8: 翼尖更锐利，追求极端流线
WING_SPAN = 450.0      # V8: 拉长翼展，增强滑翔比
WING_POS_X = 140.0     
FUSE_LENGTH = 550.0
FUSE_WIDTH = 55.0
FUSE_HEIGHT = 70.0

# 3. 气动特性 (Apex 特征)
WING_DIHEDRAL = 2.0    # 竞技滑翔机无需太大上反
WING_SWEEP = 35.0      # V8: 大幅度弧形后掠
WING_WASHOUT = -2.5    
SPAR_DIA = 8.2         

# 4. 全后掠 V 尾布局 (V-Tail Layout)
TAIL_CHORD_ROOT = 110.0
TAIL_CHORD_TIP = 50.0
TAIL_SPAN = 150.0
TAIL_SWEEP = 40.0
TAIL_POS_X = 460.0     
V_TAIL_ANGLE = 35.0    # V尾与水平面的夹角 (度)

# 5. 面积律流线机身 (Area Rule Fuselage Sections)
# (X位置比例, 宽比, 高比, Z轴下沉比) -> 塑造下沉的座舱和上翘的尾部
FUSE_SECTIONS_V8 = [
    (0.00,  0.1,  0.15,  0.0),    # 尖锐抛物线机头
    (0.15,  0.7,  0.8,  -0.1),    # 前部
    (0.30,  1.0,  1.0,  -0.2),    # 座舱 (最宽处)
    (0.45,  0.85, 0.9,  -0.15),   # ★面积律收腰点 (机翼根部结合处)
    (0.70,  0.5,  0.6,  -0.05),   # 细长过渡段
    (0.90,  0.3,  0.4,   0.1),    # 尾部上翘
    (1.00,  0.1,  0.1,   0.2)     # 机尾气动收束点
]
