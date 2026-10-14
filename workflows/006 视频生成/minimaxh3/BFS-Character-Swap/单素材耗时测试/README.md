# 单视频素材：1MP/1.5MP、10–15秒运行时间测试

**当前实测状态：01/02已生成完整成片；03按用户要求中止，04未运行。后续采样已停止。1.5MP仅保留配置，不能宣称完成耗时或稳定性已验证。**

本套只使用一个动作视频：Aerial Invert ｜ PoleMovebook [XIo3cCE4NeU].mp4。原60fps素材已另存为24fps的 `h3_bfs_aerial_full_24fps.mp4`；独立原创橙发青绿服角色PNG继续只作为身份图。

本地入口：`006 视频生成 / minimaxh3 / BFS-Character-Swap / 单素材耗时测试`。四份预设共用同一图结构，通过两个节点调整：

- **① 输出时长秒**：整数10–15秒。公式把超范围值钳制到10–15，自动计算全部帧数、Guide长度、输出帧数和音轨长度。
- **② 分辨率档位**：填写1.0或1.5；小于1.25选择1MP，否则1.5MP。宽高同时连接Guide缩放和ReferenceToVideo。

| 预设 | 实际宽高 | 实际MP | 输出时长/帧数 | H3内部生成帧数 |
| --- | --- | --- | --- | --- |
| 01_1MP_10秒_Sol+Turbo4步 | 1344×768 | 1.032192 | 10秒 / 240帧 | 243 |
| 02_1MP_15秒_Sol+Turbo4步 | 1344×768 | 1.032192 | 15秒 / 360帧 | 362 |
| 03_1.5MP_10秒_Sol+Turbo4步 | 1632×928 | 1.514496 | 10秒 / 240帧 | 243 |
| 04_1.5MP_15秒_Sol+Turbo4步 | 1632×928 | 1.514496 | 15秒 / 360帧 | 362 |

尺寸均为32倍数，Guide使用等比居中裁切，不拉伸。H3内部帧数为 `ceil((seconds×24-5)/17)×17+5`，输出前再裁成目标秒数×24帧，音轨同步裁切。因此“15秒”指最终360帧，不把362帧的15.083秒误写成15秒。原视频从0秒开始，完整长度19.13秒足够所有配置。

## 加速与显存控制

实际模型链：

```text
Ref2VA INT8 → Character Swap正式LoRA(1)
→ 本机已有Ref2VA Turbo4步LoRA(1) → SigmaShift12/3
→ ModelAttentionBackend(comfy kitchen attention)
→ BlockSparseAttention(sol-attn, tau=1.3)
→ MiniMaxChunkFeedForward(8 chunks)
→ EasyCache(threshold=0.10) → 显存统计
→ Euler/simple 4步、CFG1、seed20261014
```

原生BlockSparseAttention已在本机ComfyUI0.39.0注册；`comfy_kitchen.sol_attn_is_available(cuda)`实测为True。没有安装已弃用的旧Sol插件，或整体升级环境。[旧Kijai节点仓库说明](https://github.com/kijai/ComfyUI-SolAttn_triton)也指出目前ComfyUI/Kitchen已提供原生实现。

Sol参数：start_percent=0.15、end_percent=0.95、min_tokens=12288、extra_tokens=256、sink_conditioning=exact_kv_and_rows、verbose=True。它在窗口内使用稀疏producer，其他阶段使用Kitchen INT8稠密注意力。身份与Guide条件行保留精确KV；日志必须出现 `BlockSparseAttention: sparse producer path` 才把该次测试记录为真正启用Sol。

EasyCache启用0.10保守阈值，0.15–0.90窗口；实际是否跳步由日志记录，**不会因为接了节点就宣称缓存带来速度提升**。不同时叠加会改写H3注意力路径的Sage H3/LowVRAM attention补丁。Sol、缓存与Turbo均有质量权衡；需检查动作、脸、手指和倒挂帧。

FFN分8块、VAE1024像素/64帧分块用于降低峰值显存，可能增加一些计算开销，不能直接视为加速倍数。VAE分块重叠128像素、时间重叠8；同一VAE也用于角色与Guide编码。

本套复用现有KJNodes的FFN分块与ModelMemoryUseReportPatch；其他控制、Math、Sol、缓存、音频裁切、采样与视频IO均为核心节点。没有新模型下载或新自定义节点安装。

## 运行时间记录

命令行使用Node22内置WebSocket，无额外pip依赖：

```bash
python3 scripts/build_h3_character_swap_benchmark.py
node scripts/run_h3_character_swap_benchmark.mjs --only 01
node scripts/run_h3_character_swap_benchmark.mjs --only 02
node scripts/run_h3_character_swap_benchmark.mjs --only 03
node scripts/run_h3_character_swap_benchmark.mjs --only 04
```

不传 `--only` 会依次运行四组并跳过已完成项。每次提交前检查队列为空，不打断已有任务；脚本保存prompt_id，重新执行可读取已有任务，不会重复提交。相同图/种子在界面直接运行可能命中ComfyUI整个采样节点缓存；测速要换seed，不能把缓存返回当成一次推理。

测试记录在项目 `results/h3_character_swap_benchmark/`：actual_api、actual_workflow、history、WebSocket事件/节点时间、GPU每2秒采样、服务端日志、生成MP4和ffprobe。总时间按服务端execution_start→execution_success计算；采样时间按WebSocket进入/离开SamplerCustomAdvanced计算，包含该节点内模型准备，属于近似阶段耗时。显存峰值同时有nvidia-smi总GPU用量和KJ采样allocated/reserved日志，二者不是同一个口径。

首次执行包括模型加载和该形状的内核初始化/编译；不同尺寸/长度可能各自支付首次形状成本。输出编码、VAE、Guide编码也计入端到端总时间；不与此前不同尺寸、不同长度、16步工作流做未经控制的加速倍数比较。

实际数据、Sol命中证据和输出检查见[单素材运行时间测试报告](../../results/h3_character_swap_benchmark/单素材运行时间测试报告.md)。输出目录：`/media/wwhvw/备份/comfyui/output/h3_character_swap_benchmark/`。
