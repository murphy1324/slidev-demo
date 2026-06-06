from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


OUT_PATH = Path(__file__).with_name("frontend_component_state_flow.png")
W, H = 2048, 1478


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise RuntimeError("No suitable Chinese font found.")


TITLE = load_font(34, bold=True)
SUB = load_font(14)
COL = load_font(18, bold=True)
CARD = load_font(24, bold=True)
BODY = load_font(17)
FOOT = load_font(12)

PANEL_BORDER = (224, 230, 239)
PANEL_FILL = (249, 250, 252)
TEXT_MAIN = (45, 61, 82)
TEXT_SUB = (96, 112, 128)
BLUE = (57, 113, 217)
GREEN = (47, 153, 93)
ORANGE = (212, 129, 18)
PURPLE = (113, 76, 194)
LIGHT_BLUE = (198, 216, 242)
LIGHT_GREEN = (205, 234, 220)
LIGHT_ORANGE = (250, 226, 192)
LIGHT_PURPLE = (227, 218, 248)
LINE_BLUE = (57, 113, 217)
LINE_GREEN = (47, 153, 93)
LINE_ORANGE = (181, 108, 14)
LINE_PURPLE = (113, 76, 194)

PANELS = [
    (40, 120, 410, 1220),
    (485, 120, 930, 1220),
    (980, 120, 1425, 1220),
    (1470, 120, 2015, 1220),
]


def center_text(draw: ImageDraw.ImageDraw, box, text, font, fill=TEXT_MAIN):
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    draw.text(
        (x1 + (x2 - x1 - width) / 2, y1 + (y2 - y1 - height) / 2 - 2),
        text,
        font=font,
        fill=fill,
    )


def draw_wrapped_text(draw: ImageDraw.ImageDraw, box, text, font, fill=TEXT_MAIN, line_gap=5):
    x1, y1, x2, _ = box
    max_width = x2 - x1
    y = y1
    for paragraph in text.split("\n"):
        if not paragraph:
            y += font.size + line_gap
            continue
        line = ""
        for ch in paragraph:
            test = line + ch
            if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
                line = test
            else:
                draw.text((x1, y), line, font=font, fill=fill)
                y += font.size + line_gap
                line = ch
        if line:
            draw.text((x1, y), line, font=font, fill=fill)
            y += font.size + line_gap


def split_card_title(title: str) -> list[str]:
    manual = {
        "AuthManager + MainLayout 布局组件": ["AuthManager + MainLayout", "布局组件"],
        "SideMenu / HomeMenuItem 组件": ["SideMenu / HomeMenuItem", "组件"],
        "DashboardSidebar / DashboardPanel 组件": ["DashboardSidebar / DashboardPanel", "组件"],
        "Backend APIs 接口层": ["Backend APIs", "接口层"],
        "DashboardSidebar / DashboardPanel 组件": ["DashboardSidebar / DashboardPanel", "组件"],
    }
    if title in manual:
        return manual[title]
    return [title]


def draw_card(draw: ImageDraw.ImageDraw, x, y, w, h, header_color, body_color, title, body):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=body_color, outline=(208, 216, 228), width=2)
    title_lines = split_card_title(title)
    header_h = 56 if len(title_lines) > 1 else 40
    draw.rounded_rectangle((x, y, x + w, y + header_h), radius=18, fill=header_color)
    draw.rectangle((x, y + 20, x + w, y + header_h), fill=header_color)

    title_font = CARD
    longest = max(title_lines, key=len)
    while draw.textbbox((0, 0), longest, font=title_font)[2] > w - 30 and title_font.size > 14:
        title_font = load_font(title_font.size - 1, bold=True)

    if len(title_lines) == 1:
        center_text(draw, (x, y + 5, x + w, y + 36), title_lines[0], title_font, "white")
    else:
        line_gap = 2
        b1 = draw.textbbox((0, 0), title_lines[0], font=title_font)
        b2 = draw.textbbox((0, 0), title_lines[1], font=title_font)
        h1 = b1[3] - b1[1]
        h2 = b2[3] - b2[1]
        total_h = h1 + h2 + line_gap
        start_y = y + (header_h - total_h) / 2 - 1
        w1 = b1[2] - b1[0]
        w2 = b2[2] - b2[0]
        draw.text((x + (w - w1) / 2, start_y), title_lines[0], font=title_font, fill="white")
        draw.text((x + (w - w2) / 2, start_y + h1 + line_gap), title_lines[1], font=title_font, fill="white")

    draw_wrapped_text(draw, (x + 16, y + header_h + 12, x + w - 16, y + h - 16), body, BODY, TEXT_MAIN, line_gap=4)


