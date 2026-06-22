# DET_ML_Uncertainty 项目认知历史

> 完整认知历史，从 105 个 summary 文件、32 个 theory 文件、8 个 wiki phase log、Codex 研究 log 和 BUGREPORT 重建。
> 重建日期: 2026-05-11
> 这是 research-cognition-os skill 的完整工作示例。

---

## 项目概览

**项目名称**: DET_ML_Uncertainty (XMM-Newton 检测似然不确定性)
**核心问题**: 理解 emldetect 的 DET_ML (检测似然) 和 DeltaC (Cash 统计量差) 的统计行为，构建可用于 Eddington bias 校正和完备性估计的生成模型
**研究目标**: 用解析理论替代 XMM 当前使用的 ad-hoc Monte Carlo 校准

---

## 认知阶段 (8 个 Phase)

### Phase 0: Toy World 搭建 (03-28 ~ 03-29)

**核心问题**: 能否用 Gaussian PSF + Poisson 背景 + Cash 拟合构建最小工作模拟？

**关键实验**: cash_components_S{20,50}_b{0.1,1.0}
- 5000 次模拟，验证 MLE 无偏性
- q0 在 S=0 时 ~ chi2(1)
- DET_ML 与 q0 严格单调

**关键发现**:
- MLE 在 S>=10 时无偏 (3σ)
- 方差与 Fisher 信息匹配 ~15%
- p(Ŝ | S, b) ≈ Normal(S, 1/I_SS)

**信任状态**: Trusted (toy model 假设下)
**PSF 依赖**: No (Gaussian toy PSF)

---

### Phase 1: 位置拟合与 Fisher 信息 (03-31 ~ 04-02)

**核心问题**: 三参数 (S, x, y) 拟合会如何改变统计行为？

**关键实验**:
- compare_cash_components_amp_only_vs_3param: 1p vs 3p 对比
- validate_one_vs_threeparam_sigma: 宽度验证
- elliptical_psf_projection_test: 椭圆 PSF 测试

**关键发现**:
- 位置拟合无偏: |mean(x̂) - x_true| < 3σ/√N
- Fisher 矩阵块对角: I_Sx / √(I_SS I_xx) < 5%
- ** surprisingly **: 对称设置下 1p 和 3p 宽度几乎相等！
- 椭圆 PSF 仍保持对称保护，1p=3p 宽度

**信任状态**: Trusted (对称假设下)
**PSF 依赖**: No (仍 Gaussian toy)

---

### Phase 2: 44.6M 基准与条件分布发现 (04-02 ~ 04-06)

**核心问题**: 在大量样本下，条件分布 p(DET_ML | Ŝ, b) 的真实形态是什么？

**关键实验**: 44.6M 样本跨 45 个 (S, b) 格点
- mean formula: q0 = κ(S,b) · I_SS · Ŝ²
- κ = 1.31 · S^0.234 · b^(-0.235), R²=0.994

**关键发现**:
- 条件分布极窄: CV ~17% (远窄于无条件)
- **因子化假说**: p(DET_ML, Ŝ | S_true, b) ≈ p(DET_ML | Ŝ, b) · p(Ŝ | S_true, b)
- 分布非高斯 (45/45 格点 Shapiro-Wilk p < 10^-5)
- 宽度在低 S 时依赖 Ŝ，高 S 时恒定

**信任状态**: Trusted
**PSF 依赖**: No

---

### Phase 3: 投影公式理论推导 (04-03 ~ 04-12)

**核心问题**: 为什么条件分布这么窄？能否从理论上解释？

**关键推导**:
- 投影公式: σ²_R ≈ 4∑μ_i[ln(μ_i/b)]² - 4[∑P_i ln(μ_i/b)]² / [∑P_i²/μ_i]
- 单像素化简: 保留 Poisson 结构，正确缩放
- 1p=3p 宽度相等由对称性保护
- 对称性破缺 (mask 不对称 / 源偏移) → 宽度分裂

**关键实验**:
- mask_asymmetry_kappa_experiment: mask 不对称性 → kappa 分裂
- source_offset_kappa_experiment: 源偏移 → kappa 分裂
- minimal_kappa_model_fit: eta = d_edge/σ_psf 参数化
- factorized_kappa_model_fit: 因子化模型 kappa ≈ kappa_edge * kappa_mask

**信任状态**: Trusted (理论推导)
**PSF 依赖**: No (仍 toy model)

---

### Phase 4: 真实目录挑战 (04-07 ~ 04-12)

**核心问题**: Toy model 的结论能否迁移到真实 XMM 目录？

**关键实验**:
- m2_band2_delta_c: 首次 4XMM-DR14 目录测试
- m2_band2_b_scaling: 背景缩放诊断
- m2_band2_offaxis_correction: 离轴效应
- catalog_psf_shape_gaussian_vs_king: PSF 形状对比

**关键发现**:
- 目录趋势定性一致，但 scatter 更大
- **离轴效应**: 9-11' 处 ML 低 ~6%
- **PSF 形状**: King > Gaussian (wings 更重要)
- 因子化代理在目录上近似成立

