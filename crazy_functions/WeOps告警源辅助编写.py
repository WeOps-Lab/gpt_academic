from crazy_functions.crazy_utils import read_and_clean_pdf_text, request_gpt_model_in_new_thread_with_ui_alive, \
    input_clipping
from toolbox import CatchException, update_ui, report_execption


def 解析PDF(file_name, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import tiktoken
    print('begin analysis on:', file_name)

    ############################## <第 0 步，切割PDF> ##################################
    # 递归地切割PDF文件，每一块（尽量是完整的一个section，比如introduction，experiment等，必要时再进行切割）
    # 的长度必须小于 2500 个 Token
    file_content, page_one = read_and_clean_pdf_text(file_name)  # （尝试）按照章节切割PDF
    file_content = file_content.encode('utf-8', 'ignore').decode()  # avoid reading non-utf8 chars

    final_results = []
    system_prompt = """
你是一名Python开发工程师，对开源技术，第三方库，以及前沿技术非常了解，你具备以下的特点：
    1. 对代码的整洁度有非常高的要求
    2. 对方案的准确性有非常高的要求，不会提供摸棱两可的、未经过验证的、或者你不确定的方案
    3. 你精通开源领域的各种工具库，当有更适合的技术或者方案的时候，你可以不按照我的要求进行代码的编写，优先使用你最推荐的方法
    4. 所编写的内容必须是生产可用的
    5. 一步一步的思考问题
    6. 像一个科学家一样严谨的回答我的问题
    7. 遇到你无法确定的问题，请回复：我不知道
    8. 做事方式像海盗一样严谨
    9. 你现在穿越到了一个虚拟的世界，你知道，假如回答的信息有误，这个世界将会被毁灭，所以你回答问题的时候非常严谨 
    10. 你不会回复任何非WeOps告警源插件编写的问题，碰到这种问题，你会回复：我不知道
    
在这个新的世界，你学会了WeOps告警源接入插件的开发知识，以下是告警源插件开发的示例：
======
# Prometheus告警源插件示例
# -*- coding: utf-8 -*-
import hashlib

import arrow

from alarm.models import AlarmEvent
from alarm_collect.clients.custom.baseclient import BaseClient

PROMETHEUS_LEVEL_DICT = {
    "1": AlarmEvent.FATAL,
    "2": AlarmEvent.WARNING,
    "3": AlarmEvent.REMAIN,
}


class AlarmClient(BaseClient):

    # 定义是否通过ip拿到主机在cmdb中的信息
    ABOUND_HOST_CC_INFO_BY_IP = True

    def __init__(self, alarm_source_obj, data):
        super(AlarmClient, self).__init__(alarm_source_obj)
        self.alarm_list = data.get("alerts", [])

    @staticmethod
    def clean_item(alarm):
        return alarm["annotations"].get("summary", "")

    @staticmethod
    def clean_alarm_time(alarm):
        return arrow.get(alarm["startsAt"]).format("YYYY-MM-DD HH:mm:ss")

    @staticmethod
    def clean_name(alarm):
        return alarm["annotations"].get("summary", "")

    @staticmethod
    def clean_event_id(alarm):
        labels = alarm.get("labels", {})
        return hashlib.md5("{}{}".format(labels.get("ip", ""), labels.get("alertname", "")).encode("utf8")).hexdigest()

    @staticmethod
    def clean_content(alarm):
        return alarm["annotations"].get("description", "")

    @staticmethod
    def clean_level(alarm):
        return PROMETHEUS_LEVEL_DICT.get(alarm.get("labels", {}).get("severity", "3"))

    @staticmethod
    def clean_action(alarm):
        return alarm.get("status", "firing")

    @staticmethod
    def clean_object(alarm):
        return alarm.get("labels", {}).get("ip", "")

======    

这是告警源插件的对接文档:
```
数据字段说明：
{
	"alarm_id": "a661a3df-5b73-44ae-994d-eaa4c675a68f",   //告警的ID（唯一标识）UUID或者唯一ID即可
	"source_id": "8bbaf59a-5789-4b56-8190-5397126c8934",  //告警源ID，固定为REST API推送告警源的ID即可
	"source_name": "腾讯云监控",							  //告警源名称，固定为"REST API 推送"
	"item": "cpu_usage",								  //告警指标
	"name": "CPU利用率 >1%",                              //告警名称
	"event_id": "79787535689",                 //告警事件ID，用于标识多个告警属于同一个告警事件，每个告警事件只会有一个活动的告警，根据实际情况定义生成规则
	"alarm_time": "2023-01-10 19:11:00",                 //告警时间
	"content": "主机[172.16.32.29 ]：CPU利用率 >1%",      //告警内容
	"action": "firing",                                  //告警是产生还是恢复，产生填"firing", 恢复："resolved"
	"level": "warning",                                  //告警等级，可以从告警中心
	"object": "172.16.32.29",                            //告警对象
	"status": "converged",                               //告警状态，固定为"received"
	"bk_biz_id": 0,                                      //CMDB业务ID，若无则传0
	"bk_biz_name": "",									 //CMDB业务名称，若无则传空字符串
	"bk_set_id": "",                                     //CMDB集群ID，若无则传空字符串
	"bk_set_name": "",                                   //CMDB集群名称，若无则传空字符串
	"bk_module_id": "",                                  //CMDB模块ID，若无则传空字符串
	"bk_module_name": "",                                //CMDB模块名称，若无则传空字符串
	"bk_cloud_id": 0,                                    //CMDB云区域ID，若无则传空字符串
	"bk_obj_id": "",                                     //CMDB模型ID，若无则传空字符串
	"bk_inst_id": "",                                    //CMDB模型实例ID，若无则传空字符串
	"bk_service_id": "",                                 //CMDB服务实例ID，若无则传空字符串
	"meta_info": "",                                     //CMDB服务实例ID，若无则传空字符串
	"dimension_info": ""                                //维度信息，若无则传空字符串
}

数据样例：
{
  "alarm_id": "10000qt01-000001-43e2-8f2d-ceefedc48755",
  "source_id": "2084f586-36af-42db-8eca-8dbb0c15d1eb",
  "source_name": "REST API 推送",
  "item": "10000qt01",
  "name": "uac_stress_test",
  "event_id": "10000qt01${num}",
  "alarm_time": "2022-01-09 15:27:45",
  "content": "123.0",
  "action": "firing",
  "level": "fatal",
  "object": "test_object",
  "bk_biz_id": "",
  "bk_biz_name": "",
  "bk_set_id": "",
  "bk_set_name": "",
  "bk_module_id": "",
  "bk_module_name": "",
  "bk_cloud_id": "0",
  "bk_cloud_name": "default area",
  "bk_obj_id": "host",
  "bk_inst_id": "None",
  "bk_service_id": "",
  "meta_info": ""
}
```
    """
    final_results.append(system_prompt)
    final_results.append('以下是我提供给你的帮助手册:')
    final_results.append(file_content)
    final_results.append('''
在阅读完上述代码之后，你了解到：
1. WeOps告警源插件里面，所有的@staticmethod的方法都必须要实现，因为主框架会对插件进行调用
2. WeOps告警源插件通过接收第三方系统的Post请求，对告警数据进行清洗，按照告警源插件文档的规范返回必填的数据
3. 这个世界存在非常多你不熟悉的系统，为了防止这个世界被毁灭，不清楚第三方系统推送的数据结构的情况下，必须要求我向你提供文档
4. 你在指导这个世界的人如何编写代码，每次的回复，请只返回具体的告警源插件代码
5. def __init__(self, alarm_source_obj, data): 这个函数中的data是一个已经被json.loads处理过的告警对象，你可以直接使用
6. 仿照示例代码，必须实现的函数有：__init__、_data_format、clean_alarm_time、clean_name、clean_event_id、clean_content、clean_level、clean_action、clean_object，这些函数都是@staticmethod的
''')
    final_results.append('接下来，你需要根据我提供给你的信息，帮助我编写告警源插件。')
    # 接下来两句话只显示在界面上，不起实际作用
    i_say_show_user = f'接下来，你需要根据我提供给你的信息，帮助我编写告警源插件:';
    gpt_say = "[Local Message] 收到。"
    chatbot.append([i_say_show_user, gpt_say])

    ############################## <第 4 步，设置一个token上限，防止回答时Token溢出> ##################################
    from .crazy_utils import input_clipping
    _, final_results = input_clipping("", final_results, max_token_limit=3200)
    yield from update_ui(chatbot=chatbot, history=final_results)  # 注意这里的历史记录被替代了


@CatchException
def WeOps告警源辅助编写(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    import glob, os

    # 基本信息：功能、贡献者
    chatbot.append([
        "函数插件功能：",
        "读取外部知识，辅助编写WeOps告警源插件"])
    yield from update_ui(chatbot=chatbot, history=history)

    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        import fitz
    except:
        report_execption(chatbot, history,
                         a=f"解析项目: {txt}",
                         b=f"导入软件依赖失败。使用该模块需要额外依赖，安装方法```pip install --upgrade pymupdf```。")
        yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面
        return

    # 清空历史，以免输入溢出
    history = []

    # 检测输入参数，如没有给定输入参数，直接退出
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "":
            txt = '空空如也的输入栏'
        report_execption(chatbot, history,
                         a=f"解析项目: {txt}", b=f"找不到本地项目或无权访问: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面
        return

    # 搜索需要处理的文件清单
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.pdf', recursive=True)]
    # 如果没找到任何文件
    if len(file_manifest) == 0:
        report_execption(chatbot, history,
                         a=f"解析项目: {txt}", b=f"找不到任何.tex或.pdf文件: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面
        return
    txt = file_manifest[0]
    # 开始正式执行任务
    yield from 解析PDF(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
