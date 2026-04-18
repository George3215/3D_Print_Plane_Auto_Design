<div align="center">
  <img src="assets/blueprint.png" width="800" alt="Apex V8 Aircraft Blueprint">
</div>

# 🚀 Apex Parametric Aircraft Generator

<div align="center">

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![CadQuery 2.4](https://img.shields.io/badge/CadQuery-2.4.0-darkgreen?style=for-the-badge&logo=cplusplus)
![3D Printing](https://img.shields.io/badge/Bambu_Studio-Optimized-orange?style=for-the-badge&logo=bambulab)
![License MIT](https://img.shields.io/badge/License-MIT-blueviolet?style=for-the-badge)

*An intelligent, 100% parametric CAD generation pipeline for high-performance RC Aircraft.*
*将代码转换为物理赛机的纯参数化航模生成系统。*

</div>

## ✨ Highlights / 设计亮点

Apex (V8) 彻底打破了传统 3D 建模的局限，通过极简的 Python 配置，在数秒内即可通过 OpenCASCADE 几何内核渲染出顶级竞赛滑翔机的曲线：

*   👗 **可乐瓶流线机身 (Area Ruled Fuselage)**: 应用非线性的面积律设计，消除多余波阻，呈现高级超跑般的曲面质感。
*   🦅 **半椭圆曲面后掠翼 (Semi-Elliptical Wing)**: 告别僵硬的直线梯形！采用多级非线性放样造就大后掠椭圆翼尖，气动与视觉双重巅峰。
*   🌪 **自动防失速几何 (Washout Twist)**: 默认植入 -2.5° 翼尖下扭偏角，大幅延缓大仰角时的致命翼尖失速（死亡螺旋保护）。
*   ✂️ **V 尾革命 (Swept V-Tail)**: 取代了沉重的十字平垂尾，融合升降舵与方向舵功能的 35° 全后掠 V 型尾翼，赋予整机极客科技感。
*   🖨 **拓竹切片原生渲染 (Bambu Native)**: 输出 100% 水密闭合（Manifold Solid）模型，完美兼容 3D 打印软件的 `Surface Mode (单墙)` 抽壳计算逻辑。

---

## 🛠 Tech Stack / 开发引擎

*   **Core Logic**: `Python`
*   **Geometry Engine**: `CadQuery` (基于 OpenCASCADE 数学体系)
*   **Deployment**: 适配 `Bambu Lab` 体系的 3D 打印工作流

---

## 📦 Setup & Usage / 开始使用

### 1. 环境搭建 (Conda推荐)
由于项目底层依赖强大的 C++ CAD 数学库，建议您在 Miniconda 中运行，避免版本冲突：
```bash
conda create -n cad python=3.10
conda activate cad
pip install -r requirements.txt
```

### 2. 注入你的灵魂 (Configuration)
打开 `aircraft_config.py`，在这里你就是上帝：
*   想飞得更稳？修改 `WING_SPAN` 加长翼展。
*   想更锐利的滑翔？修改 `WING_SWEEP` 增加后掠。
*   管材大小不对？直接修改 `SPAR_DIA` 设置您手头有的碳纤管孔径。

### 3. 一键渲染 (Build Target)
在激活环境后的终端中执行：
```bash
python aircraft_generator.py
```
终端在数秒响应后，会吐出如下信息，并在根目录生成崭新的航模：
```text
✨ [APEX V8] 启动巅峰流线型气动建模...
🛩️ Apex 构建：可乐瓶曲线机身 (Area Rule Fuselage)...
🛩️ Apex 构建：现代全后掠 V 尾 (Swept V-Tail)...
✅ V8 Apex 构建完成！导出体积: 58833 mm³
📦 STEP 模型已保存至：aircraft_model_final_v8_apex.step
```

---

## 🤖 Automaton Heritage / 项目由来 (The Master Prompt)

> 这个项目是由顶级的智能代码 Agent（如 **Google Deepmind Antigravity** 系统）通过多轮结对编程（Pair-Programming）进化而来的标杆级产物。
> 如果您希望利用大语言模型（LLMs）继续在这个基础上疯狂修改（例如自动加装双体起落架系统、开挖舵机暗槽等），您可以直接将下方这段 **[Master Prompt]** 喂给 AI，它会瞬间理解本项目的来龙去脉接手您的工作：

**[LLM Master Architecture Prompt]**
```markdown
你是世界顶级的航空工程建模智能体，精通 Python、CadQuery 框架以及拓竹工作流。
目前你接手的项目是 "Apex Parametric Aircraft"，它拥有三层完全解耦的架构：
1. `aircraft_config.py` 存储物理尺寸变量 (包含 Dihedral, Sweep, Washout, V-Tail 角度以及 面律(Area Rule) 机身曲率系数)。
2. `aircraft_generator.py` 是引擎中心，采用多线段 (Spline) 拟合 NACA 型面，再利用 `cq.Solid.makeLoft(ruled=False)` 执行非线性曲面插值。
3. 机身、主翼与 V 尾最终必须采用深度的 Boolean `union()` 布尔组合形成一个无内腔相交错误的绝对水密 (Manifold) 实体 STEP 导出，且不允许输出预留中空腔体（我们依赖切片软件来自动判断抽壳密度）。

你现在必须遵从这套几何构造范式及水密严科限制，来执行我接下来的任务。
```
---

> *"Made with ❤️ for Aerospace Geeks."*
