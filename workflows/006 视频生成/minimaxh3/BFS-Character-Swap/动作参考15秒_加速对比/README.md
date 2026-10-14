# 动作参考15秒：加速方案与Turbo组合

侧栏入口：`006 视频生成/minimaxh3/BFS-Character-Swap/动作参考15秒_加速对比`。

原版无加速基线已取消。当前保留七个活动方案；完成7/7组。所有方案读取同一个独立角色PNG和同一个动作视频，保存精确15秒、768×1344、24fps完整MP4及源音轨。用户自行判定质量，没有导出帧图。

| 方案 | 步数 | Turbo LoRA | 状态 | 完整生成耗时 | 采样阶段耗时 |
| --- | ---: | --- | --- | ---: | ---: |
| 02_仅Turbo_4步 | 4 | 有 | 已完成 | 632.448秒 (10.54分钟) | 602.129秒 |
| 03_Turbo+Sol_4步 | 4 | 有 | 已完成 | 717.549秒 (11.96分钟) | 579.753秒 |
| 04_Turbo+Spark-H3_4步 | 4 | 有 | 已完成 | 682.326秒 (11.37分钟) | 652.085秒 |
| 05_Turbo+VEDA_4步 | 4 | 有 | 已完成 | 353.355秒 (5.89分钟) | 321.554秒 |
| 06_仅Sol_16步 | 16 | 无 | 已完成 | 2309.627秒 (38.49分钟) | 2280.068秒 |
| 07_仅Spark-H3_16步 | 16 | 无 | 已完成 | 2441.209秒 (40.69分钟) | 2411.523秒 |
| 08_仅VEDA_16步 | 16 | 无 | 已完成 | 993.426秒 (16.56分钟) | 963.193秒 |

共同加速后端Kitchen INT8，EasyCache关闭。02–05加载已有Ref2VA Turbo4步LoRA并使用Euler/simple；06–08不加载Turbo，使用16步er_sde/simple，仍加载Character Swap功能LoRA。FFN8块及VAE分块为共同显存保护。注意“仅Sol／Spark／VEDA”也包含共同Kitchen稠密后端。Sol、Spark、VEDA三种稀疏算法不相互叠加。

新增节点包：ComfyUI-Spark-H3官方comfyui-v0.1.3的SM120/CUDA13.0 Linux版本，后端comfy-kitchen0.2.37+spark.h3.sm120.cu130.1；ComfyUI-Veda来源veda-sparse/Veda-on-ComfyUI，commit67e4eb5541b648555563144401ebaba832bd73ec。节点源码永久副本保存在 `/media/wwhvw/备份/comfyui/custom_nodes`，当前运行节点位于测试容器临时挂载目录；重建容器需恢复节点并安装Spark wheel。

VEDA模型：`/root/ComfyUI/models/veda/minimax_h3_r2va_veda_preview_fp8.safetensors`，275415752字节，SHA256 `23edace948693772be33d5cc945d302d2b037a29bd44bd57071bfbdd8b02517d`。需以下载清单中验证结果为准。

工作流生成：`python3 scripts/build_h3_acceleration_compare.py`。单组执行：`node scripts/run_h3_acceleration_compare.mjs --only 03`；全部执行会跳过已成功完成的组。报告更新：`python3 scripts/report_h3_acceleration_compare.py`。先查看队列是否空闲，避免与其他任务竞争GPU。

[完整实测报告](</home/wwhvw/文档/ChatGPT/生图/results/h3_acceleration_compare/15秒1MP加速时长对比.md>)。首次初始化、内核编译及条件缓存会影响端到端时间；报告同时保留采样耗时，采样缓存结果不计入。保留既有工作流和已取消原版的执行记录。

## 同步Video Compare

4列×2行、3072×2912、24fps、完整15秒。上排依次为Turbo、Turbo＋Sol、Turbo＋Spark-H3、Turbo＋VEDA；下排依次为原动作参考、Sol16步、Spark-H3 16步、VEDA16步。所有画面从0秒同步播放，七份生成画面均保留768×1344原分辨率；标注方案、步数与实际完整生成耗时。仅保留一条源音轨，没有导出帧图或添加质量评价。

![七方案与动作参考同步Video Compare](</home/wwhvw/文档/ChatGPT/生图/results/h3_acceleration_compare/video_compare/H3_15秒1MP_七方案同步VideoCompare.mp4>)

复现脚本：`scripts/build_h3_video_compare.py`；布局与输出规格记录：`results/h3_acceleration_compare/video_compare/comparison_manifest.json`。
