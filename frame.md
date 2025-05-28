# YouTube Multi-Agent System 架构

## 系统概述

一个基于多Agent协作的YouTube视频创作辅助系统，集成了选题、研究、脚本、审查、编辑、缩略图、发布和分析等功能。

```
┌────────────────────┐
│ Strategy Agent     │ ← 从YouTube趋势和新闻生成选题建议
└────────▲───────────┘
         │
         ▼
┌────────────────────┐
│ Research Agent     │ ← 生成深度研究报告
└────────▲───────────┘
         │
         ▼
┌────────────────────┐
│ Scriptwriter Agent │ ← 生成视频脚本（支持多种时长）
└────────▲───────────┘
         │
         ▼
┌────────────────────┐
│ Review Agent       │ ← 审查和改写脚本
└────────▲───────────┘
         │
         ▼
┌────────────────────┐
│ Editor Assistant   │ ← 推荐剪辑素材和音效
└────────▲───────────┘
         │
         ▼
┌────────────────────┐
│ Thumbnail Agent    │ ← 根据标题/内容生成缩略图设计方案（构图、配色、关键词）
└────────▲───────────┘
         │
         ▼
┌────────────────────┐
│ Publishing Agent   │ ← 自动上传YouTube，生成SEO优化元数据，安排发布
└────────▲───────────┘
         │
         ▼
┌────────────────────┐
│ Analytics Agent    │ ← 跟踪性能指标，分析受众，提供优化建议
└────────────────────┘

```

## API接口文档

### 1. Strategy Agent `/strategy`
- 从YouTube趋势和新闻生成选题建议
- 支持多地区选择：主要市场/次要市场/其他地区
- 包含竞品分析和机会评估

### 2. Research Agent `/research`
- 生成深度研究报告
- 支持多个数据源整合
- 提供数据支撑的论证

### 3. Scriptwriter Agent `/script`
- 生成专业视频脚本
- 支持多种时长选项（<10分钟/10-15分钟/>15分钟）
- 根据风格调整内容节奏

### 4. Review Agent `/review`
- 审查脚本质量
- 提供改写建议
- 确保内容准确性

### 5. Editor Assistant `/editor`
- 推荐剪辑素材
- 音效建议
- 导出为剪辑软件可用格式

### 6. Thumbnail Agent `/thumbnail`
- 生成缩略图设计方案
- 提供构图和配色建议
- 优化点击率表现

### 7. Publishing Agent `/publish`
- 视频上传和发布管理
- SEO元数据优化
- 最佳发布时间建议
- 卡片和片尾画面设置

### 8. Analytics Agent `/analytics`
- 追踪视频表现
- 受众分析
- A/B测试建议
- 内容优化建议

## 技术要求

### API密钥
```
DEEPSEEK_API_KEY=您的Deepseek API密钥
YOUTUBE_API_KEY=您的YouTube API密钥
YOUTUBE_CLIENT_SECRETS_FILE=OAuth2客户端凭据路径
```

### 依赖服务
- FastAPI
- YouTube Data API v3
- YouTube Analytics API
- Deepseek API

### 部署要求
- Python 3.8+
- 虚拟环境
- 环境变量配置
- OAuth2认证设置

## 开发规范

1. 代码规范
   - 使用类型注解
   - 完整的错误处理
   - 详细的日志记录

2. API规范
   - RESTful设计
   - 统一的错误响应
   - 请求限制实现

3. 安全规范
   - API密钥管理
   - 认证文件保护
   - 数据加密传输

4. 测试规范
   - 单元测试覆盖
   - 集成测试
   - 性能测试

## 使用流程

1. 创建内容
   - 使用Strategy Agent生成选题
   - Research Agent深入研究
   - Scriptwriter生成脚本
   - Review Agent审查内容

2. 制作准备
   - Editor Assistant辅助剪辑
   - Thumbnail Agent设计封面
   - Publishing Agent优化元数据

3. 发布管理
   - 选择最佳发布时间
   - 设置SEO信息
   - 配置卡片和片尾画面

4. 追踪优化
   - Analytics Agent分析表现
   - 实施优化建议
   - 持续改进内容质量
