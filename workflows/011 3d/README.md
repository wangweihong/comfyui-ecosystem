  # ComfyUI 3D 工作流
  本目录包含基于 Trellis2 的 3D 模型生成工作流，用于从多视角图像创建高质量的 3D 模型。
  ## 工作流列表
  ### 3D 目录
  #### 1. Trellis2_MV_Combined.json
  - **功能**：完整的多视角 3D 模型生成工作流
  - **特点**：
    - 支持从多个视角（前、后、左、右）的图像生成 3D 模型
    - 包含网格生成和纹理映射
    - 提供完整的参数控制，如种子、管道类型、结构步骤等
    - 生成可直接使用的 3D 模型文件

  #### 2. Trellis2_MV_MeshOnly.json
  - **功能**：专注于网格生成的工作流
  - **特点**：
    - 只生成 3D 网格结构，不包含纹理
    - 包含图像预处理步骤，如背景移除和填充
    - 支持网格优化和重网格化
    - 适合需要自定义纹理的场景

  #### 3. Trellis2_MV_TextureMesh.json
  - **功能**：包含纹理和网格生成的完整工作流
  - **特点**：
    - 生成带纹理的 3D 模型
    - 包含 3D 模型预览功能
    - 支持模型文件导出（GLB 格式）
    - 提供相机和场景配置选项

  #### 4. trellies2_high_quality.json
  - **功能**：高质量 3D 模型生成工作流
  - **特点**：
    - 优化的参数设置，用于生成更高质量的 3D 模型
    - 可能包含更多的细化步骤
    - 适合对模型质量要求较高的场景

  ## 系统要求
  - ComfyUI 环境
  - Trellis2 扩展
  - 足够的 GPU 内存（建议至少 8GB）
  - 多视角输入图像（前、后、左、右视图）

  ### 依赖模型路径
  - [u2net.onnx](https://huggingface.co/tomjackson2023/rembg/tree/main)
    - 模型路径：/root/.u2net/u2net.onnx
  - 图转3d模型
    - [microsoft/trellies.2](https://huggingface.co/microsoft/TRELLIS.2-4B)
      - 模型路径：ComfyUI/models/microsoft/trellies.2/
        ```
            ── TRELLIS.2-4B
        │   ├── ckpts
        │   │   ├── ckpts
        │   │   │   └── ckpts
        │   │   ├── shape_dec_next_dc_f16c32_fp16.json
        │   │   ├── shape_dec_next_dc_f16c32_fp16.safetensors
        │   │   ├── shape_enc_next_dc_f16c32_fp16.json
        │   │   ├── shape_enc_next_dc_f16c32_fp16.safetensors
        │   │   ├── slat_flow_img2shape_dit_1_3B_1024_bf16.json
        │   │   ├── slat_flow_img2shape_dit_1_3B_1024_bf16.safetensors
        │   │   ├── slat_flow_img2shape_dit_1_3B_512_bf16.json
        │   │   ├── slat_flow_img2shape_dit_1_3B_512_bf16.safetensors
        │   │   ├── slat_flow_imgshape2tex_dit_1_3B_1024_bf16.json
        │   │   ├── slat_flow_imgshape2tex_dit_1_3B_1024_bf16.safetensors
        │   │   ├── slat_flow_imgshape2tex_dit_1_3B_512_bf16.json
        │   │   ├── ss_flow_img_dit_1_3B_64_bf16.json
        │   │   ├── ss_flow_img_dit_1_3B_64_bf16.safetensors
        │   │   ├── tex_dec_next_dc_f16c32_fp16.json
        │   │   ├── tex_dec_next_dc_f16c32_fp16.safetensors
        │   │   ├── tex_enc_next_dc_f16c32_fp16.json
        │   │   └── tex_enc_next_dc_f16c32_fp16.safetensors
        │   ├── pipeline.json
        │   ├── README.md
        │   ├── reconviagen_pipeline.json
        │   └── texturing_pipeline.json
        └── TRELLIS-image-large
            └── ckpts
                ├── ss_dec_conv3d_16l8_fp16.json
                └── ss_dec_conv3d_16l8_fp16.safetensors
      ```
    - [visualbruno/trellies2](https://huggingface.co/visualbruno/TRELLIS.2-4B-FP8)
      - 模型路径：ComfyUI/models/visualbruno/TRELLIS.2-4B-FP8/
        ```
          TRELLIS.2-4B-FP8
            ├── ckpts_fp8
            │   ├── shape_dec_next_dc_f16c32_fp8.json
            │   ├── shape_dec_next_dc_f16c32_fp8.safetensors
            │   ├── shape_enc_next_dc_f16c32_fp8.json
            │   ├── shape_enc_next_dc_f16c32_fp8.safetensors
            │   ├── slat_flow_img2shape_dit_1_3B_1024_fp8.json
            │   ├── slat_flow_img2shape_dit_1_3B_1024_fp8.safetensors
            │   ├── slat_flow_img2shape_dit_1_3B_512_fp8.json
            │   ├── slat_flow_img2shape_dit_1_3B_512_fp8.safetensors
            │   ├── slat_flow_imgshape2tex_dit_1_3B_1024_fp8.json
            │   ├── slat_flow_imgshape2tex_dit_1_3B_1024_fp8.safetensors
            │   ├── slat_flow_imgshape2tex_dit_1_3B_512_fp8.json
            │   ├── ss_flow_img_dit_1_3B_64_fp8.json
            │   ├── ss_flow_img_dit_1_3B_64_fp8.safetensors
            │   ├── tex_dec_next_dc_f16c32_fp8.json
            │   ├── tex_dec_next_dc_f16c32_fp8.safetensors
            │   ├── tex_enc_next_dc_f16c32_fp8.json
            │   └── tex_enc_next_dc_f16c32_fp8.safetensors
            ├── pipeline_fp8.json
            └── README.md
    ```
## 输入要求
- 图像格式：支持常见格式（PNG、JPG 等）
- 图像分辨率：建议至少 512x512
- 视角要求：需要提供前、后、左、右四个视角的图像
- 图像质量：清晰、光照一致、背景简单的图像效果更好

## 输出
- 3D 模型文件（GLB 格式）
- 网格数据
- 纹理贴图

## 注意事项
- 生成高质量 3D 模型可能需要较长时间
- 复杂场景可能需要更多的计算资源
- 输入图像的质量直接影响生成结果
- 建议使用相同光照条件下拍摄的图像以获得最佳效果

## 故障排除
- **内存不足**：尝试降低模型分辨率或使用低显存模式
- **模型质量差**：检查输入图像质量，确保视角覆盖完整
- **生成失败**：检查 Trellis2 扩展是否正确安装，以及模型文件是否可用

## 相关资源
- [Trellis2 文档](https://github.com/visualbruno/ComfyUI-Trellis2)
- [ComfyUI 官方文档](https://comfyui.github.io/ComfyUI/)
