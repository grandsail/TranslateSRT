"""
使用有道词典API对SRT文件进行中->英和英->中翻译
使用前要安装python和pysrt插件
"""
import json
import pysrt
import requests

# 翻译函数，word 需要翻译的内容
def translate(word):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        return response.text
    else:
        print("有道词典调用失败")
        return None

# 获得翻译结果
def get_reuslt(repsonse):
    #
    result = json.loads(repsonse)
    return result['translateResult'][0][0]['tgt']


def main():
    print("输入你想要翻译的SRT文件名称")
    input_file_name = input("如 test.srt 名称为 test\n")
    try:
        subs = pysrt.open(input_file_name+'.srt')
    except:
        print("打开文件失败，请输入本文件夹下正确的SRT文件名")
        return 0
    for line in subs:
        print(line.text)
        # 在此可以添加对每句话的操作，如去掉末尾句号
        list_trans = translate(line.text)
        line.text = get_reuslt(list_trans)
    subs.save('export.srt', encoding='utf-8')


if __name__ == '__main__':
    main()