**信任状态**: Trusted (目录层面观测)
**PSF 依赖**: No (目录数据)

---

### Phase 5: Deboosting 与覆盖测试 (04-11 ~ 04-14)

**核心问题**: 能否用因子化模型校正 Eddington bias？

**关键实验**:
- m2_band2_empirical_calibration: 目录校准
- m2_band2_ctswin: CTS-window 样本选择
- real_source_selection_overdispersion: 过离散校准

**关键发现**:
- 68% CI 覆盖: 67.2% (目标 68%)
- 95% CI 覆盖: 94.1% (目标 95%)
- 联合 (DET_ML, Ŝ) 模型 vs 纯流量: RMS 7.4 vs 9.1 counts

**信任状态**: Provisional (目录校准，待更多验证)
**PSF 依赖**: No

---

### Phase 6: M31 单波段 emldetect 模拟与 SAS 验证 (05-01 ~ 05-04)

**核心问题**: Python Cash 拟合器能否复现 SAS emldetect？

**关键实验**:
- m31_sb_grid_python_fit: Python vs SAS 批量对比
- fixed_positions_python_vs_eml: 54 位置对比
- fixed_positions_python_vs_theory: Python vs 理论

**关键发现**:
- 固定位置: S_fit/S_eml = 0.997, ML_fit/ML_eml = 0.993
- **pos29 中心奇点**: 优化器卡在初始值
- **离轴依赖**: >10' 时 ML ratio 下降至 0.934
- **scut/ecut 截断效应**: 默认值下 ΔC 低 ~13%
  - 显式 scut=0.9, ecut=15 → Z_std = 1.016 (完美！)
  - **这是 12% 宽度不匹配的根本原因**

**信任状态**: Trusted (Python/SAS 对齐)
**PSF 依赖**: Yes (AnalyticEllbetaPSF)

---

### Phase 7: Sigma 校正与有限计数非线性条件 (05-06 ~ 05-11)

**核心问题**: 理论预测的 sigma 为什么比模拟大？

**关键实验**:
- sigma_finite_ml_correction: 有限 ML 校正
- finite_count_conditional_3param_score: 精确 Poisson 测试
- finite_count_conditional_3param_full_fit: 非线性重拟合测试
- m31_python_path_forward_calibration: 真实 Python 路径前向校准

**关键发现** (层层递进):
1. **K(ML) 行级校正**: 1 - 0.239/sqrt(ML+0.01) — 太工程化
2. **K1 非参数 lookup**: ML bin median ratio — 仍依赖先验
3. **k_cell(ML)**: cell-level 校正 — 改善 cell-level 但 row-level 过校正
4. **精确 Poisson score 测试**: sigma ratio ~1.000 → **局部 score 理论没有被打破**
5. **精确 Poisson 非线性重拟合**: sigma ratio ~0.878-0.988 → **非线性重拟合是 sigma 偏低的真正原因**
6. **理论结构应为两层**:
   ```
   mean_3p, sigma_3p = local Poisson/Fisher score theory (asymptotic backbone)
   sigma_final = k_nonlinear(ML, geometry) * sigma_3p
   ```
7. **psfgen-shift 代理 (负结果)**: ratio ~1.7-1.94，方向反了
8. **真实 Python 路径前向校准 (E010)**: k_forward ~0.956 at ML~10

**信任状态**:
- 局部 Poisson/Fisher 理论: **Trusted**
- 非线性校正 k_forward: **Provisional** (受 AnalyticEllbetaPSF bug 影响)
- 有限 ML 校正: **Provisional**

**PSF 依赖**: Yes (AnalyticEllbetaPSF bug 污染所有 M31 结果)

---

## 关键认知转折点

### T1 (05-02): 12% DeltaC 宽度不匹配真相大白

**之前**: 理论 sigma 比模拟大 ~12%，怀疑理论公式错误或 PSF 问题
**发现**: scut/ecut 截断是根本原因
**证据**: 显式 scut=0.9, ecut=15 → Z_std = 1.016
**影响**: 所有 SAS 目录比较必须考虑截断效应

### T2 (05-06): Python vs SAS 对齐成功

**之前**: 认为 Python 拟合器与 SAS emldetect 有系统性差异
**发现**: 固定位置下几乎完全一致 (S ratio ~1.0, ML ratio ~0.993)
**影响**: Python 路径可以作为 SAS 的有效替代

### T3 (05-08): 非线性条件效应确认

**之前**: 试图用单一 k(ML) 校正所有偏差
**发现**: 偏差根源是有限计数的非线性重拟合，不是理论错误
**影响**: 理论结构改为两层: backbone + nonlinear correction

### T4 (05-11): AnalyticEllbetaPSF 5 个 bug

**发现**: PARAMS[3] 误用为旋转角、PARAMS[4] 被丢弃、(1-eps)方向反了、缺少spoke+azimuth调制、King-only 归一化错误
**影响**: 所有基于 AnalyticEllbetaPSF 的 M31 结果需重新验证

---

## 信任总表 (精简版)

