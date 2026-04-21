---
theme: seriph
layout: cover
background: ./img/back.png
title: 基于自然语言交互的超算运行数据分析与可视化系统设计与实现
info: |
  ## 毕业设计中期答辩
class: text-section title-slide text-black
transition: slide-left
mdc: true
duration: 12min
---

# 基于自然语言交互的超算运行数据分析

# 与可视化系统的设计与实现

<div class="mt-10 text-left inline-block leading-8">
  <div><b>项目类型：</b>本科毕业设计 中期答辩</div>
  <div><b>项目摘要：</b>面向高性能计算平台运行管理场景的智能交互系统</div>
  <div><b>汇报人：</b>林沫非</div>
  <div><b>汇报日期：</b>2026-04-24</div>
</div>

<!--
老师们好，我是计算机2206的林沫非。

今天汇报的题目是：
“基于自然语言交互的超算运行数据分析与可视化系统设计与实现”。

本项目面向高性能计算平台的运行管理场景，
通过自然语言交互、智能体以及可视化技术，
实现运行数据的自动分析与展示，是一个偏工程实现和系统落地的项目。
-->

---
transition: fade-out
layout: quote
background: ./img/back-right.png
---

# 目录

- 研究背景与课题目标
- 系统设计与技术方案
- 系统展示与实现效果
- 下一步计划


