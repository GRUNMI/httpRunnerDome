遍历循环取值
"postid2":"${get_postids(5)}"
只取第一个值
"postid2":"$[{get_postids(5)}]"


JSON格式检测

    作用：检测JSON格式的正确性
    关键字：validate
    格式：hrun --validate test.json
    说明：其中test.json为json格式的文件名，并且可一次性指定多个文件


JSON格式美化

    作用：美化JSON的格式，使得测试脚本便于维护和阅读
    关键字：prettify
    格式：hrun --prettify test.json
    说明：其中test.json为json格式的文件名，并且可一次性指定多个文件

抓包工具录制结果
将har文件进行转换
cmd命令：
>>>  har2case kauidi.har  kuaidi.json
>>>  har2case kauidi.har  kuaidi.yml 【准换成YAML格式用例】
这样就可以把har格式的转换为json格式的用例



httprunner的用例模板。

1. 用例用[{"config":{}},"test":{}}]格式。

2. config 为全局配置变量

name
required
格式：string
测试用例集的名称，在测试报告中将作为标题
variables
optional
格式：list of dict
定义的全局变量，作用域为整个用例集
parameters
optional
格式：list of dict
全局参数，用于实现数据化驱动，作用域为整个用例集
request
optional
格式：dict of dict
request 的公共参数，作用域为整个用例集
常用参数包括 base_url 和 headers
base_url
optional
格式：string
测试用例集请求 URL 的公共 host，指定该参数后，test 中的 url 可以只描述 path 部分
headers
optional
格式：dict of dict
request 中 headers 的公共参数，作用域为整个用例集
output
optional
格式：list of string
整个用例集输出的参数列表，可输出的参数包括公共的 variable 和 extract 的参数
在 log-level 为 debug 模式下，会在 terminal 中打印出参数内容
3. Test用例参数
name
required
格式：string
测试用例的名称，在测试报告中将作为每一项测试的标题

request
required
格式：dict of dict
HTTP 请求的详细内容
可用参数详见 python-requests 官方文档

variables
optional
格式：list of dict
测试用例中定义的变量，作用域为当前测试用例

parameters
optional
格式：list of dict
测试用例中定义的参数列表，作用域为当前测试用例，用于实现对当前测试用例进行数据化驱动

extract
optional
格式：list of dict
从当前 HTTP 请求的响应结果中提取参数，并保存到参数变量中（例如token），后续测试用例可通过$token的形式进行引用
支持多种提取方式
响应结果为 JSON 结构，可采用.运算符的方式，例如headers.Content-Type、content.success；
响应结果为 text/html 结构，可采用正则表达式的方式，例如blog-motto\">(.*)</h2>
详情可阅读《ApiTestEngine，不再局限于API的测试》

validate
optional
格式：list of dict
测试用例中定义的结果校验项，作用域为当前测试用例，用于实现对当前测试用例运行结果的校验
支持两种格式：
{"comparator_name": [check_item, expect_value]}
{"check": check_item, "comparator": comparator_name, "expect": expect_value}

setup_hooks
optional
格式：list of string
在 HTTP 请求发送前执行 hook 函数，主要用于准备工作
hook 函数放置于 debugtalk.py 中，并且必须包含三个参数：
method: 请求方法，e.g. GET, POST, PUT
url: 请求 URL
kwargs: request 的参数字典

teardown_hooks
optional
格式：list of string
在 HTTP 请求发送后执行 hook 函数，主要用户测试后的清理工作
hook 函数放置于 debugtalk.py 中，并且必须包含一个参数：
resp_obj: requests.Response 实例

    [
        {
            "config": {
                "name": "testset description",
                "variables": [
                    {"device_sn": "${gen_random_string(15)}"},
                    {"user_id": 1000}
                ],
                "parameters": [
                    {"user_id": [2001, 2002, 2003, 2004]}
                ],
                "request": {
                    "base_url": "http://172.16.78.72:8301/",
                    "headers": {
                        "User-Agent": "python-requests/2.18.4",
                        "device_sn": "$device_sn",
                        "Content-Type": "application/json"
                    }
                },
                "output":["token"]
            }
        },
        {
            "test": {
                "name": "login and get token",
                "variables":[],
                "request": {
                    "url": "v1/chameleon-user/user/login",
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "method": "POST",
                    "json": {
                        "account":"admin",
                        "password":"zs123YL!"
                    }
                },
                "json":{},
                "extract": [
                    {"token": "content.token"}
                ],
                "validate": [
                    {"eq": ["status_code", 200]},
                    {"eq": ["headers.Content-Type", "application/json;charset=UTF-8"]}
                ],
                "setup_hooks":[],
                "teardown_hooks":[]
            }
        }
    ]