def draw_arrow(draw: ImageDraw.ImageDraw, p1, p2, color, width=4, head=12):
    import math

    x1, y1 = p1
    x2, y2 = p2
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    a1 = angle + math.pi * 0.88
    a2 = angle - math.pi * 0.88
    hx1 = x2 + head * math.cos(a1)
    hy1 = y2 + head * math.sin(a1)
    hx2 = x2 + head * math.cos(a2)
    hy2 = y2 + head * math.sin(a2)
    draw.polygon([(x2, y2), (hx1, hy1), (hx2, hy2)], fill=color)


def main():
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    for x1, y1, x2, y2 in PANELS:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=24, fill=PANEL_FILL, outline=PANEL_BORDER, width=2)

    center_text(draw, (0, 15, W, 58), "agent_front 前端组件与状态流", TITLE)
    center_text(draw, (0, 60, W, 84), "基于真实项目结构整理，供论文配图使用", SUB, TEXT_SUB)

    headers = [
        ("页面入口与布局骨架", BLUE, PANELS[0]),
        ("交互组件层", GREEN, PANELS[1]),
        ("协议与状态管理", ORANGE, PANELS[2]),
        ("任务与图表渲染", PURPLE, PANELS[3]),
    ]
    for text, color, (x1, y1, x2, y2) in headers:
        draw.rounded_rectangle((x1 + 10, y1 + 8, x2 - 10, y1 + 48), radius=18, fill=color)
        center_text(draw, (x1 + 10, y1 + 10, x2 - 10, y1 + 44), text, COL, "white")

    draw_card(draw, 65, 210, 325, 150, BLUE, LIGHT_BLUE, "LoginPage 组件",
              "仿 SSH 的登录入口\n填写 IP、端口、用户名、密码\n调用 useAuthStore.login() 建立连接")
    draw_card(draw, 65, 400, 325, 170, BLUE, LIGHT_BLUE, "AuthManager + MainLayout 布局组件",
              "负责认证守卫与主布局\n组织历史侧栏、聊天区与 Data Board\n未登录时跳转回登录页")
    draw_card(draw, 65, 620, 325, 160, BLUE, LIGHT_BLUE, "ChatPage 页面组件",
              "聊天主页面组合根节点\n渲染 ChatArea 与 ChatBox\n新消息到达后自动滚动")
    draw_card(draw, 65, 840, 325, 180, BLUE, LIGHT_BLUE, "Backend APIs 接口层",
              "/auth/loginV2\n/bus/aigcModel/models\n/bus/aigcSkills/skills\n/ai/chat/stream（SSE）")

    draw_card(draw, 510, 195, 405, 170, GREEN, LIGHT_GREEN, "SideMenu / HomeMenuItem 组件",
              "渲染对话历史列表\n切换已保存会话\n通过 getDialogueList() 加载历史记录")
    draw_card(draw, 510, 415, 405, 160, GREEN, LIGHT_GREEN, "ChatBox 输入组件",
              "自然语言输入框\n支持 Model 选择与 Skills 多选\nsendMsg(question) 发起一次任务")
    draw_card(draw, 510, 635, 405, 200, GREEN, LIGHT_GREEN, "ChatArea 展示组件",
              "渲染 Markdown 回答与任务卡片\n从历史记录中恢复任务快照\n提交 resume 载荷完成确认交互")
    draw_card(draw, 510, 900, 405, 180, GREEN, LIGHT_GREEN, "AguiTaskCard 任务组件",
              "展示状态、进度与阶段说明\n展示时间线日志、图表卡片与交互表单\n支持 Open In DataBoard 与 Submit resume")

    draw_card(draw, 1005, 180, 390, 190, ORANGE, LIGHT_ORANGE, "useChat 通信模块",
              "拉取模型与技能选项\nsendMsg() -> /ai/chat/stream\nfetchEventSource 持续消费 SSE\n统一别名事件并绑定 run_id / task_id")
    draw_card(draw, 1005, 445, 390, 190, ORANGE, LIGHT_ORANGE, "useChatStore 状态模块",
              "维护 dialogueId\n维护 chatMessages 与 toolCallMessages\n维护 aguiTasks\n维护 availableModels、selectedModel\n维护 availableSkills、selectedSkills")
    draw_card(draw, 1005, 715, 390, 205, ORANGE, LIGHT_ORANGE, "核心事件流",
              "chat_begin、status、tool_call、tool_result\nexec_begin、exec_output_delta、exec_end\ncall 或 ask -> resume\nchart -> Vega-Lite spec\n前后端通过 SSE 事件流持续同步任务状态")
    draw_card(draw, 1005, 980, 390, 140, ORANGE, LIGHT_ORANGE, "任务关联逻辑",
              "按 run_id、task_id、call_id 聚合\n将增量更新持续写入同一个 AguiTask")

    draw_card(draw, 1495, 180, 470, 145, PURPLE, LIGHT_PURPLE, "useDashboardStore 状态模块",
              "维护 spec、data、isPanelOpen、lastMessageId\nchart 事件直接写入 Data Board 状态")
    draw_card(draw, 1495, 405, 470, 170, PURPLE, LIGHT_PURPLE, "DashboardSidebar / DashboardPanel 组件",
              "可折叠的图表面板\n根据 chart spec 动态调整宽度\n承载完整图表结果区域")
    draw_card(draw, 1495, 650, 470, 160, PURPLE, LIGHT_PURPLE, "VegaLiteChart 图表组件",
              "直接消费 Vega-Lite spec\n通过 vega-embed 渲染图表\n保持可读宽度与横向滚动能力")
    draw_card(draw, 1495, 900, 470, 180, PURPLE, LIGHT_PURPLE, "用户可见输出",
              "答案区：Markdown 最终回答\n任务区：时间线与交互卡片\n图表区：Data Board 可视化结果")

    draw_arrow(draw, (390, 280), (510, 280), LINE_BLUE)
    draw_arrow(draw, (390, 480), (510, 480), LINE_BLUE)
    draw_arrow(draw, (390, 700), (510, 700), LINE_BLUE)

    draw_arrow(draw, (712, 365), (712, 415), LINE_GREEN)
    draw_arrow(draw, (915, 495), (1005, 495), LINE_GREEN)
    draw_arrow(draw, (915, 735), (1005, 735), LINE_GREEN)
    draw_arrow(draw, (805, 1080), (1120, 1110), LINE_GREEN)

    draw_arrow(draw, (1200, 370), (1200, 445), LINE_ORANGE)
    draw_arrow(draw, (1200, 635), (1200, 715), LINE_ORANGE)
    draw_arrow(draw, (1395, 275), (1495, 275), LINE_ORANGE)
    draw_arrow(draw, (1395, 540), (1495, 540), LINE_ORANGE)

    draw_arrow(draw, (1730, 325), (1730, 405), LINE_PURPLE)
    draw_arrow(draw, (1730, 575), (1730, 650), LINE_PURPLE)
    draw_arrow(draw, (1730, 810), (1730, 900), LINE_PURPLE)
    draw_arrow(draw, (1395, 835), (1495, 980), LINE_ORANGE)

    pts = [(915, 1005), (915, 1125), (2010, 1125), (2010, 540), (1965, 540)]
    for a, b in zip(pts, pts[1:]):
        if b == pts[-1]:
            draw_arrow(draw, a, b, LINE_PURPLE)
        else:
            draw.line((a[0], a[1], b[0], b[1]), fill=LINE_PURPLE, width=4)

    center_text(
        draw,
        (0, 1438, W, 1462),
        "依据 LoginPage、MainLayout、ChatPage、ChatBox、ChatArea、AguiTaskCard、useChat、useChatStore、useDashboardStore、DashboardSidebar 与 VegaLiteChart 整理",
        FOOT,
        TEXT_SUB,
    )

    img.save(OUT_PATH)
    print(OUT_PATH.resolve())


if __name__ == "__main__":
    main()