<style>
h1 {
  background-color: #2B90B6;
  background-image: linear-gradient(45deg, #4EC5D4 10%, #146b8c 20%);
  background-size: 100%;
  -webkit-background-clip: text;
  -moz-background-clip: text;
  -webkit-text-fill-color: transparent;
  -moz-text-fill-color: transparent;
}
.slidev-layout {
  background: url('/img/back-right.png') no-repeat right center;
  background-size: cover;
}

</style>

<!--
本次汇报主要分为四个部分：

首先介绍研究背景和课题目标，
然后说明系统设计与技术方案，
接着展示当前已经完成的功能和效果，
最后介绍下一步的工作计划。
-->

---
layout: section
---

# 研究背景与课题目标

---
layout: two-cols
---

# 研究背景
KeyPoint：海量信息 高门槛

### 超算运行场景的典型问题 
- 平台运行数据多、来源复杂，普通用户难以快速获取所需信息
  > 例如作业运行状态、资源占用、历史统计结果往往分散在不同系统或页面中
- 数据查询、统计分析和可视化通常依赖脚本或固定页面，灵活性不足
  > 用户如果想临时提出一个新的分析问题，往往无法直接通过现有页面完成
- 用户提出分析需求时，往往需要掌握数据库、命令行或图表工具，使用门槛高
  > 这使得很多分析需求必须依赖开发者或熟悉平台的人来完成

::right::

<div class="w-full flex mt-6 items-center justify-center">
  <img
    src="./img/terminal.png"
    alt="超算平台运行管理界面"
    class="w-full h-full object-contain"
  />
</div>


<!--
这里简单介绍一下课题背景。

在超算运行管理场景中，数据量非常大，而且来源复杂，
很多分析工作仍然依赖脚本、命令行或者固定页面来完成。

这对非技术用户来说使用门槛较高，也会影响整体分析效率。
所以这个课题首先要解决的问题，就是如何让用户更自然、更低门槛地使用这些分析能力。
-->

---

# 课题目标
KeyPoint：可视化任务流 交互

### 课题目标
- 让用户以自然语言方式描述统计与分析需求
  > 用户不需要先学习 SQL、Shell 或图表配置语法
- 系统自动完成数据查询、统计分析和可视化展示
  > 将“理解问题—调用能力—返回结果”这一过程尽量自动化
- 将智能体执行过程转化为可交互、可追踪的前端任务流程
  > 用户不仅看到最终答案，也能看到系统是如何一步步完成任务的
- 降低超算运行数据分析的使用门槛，提高分析效率和可视化效果
  > 让系统从“只能给结果”进一步变成“能协作完成分析任务”

<div><br/></div>

### 课题定位

**一个面向超算运行数据分析与可视化的自然语言交互系统。**

<!--
这个课题的核心目标是降低使用门槛。

用户只需要用自然语言描述需求，
系统就可以自动完成数据查询、分析和可视化。

同时，我希望把执行过程组织成一个可视化的任务流，
并在关键步骤与用户进行交互。
这样系统就不是简单地做一个聊天框，
而是做成一个真正面向分析任务的交互系统。
-->

---
layout: section
---

# 系统设计与技术方案

---
layout: two-cols
transition: none
---

# 技术栈与系统设计

### 系统分层
1. 页面层：登录页、聊天页、Data Board
   > 负责用户可见界面的组织与切换
2. 状态层：聊天、任务、图表、鉴权状态
   > 统一管理会话过程中的前端状态
3. 协议层：SSE 事件解析、交互 prompt、图表解析
   > 负责把后端流式消息转成可消费的结构化事件
4. 展示层：Markdown、任务卡片、时间线、交互卡片、图表卡片
   > 将不同类型的信息映射到不同的前端组件中


::right::

<div class="w-full flex ml-2 items-center justify-center">
  <img
    src="./img/architecture.png"
    alt="系统架构图"
    class="w-full h-full object-contain"
  />
</div>

<!--
这一页是系统的整体技术方案。

前端基于 Next.js 和 React 构建，
通过 SSE 来承载智能体的流式执行过程。

整体架构分为页面层、状态层、协议层和展示层，
这样的拆分方式可以让系统更清晰：
一方面方便后续扩展新能力，
另一方面也便于维护和调试。
-->

---
layout: two-cols
---

# 技术栈与系统设计

### 系统分层
1. 页面层：登录页、聊天页、Data Board
   > 负责用户可见界面的组织与切换
2. 状态层：聊天、任务、图表、鉴权状态
   > 统一管理会话过程中的前端状态
3. 协议层：SSE 事件解析、交互 prompt、图表解析
   > 负责把后端流式消息转成可消费的结构化事件
4. 展示层：Markdown、任务卡片、时间线、交互卡片、图表卡片
   > 将不同类型的信息映射到不同的前端组件中


::right::

<div><br/></div>
<div><br/></div>

<div class="ml-5">

### 技术栈

</div>

<div class="scale-70 origin-top-left ml-5">

| 类别 | 技术方案 |
|---|---|
| 前端框架 | Next.js 15 + React 19 |
| 语言 | TypeScript |
| UI 组件 | MUI |
| 状态管理 | Zustand |
| 流式协议 | `@microsoft/fetch-event-source` |
| 图表渲染 | Vega-Lite / vega-embed |
| 部署方式 | 静态导出 + Nginx |

</div>


---
layout: two-cols
transition: none
---

# 流式协议设计

### 前端分流策略
- 最终回答：进入答案区
> 保证用户能快速找到结论
- 过程日志：进入任务时间线
> 展示任务推进过程与关键节点
- 用户交互：进入交互卡片
> 便于用户直接确认、选择或补充参数
- 图表结果：进入 Data Board
> 集中展示可视化结果


::right::

<div class="w-full flex ml-2 items-center justify-center">
  <img
    src="./img/stream.png"
    alt="系统架构图"
    class="w-full h-full object-contain"
  />
</div>


<!--
分流是系统的一个关键设计点。

前端不会简单把后端所有输出都当作普通文本展示，
而是根据语义进行分流。

这样可以让最终回答、过程日志、用户交互和图表结果，
分别进入适合自己的展示区域。
这也是我认为这个系统和传统聊天页面相比，一个比较关键的区别。
-->
---
layout: two-cols
---

# 流式协议设计


### 前端分流策略
- 最终回答：进入答案区
> 保证用户能快速找到结论
- 过程日志：进入任务时间线
> 展示任务推进过程与关键节点
- 用户交互：进入交互卡片
> 便于用户直接确认、选择或补充参数
- 图表结果：进入 Data Board
> 集中展示可视化结果


::right::

<div><br/></div>
<div><br/></div>

<div class="ml-5">

### 核心事件

</div>

<div class="scale-70 origin-top-left ml-5">


- `chat_begin`：一次对话任务开始
- `status`：表示当前阶段性状态更新
- `call`：系统向用户发起确认或补充信息请求
- `delta`：流式追加最终回答内容
- `message`：完整回答收束
- `tool_call`：智能体调用外部工具或能力
- `tool_result`：工具返回结果
- `exec_begin`：某段执行过程开始
- `exec_output_delta`：执行输出实时追加
- `exec_error`：执行异常信息
- `exec_end`：执行结束
- `chat_error`：对话级别错误

</div>

---
layout: section
---

# 系统展示与实现效果

---
layout: two-cols
---

# 总体任务流效果


演示场景：用户输入“帮我提交 agenttest 目录下任务”


### 展示内容
- 自然语言输入
  > 用户直接以任务目标来表达需求
- 智能体规划与执行
  > 后端根据目标拆分步骤并选择合适能力
- 前端展示任务卡片与时间线
  > 将执行过程实时反馈给用户
- 用户参与关键决策
  > 例如文件选择、资源配置确认等
- 最终得到结果
  > 给出任务提交反馈与状态结果

::right::

<div class="w-full flex items-center justify-center mt-3 ml-2">
  <video
    src="./video/total.mp4"
    autoplay
    muted
    class="w-full object-cover bg-transparent outline-none"
  ></video>
</div>

<!--
这里展示的是一个完整的任务流示例。

用户输入自然语言后，
智能体会先理解任务目标，然后进行规划与执行，
前端则实时展示任务推进过程。

在关键步骤，系统会请求用户确认或补充参数，
用户完成交互之后，任务继续推进，最终得到结果。

接下来，我会分别展开说明聊天、交互和图表这几个关键机制。
-->

---
layout: two-cols
---

# 聊天系统与任务卡片


### 展示机制
- 支持多轮对话与流式渲染
  > 用户可以连续提出问题，系统逐步返回内容
- 执行过程抽象为任务卡片
  > 将后端行为转成更易理解的前端表达
- 展示状态、进度和日志
  > 让用户知道任务进行到哪一步、当前在做什么
- 最终结果高亮展示
  > 将结果与过程区分开，提升可读性

<div><br/></div>

### 历史任务回放
- 可视化历史任务执行过程，恢复任务时间线
  > 用户后续可以回看任务执行的脉络

::right::

<div class="w-full flex items-center justify-center mt-5">
  <!-- <video
    src="./video/chart_end.mp4"
    controls
    class="w-full object-cover bg-transparent outline-none autoplay"
  ></video> -->
    <img
    src="./img/chat.png"
    alt="系统架构图"
    class="h-full object-contain"
  />
</div>

<!--
这一页主要有两个重点。

第一，聊天本身是流式的，响应会实时展示；
第二，执行过程被抽象成任务卡片，
用户可以更直观地看到每一步的状态和日志。

另外，系统也支持历史任务回放，
这样用户不仅能看当前任务，还能回看之前任务的执行过程。
-->

---
layout: two-cols
---

# 交互式任务流


### 用户参与决策
- 表单交互：适合补充参数、填写任务信息
- 文件选择：在多个候选输入之间进行确认
- 参数选择：资源配置、节点数等运行参数
- 混合输入：同时支持文本输入与选项选择

<div><br/></div>

### 交互价值：协作式执行任务
- 将关键决策节点交还给用户
  > 避免系统在不确定情况下直接替用户做决定
- 保留推荐能力，同时允许人工修正
  > 用户可以接受推荐，也可以自行调整
- 形成“系统规划 + 用户确认”的协作闭环
  > 兼顾自动化程度与可控性

::right::

<div class="w-full flex flex-col items-center justify-center mt-5">
  <img
    src="./img/inter1.png"
    alt="交互1"
    class="h-full object-contain"
  />  
  <img
    src="./img/inter2.png"
    alt="交互2"
    class="h-full object-contain mt-2"
  />
</div>

<!--
系统不是单向问答，而是协作式执行。

智能体会分析任务过程中的关键步骤，
并在这些节点请求用户确认或补充信息。

比如在这个示例里，
系统会在选择可执行文件、设置资源配置等环节发起交互，
同时给出一些推荐选项。

用户可以直接采用推荐，也可以自己调整，
这样就把关键决策保留给了用户，
形成了一个完整的协作闭环。
-->

---
layout: two-cols
---

# 图表展示交互

### Data Board 面板
- 识别 Vega-Lite 并进行展示
  > 智能体返回结构化图表后，前端自动渲染
- 支持“chat with data”
  > 用户可以基于当前图表继续提问和分析
- 自动包装图表上下文发送给智能体
  > 减少用户重复描述上下文的成本

<div><br/></div>

### 当前价值
- 将结果从文本扩展为图表表达
  > 更适合展示趋势、对比、分布等分析结果
- 支持围绕图表继续交互
  > 图表不只是终点，也可以成为下一轮分析的起点

::right::

<div class="w-full flex items-center justify-center mt-15">
  <video
    src="./video/chart_end.mp4"
    autoplay
    muted
    class="w-full object-cover bg-transparent outline-none"
  ></video>
</div>

<!-- 
在可视化方面，
系统可以识别智能体返回的 Vega-Lite 结果，并在 Data Board 中展示。

同时，用户还可以围绕当前图表继续发起交互，
系统会自动把图表相关上下文一起发送给智能体，
从而支持“基于图表继续分析”的使用方式。
-->

---

# 总结

### 系统已经具备
- 自然语言分析入口
  > 用户可以直接通过自然语言发起分析任务
- 统一交互界面
  > 聊天、任务、交互和图表被整合到同一套界面中
- 任务执行闭环
  > 从输入、规划、交互到结果展示已经基本打通
- Nginx 部署落地
  > 具备初步工程化部署能力

<!--
总结来说，
目前系统已经从一个简单的想法，
逐步落成了一个可以实际演示的原型系统。

它已经具备自然语言入口、统一交互界面、任务执行闭环，
以及初步的工程化部署能力。
-->

---
layout: section
---

# 下一步计划

---

# 下一步计划

### 后续工作方向

- 完善自然语言分析流程
  > 提升复杂场景下的理解能力与交互稳定性
- 优化任务展示与交互体验
  > 让任务状态、进度和用户操作更加清晰
- 增强图表与可视化能力
  > 支持更丰富的展示形式和更自然的图表交互
- 推进工程化与部署稳定性
  > 完善真实环境下的部署、联调与运行体验
- 准备论文与答辩材料
  > 梳理系统设计、实现过程和实验展示内容

<!--
下一步主要围绕功能完善、体验优化和工程稳定性推进。

一方面继续提升自然语言分析和交互能力，
另一方面完善可视化和工程化部分。

最后，也会同步推进论文撰写和答辩材料准备。
-->

---
layout: cover
class: text-center title-end
---

# 感谢聆听

<div><br/></div>

### 欢迎老师批评指正

<style>
.slidev-layout {
  background: url('/img/back-left.png') no-repeat right center;
  background-size: cover;
}
</style>

<!--
我的汇报到这里结束，谢谢各位老师的聆听。
欢迎老师批评指正。
-->
