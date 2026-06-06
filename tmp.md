
---
layout: two-cols
---

# 典型场景一：自然语言查询与图表展示

### 示例任务

“查询 2025 年 CPU 机时使用情况，并绘制趋势图”

### 实现过程

- 用户以自然语言发起请求
- 智能体规划查询步骤并执行统计
- 后端通过 <code>chart</code> 事件直接返回 Vega-Lite 图表 JSON
- 前端将图表写入任务卡片并同步到 Data Board

### 结果特点

- 结论与过程同时可见
- 图表规范结构化、可复用
- 图表显示不依赖前端手写每一种图形逻辑

::right::

<div class="pt-6 flex items-center justify-center">
  <img
    src="./figures/data_board_detail.png"
    alt="Data Board 图表展示"
    class="w-[96%] object-contain rounded"
  />
</div>

<!--
这个场景体现的是运行数据分析闭环。
用户提出自然语言问题后，系统不仅返回文字结论，还返回结构化图表。
这里需要强调，图表不是前端从文本里猜出来的，而是后端通过 chart 事件按约定直接返回 Vega-Lite 规范。
-->

---
layout: two-cols
---

# 典型场景二：人在回路的任务提交

### 示例任务

“帮我提交某目录下的任务”

### 过程特点

- 系统识别这是带风险的操作，不直接替用户完成
- 对缺失参数和关键资源进行确认
- 通过交互卡片暂停任务，等待用户输入
- 用户提交后，通过 <code>resume</code> 恢复原有上下文继续执行

### 价值

- 保留自然语言交互的便利性
- 避免高风险场景下系统“自作主张”
- 提升过程透明度与可控性

::right::

<div class="pt-6 flex flex-col gap-3 items-center">
  <img
    src="./figures/chat_interation_1.png"
    alt="文件选择交互"
    class="w-[88%] object-contain rounded"
  />
  <img
    src="./figures/chat_end.png"
    alt="提交成功结果"
    class="w-[88%] object-contain rounded"
  />
</div>

<!--
这个场景体现的是 ask 到 resume 的闭环。
对于作业提交这类风险操作，系统不会直接执行到底，而是在关键节点停下来，请用户确认文件、资源参数等信息。
这样智能体是主动的，但控制权仍然在用户手中。
-->

---

# 新增能力：围绕图表继续追问

<div class="grid grid-cols-[1fr_1fr] gap-8 items-center mt-4">
  <div class="text-[15px] leading-7">
    <div class="font-600 text-lg mb-2">实现方式</div>
    <ul>
      <li>前端引入 CopilotKit</li>
      <li>自动包装当前图表规范、图表上下文和会话摘要</li>
      <li>用户可继续用自然语言描述修改需求</li>
      <li>系统返回新的 Vega-Lite 规范并重新渲染</li>
    </ul>
    <div class="font-600 text-lg mt-4 mb-2">支持的追问类型</div>
    <ul>
      <li>修改图表类型，如折线图改为柱状图</li>
      <li>调整筛选范围、时间粒度或分组维度</li>
      <li>围绕当前结果继续分析和解释</li>
    </ul>
    <div class="font-600 text-lg mt-4 mb-2">意义</div>
    <div>
      Data Board 不再是静态展示区域，而成为可持续交互的分析空间。
    </div>
  </div>

  <div class="flex items-center justify-center">
    <img
      src="./figures/data_board_detail.png"
      alt="围绕图表继续追问"
      class="w-[96%] object-contain rounded"
    />
  </div>
</div>

<!--
这是结期阶段最重要的一个新增点。
系统现在已经支持围绕图表继续追问，而不是只生成一张静态图。
通过 CopilotKit，当前图表上下文会被自动包装，用户可以继续用自然语言说“改成柱状图”“按队列分组”等，
系统再返回新的图表规范完成更新。
-->