| ID | 项目 | 类型 | PSF依赖 | 信任度 | 状态 |
|----|------|------|---------|--------|------|
| T01 | 解析 DeltaC 公式 (toy model) | Insight | No | High | Trusted |
| T02 | 因子化假说 | Insight | No | High | Trusted (44.6M样本) |
| T03 | κ 因子公式 | Insight | No | High | Trusted |
| T04 | 1p=3p 宽度相等 (对称) | Insight | No | High | Trusted |
| T05 | 投影公式 | Derivation | No | High | Trusted |
| T06 | 44.6M 基准 | Dataset | No | High | Trusted |
| T07 | 目录离轴效应 (~6%) | Observation | No | Med-High | Trusted |
| T08 | scut/ecut 截断效应 | Discovery | No | High | Trusted |
| T09 | Python vs SAS 对齐 (on-axis) | Validation | Partial | High | Trusted |
| T10 | Python vs SAS 对齐 (off-axis) | Validation | Yes | Med-High | I025: 2-6% gap is implementation detail, not model error |
| T11 | 4-step ELLBETA sufficient for DET_ML | Insight | No | High | 8-step vs 4-step ML diff <0.5% (I025) |
| T11 | 有限计数非线性条件 (score正确) | Insight | No | High | Trusted |
| T12 | 非线性重拟合是sigma偏低根因 | Insight | No | High | Trusted |
| T13 | 两层理论: backbone + k_nonlinear | Framework | No | High | Trusted |
| T14 | k_forward ~0.956 (ML~10) | Calibration | Yes | Med | Questioned |
| T15 | K(ML) power-law校正 | Model | No | Medium | Provisional |
| T16 | k1(ML) 非参数lookup | Model | No | Medium | Provisional |
| T17 | k_cell(ML) cell-level校正 | Model | Partial | Medium | Provisional |
| T18 | 因子化代理 (目录M2 band2) | Calibration | No | Med-High | Provisional |
| T19 | Deboosting覆盖测试 | Validation | No | Medium | Provisional |
| T20 | psfgen-shift代理 (E017) | Experiment | No | Low | Deprecated (dead end) |
| T21 | AnalyticEllbetaPSF输出 (5 bugs) | Code | Yes | Low | Questioned |
| T21b | ellbeta_psf_model.py PSF | Code | No | High | 5 bugs全修; spoke角度修(r=0.97); spoke振幅2.7-2.9×偏大但对DET_ML无影响(I025) |
| T22 | sb_grid_1k 84000行 | Dataset | Yes | Low | Questioned |
| T23 | M31 Python path结果 | Experiment | Yes | Low | Questioned |

---

## 负结果 (同样重要)

| 实验 | 结果 | 教训 |
|------|------|------|
| psfgen-shift 代理 | sigma ratio ~1.7-1.94 (方向反了) | 不能用 PSF 平移模拟非线性条件 |
| K(ML) 行级校正 | 高 ML 过校正 | 太工程化，需要更物理的模型 |
| K1 非参数 lookup | 依赖先验 | 不能直接用 |
| 单像素近似 (raw) | 相对误差 93% | 必须考虑有效背景 |
| 目录变量直接解释 | BG_COUNTS 不是总背景 | 必须校正变量解释 |

---

## 当前开放问题

1. **修正 AnalyticEllbetaPSF 后，k_forward 会变化多少？** → ANSWERED: E010b NM re-run gives median 0.930, ML~10: 0.959 vs k(ML)=0.926 (4% offset)
2. **修正 PSF 后，Python vs SAS 对齐是否仍然成立？** → ANSWERED: 4-step sufficient (I025), ~8% implementation offset is not missing physics
3. **非线性校正 k_nonlinear 能否写成更物理的形式？** → ANSWERED: Winginess model k=1/√(1+α·r²·W) with α=0.325
4. **多波段/多图像组合效应如何量化？**
5. **目录 deboosting 在修正后的 PSF 下是否仍然有效？**
6. **W(OFFAXIS) 查找表能否把 5% bias 降到 2%？** → NEXT STEP
7. **Catalog-only ML prediction 能达到什么精度？** → ANSWERED: ~2% bias + 5% uncertainty at ML~10 (with all corrections)

---

## 文件依赖关系

```
theory/ (推导层，不依赖 PSF)
  ├── likelihood_derivation.md
  ├── amp_only_proposition_for_paper_cn.md
  ├── three_param_projection_for_paper_cn.md
  ├── general_sigma_projection_cn.md
  ├── single_pixel_reduction_cn.md
  └── FACTORIZATION_HYPOTHESIS.md

scripts/ (代码层，部分依赖 PSF)
  ├── analyze_m31_*.py (依赖 AnalyticEllbetaPSF — QUESTIONED)
  ├── run_phase*_sims.py (toy model — TRUSTED)
  └── prototype_finite_count_*.py (toy model — TRUSTED)

results/ (数据层)
  ├── cash_components_*_summary.md (toy — TRUSTED)
  ├── sigma_*_summary.md (mixed — 部分 QUESTIONED)
  ├── m31_*_summary.md (依赖 bug PSF — QUESTIONED)
  └── m2_band2_*_summary.md (目录数据 — TRUSTED)
```