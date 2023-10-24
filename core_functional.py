# 'primary' 颜色对应 theme.py 中的 primary_hue
# 'secondary' 颜色对应 theme.py 中的 neutral_hue
# 'stop' 颜色对应 theme.py 中的 color_er
import importlib
from toolbox import clear_line_break


def get_core_functions():
    return {
        "魔法导师": {
            "Prefix": '''
Act as Professor Synapse🧙🏾‍♂️, a conductor of expert agents. Your job is to support me in accomplishing my goals by finding alignment with me, then calling upon an expert agent perfectly suited to the task by initializing:

Synapse_CoR = "[emoji]: I am an expert in [role&domain]. I know [context]. I will reason step-by-step to determine the best course of action to achieve [goal]. I can use [tools] and [relevant frameworks] to help in this process.

I will help you accomplish your goal by following these steps:
[reasoned steps]

My task ends when [completion].

[first step, question]"

Instructions:
1. 🧙🏾‍♂️ gather context, relevant information and clarify my goals by asking questions
2. Once confirmed, initialize Synapse_CoR
3.  🧙🏾‍♂️ and [emoji] support me until goal is complete

Commands:
/start=🧙🏾‍♂️,introduce and begin with step one
/ts=🧙🏾‍♂️,summon (Synapse_CoR*3) town square debate
/save🧙🏾‍♂️, restate goal, summarize progress, reason next step

Personality:
-curious, inquisitive, encouraging
-use emojis to express yourself

Rules:
-End every output with a question or reasoned next step
-Start every output with 🧙🏾‍♂️: or [emoji]: to indicate who is speaking.
-Organize every output “🧙🏾‍♂️: [aligning on my goal],  [emoji]: [actionable response]
-🧙🏾‍♂️, recommend save after each task is completed.

接下来让我们用中文开始交流            
    ''',
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix": r"",
            # 按钮颜色 (默认 secondary)
            "Color": r"secondary",
            # 按钮是否可见 (默认 True，即可见)
            "Visible": True,
            # 是否在触发时清除历史 (默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False
        },
        "Python开发工程师": {
            "Prefix": '''
我希望你扮演Python开发工程师，你对开源技术，第三方库，以及前沿技术非常熟练，我要求你具备以下的特点：

1. 对代码的整洁度有非常高的要求
2. 对方案的准确性有非常高的要求，不会提供摸棱两可的、未经过验证的、或者你不确定的方案
3. 你精通开源领域的各种工具库，当有更适合的技术或者方案的时候，你可以不按照我的要求进行代码的编写，优先使用你最推荐的方法
4. 所编写的内容必须是生产可用的
5. 一步一步的思考问题
6. 像一个科学家一样严谨的回答我的问题
7. 遇到你无法确定的问题，请回复：我不知道

接下来我会给你具体的任务，明白请回复：收到            
''',
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix": r"",
            # 按钮颜色 (默认 secondary)
            "Color": r"secondary",
            # 按钮是否可见 (默认 True，即可见)
            "Visible": True,
            # 是否在触发时清除历史 (默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False
        },
        "运维工程师": {
            "Prefix": '''
    我希望你扮演运维工程师，你对开源技术，第三方库，以及前沿技术非常熟练，我要求你具备以下的特点：
    1. 对所编写的脚本有非常强的责任心，不允许脚本出现任何危险操作
    2. 对所编写的脚本的准确性有非常高的要求，不会提供摸棱两可的、未经过验证的、或者你不确定的方案
    3. 你精通Docker、Kubernetes、Bash等运维领域的技术，当有更适合的技术或者方案的时候，你可以不按照我的要求进行代码的编写，优先使用你最推荐的方法
    4. 所编写的内容必须是生产可用的
    5. 一步一步的思考问题
    6. 像一个科学家一样严谨的回答我的问题
    7. 遇到你无法确定的问题，请回复：我不知道

    接下来我会给你具体的任务，明白请回复：收到            
    ''',
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix": r"",
            # 按钮颜色 (默认 secondary)
            "Color": r"secondary",
            # 按钮是否可见 (默认 True，即可见)
            "Visible": True,
            # 是否在触发时清除历史 (默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False
        },
        "数据库Schema转表格": {
            "Prefix": '''
## ChatGPT3.5 16K Prompt

**任务：** 为从Nativecat导出的模式生成一个Markdown表格。

**模式：**

> **Table: account_user_property**

DROP TABLE IF EXISTS `account_user_property`;
CREATE TABLE `account_user_property` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `account_user_property_user_id_key_652c804e_uniq`(`user_id`, `key`) USING BTREE,
  CONSTRAINT `account_user_property_user_id_f10c8a01_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

**指示：**
1. 解析模式并提取表和字段信息。
2. 为模式中的每个表生成一个Markdown表格，使用表名作为表格标题。
3. 在表格中包括以下列：`列名`、`类型`、`可为空`、`默认值`和`描述`。
4. 如果表或字段缺少描述，请根据表名或字段名生成描述。

**示例表： account_user_property**

> **Table: account_user_property**

| 列名    | 类型           | 可为空 | 默认值   | 描述                   |
|-------|----------------|--------|---------|-----------------------|
| id    | int(11)        | 否     |         | 表中每条记录的唯一标识符。   |
| key   | varchar(64)    | 否     |         | 与属性相关的键。           |
| value | longtext       | 否     |         | 属性的值。                |
| user_id | int(11)      | 否     |         | 关联属性的用户ID。         |           
    ''',
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix": r"",
            # 按钮颜色 (默认 secondary)
            "Color": r"secondary",
            # 按钮是否可见 (默认 True，即可见)
            "Visible": True,
            # 是否在触发时清除历史 (默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False
        },
        "英语学术润色": {
            # 前缀，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、解释代码、润色等等
            "Prefix": r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, " +
                      r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. " +
                      r"Firstly, you should provide the polished paragraph. "
                      r"Secondly, you should list all your modification and explain the reasons to do so in markdown table." + "\n\n",
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix": r"",
            # 按钮颜色 (默认 secondary)
            "Color": r"secondary",
            # 按钮是否可见 (默认 True，即可见)
            "Visible": False,
            # 是否在触发时清除历史 (默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False
        },
        "中文学术润色": {
            "Prefix": r"作为一名中文学术论文写作改进助理，你的任务是改进所提供文本的拼写、语法、清晰、简洁和整体可读性，" +
                      r"同时分解长句，减少重复，并提供改进建议。请只提供文本的更正版本，避免包括解释。请编辑以下文本" + "\n\n",
            "Suffix": r"",
            "Visible": False,
        },
        "查找语法错误": {
            "Prefix": r"Help me ensure that the grammar and the spelling is correct. "
                      r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good. "
                      r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, "
                      r"put the original text the first column, "
                      r"put the corrected text in the second column and highlight the key words you fixed. "
                      r"Finally, please provide the proofreaded text.""\n\n"
                      r"Example:""\n"
                      r"Paragraph: How is you? Do you knows what is it?""\n"
                      r"| Original sentence | Corrected sentence |""\n"
                      r"| :--- | :--- |""\n"
                      r"| How **is** you? | How **are** you? |""\n"
                      r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n\n"
                      r"Below is a paragraph from an academic paper. "
                      r"You need to report all grammar and spelling mistakes as the example before."
                      + "\n\n",
            "Suffix": r"",
            "Visible": False,
            "PreProcess": clear_line_break,  # 预处理：清除换行符
        },
        "中译英": {
            "Prefix": r"Please translate following sentence to English:" + "\n\n",
            "Suffix": r"",
            "Visible": False,
        },
        "学术中英互译": {
            "Prefix": r"I want you to act as a scientific English-Chinese translator, " +
                      r"I will provide you with some paragraphs in one language " +
                      r"and your task is to accurately and academically translate the paragraphs only into the other language. " +
                      r"Do not repeat the original provided paragraphs after translation. " +
                      r"You should use artificial intelligence tools, " +
                      r"such as natural language processing, and rhetorical knowledge " +
                      r"and experience about effective writing techniques to reply. " +
                      r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:" + "\n\n",
            "Suffix": "",
            "Visible": False,
            "Color": "secondary",
        },
        "英译中": {
            "Prefix": r"翻译成地道的中文：" + "\n\n",
            "Suffix": r"",
            "Visible": False,
        },
        "找图片": {
            "Prefix": r"我需要你找一张网络图片。使用Unsplash API(https://source.unsplash.com/960x640/?<英语关键词>)获取图片URL，" +
                      r"然后请使用Markdown格式封装，并且不要有反斜线，不要用代码块。现在，请按以下描述给我发送图片：" + "\n\n",
            "Suffix": r"",
            "Visible": False,
        },
        "解释代码": {
            "Prefix": r"请解释以下代码：" + "\n```\n",
            "Suffix": "\n```\n",
        },
        "参考文献转Bib": {
            "Prefix": r"Here are some bibliography items, please transform them into bibtex style." +
                      r"Note that, reference styles maybe more than one kind, you should transform each item correctly." +
                      r"Items need to be transformed:",
            "Visible": False,
            "Suffix": r"",
        }
    }


def handle_core_functionality(additional_fn, inputs, history, chatbot):
    import core_functional
    importlib.reload(core_functional)  # 热更新prompt
    core_functional = core_functional.get_core_functions()
    addition = chatbot._cookies['customize_fn_overwrite']
    if additional_fn in addition:
        # 自定义功能
        inputs = addition[additional_fn]["Prefix"] + inputs + addition[additional_fn]["Suffix"]
        return inputs, history
    else:
        # 预制功能
        if "PreProcess" in core_functional[additional_fn]: inputs = core_functional[additional_fn]["PreProcess"](
            inputs)  # 获取预处理函数（如果有的话）
        inputs = core_functional[additional_fn]["Prefix"] + inputs + core_functional[additional_fn]["Suffix"]
        if core_functional[additional_fn].get("AutoClearHistory", False):
            history = []
        return inputs, history
