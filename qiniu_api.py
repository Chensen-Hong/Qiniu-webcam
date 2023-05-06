import time
from qiniu import QiniuMacAuth, http, Auth
import json
import urllib.request
import cv2 as cv

# 查询设备信息
def listNamespacesInfo(access_key, secret_key, namespaceId, gbId):
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/devices/{gbId}"
    # 发起POST请求
    ret, res = http._get_with_qiniu_mac(url, params=None, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


#  启用流
def enableStreams(access_key, secret_key, namespaceId, streamId):
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/streams/{streamId}/enabled"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, None, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


# 禁用流
def stopStreams(access_key, secret_key, namespaceId, streamId):
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/streams/{streamId}/stop"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, None, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


# 启动设备拉流
def startDevice(access_key, secret_key, namespaceId, gbId):
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/devices/{gbId}/start"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, None, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


def getStreamUrl(access_key, secret_key, namespaceId, gbId):
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/streams/{gbId}/urls"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, {'playIp': '127.0.0.1'}, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


# 停止设备拉流
def stopDevice(access_key, secret_key, namespaceId, gbId):
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/devices/{gbId}/stop"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, None, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


# 按需截图
def takeScreenshot(access_key, secret_key, namespaceId, streamId):
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/streams/{streamId}/snap"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, None, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


# 变焦控制 - 清晰度
def controlZooming(access_key, secret_key, namespaceId, gbId, body):
    '''

    Args:
        body: {
                cmd：focusnear(焦距变近), focusfar(焦距变远),stop(停止)，
                speed：调节速度(1~10, 默认位5)
            }
    '''
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/devices/{gbId}/focus"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, body, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


# 光圈控制 - 亮度
def controlDiaphragm(access_key, secret_key, namespaceId, gbId, body):
    '''
    Args:
        body: {
                cmd：irisin(光圈变小), irisout(光圈变大),stop(停止)，
                speed：调节速度(1~10, 默认位5)
            }
    '''
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/devices/{gbId}/iris"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, body, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


# 云台控制
def controlConsole(access_key, secret_key, namespaceId, gbId, body):
    '''
    Args:
        body: {
                cmd：left(向左), right(向右), up(向上), down(向下), leftup(左上), rightup(右上), leftdown(左下),
                    rightdown(右下), zoomin(放大), zoomout(缩小),stop(停止PTZ操作)

                speed：调节速度(1~10, 默认位5)
            }
    '''
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/devices/{gbId}/ptz"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, body, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


# 预置位控制
def controlPresetBit(access_key, secret_key, namespaceId, gbId, body):
    '''
    Args:
        body: {
                cmd：set(新增预置位), goto(设置),remove(删除)
                name：预置位名称(cmd为set时有效,支持中文)
                presetId：预置位ID(cmd为goto,remove 时必须指定)
            }
    '''
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/devices/{gbId}/presets"
    # 发起POST请求
    ret, res = http._post_with_qiniu_mac(url, body, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


# 获取预置位列表
def listPresets(access_key, secret_key, namespaceId, gbId):
    auth = QiniuMacAuth(access_key, secret_key)
    # 请求URL
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/devices/{gbId}/presets"

    # 发起POST请求
    ret, res = http._get_with_qiniu_mac(url, params=None, auth=auth)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, ret


def listSnapshots(access_key, secret_key, namespaceId, streamId, line, marker, start, end):
    '''
        参数名称	必填	字段类型	说明
        type	是	integer	1:实时截图对应的图片列表 2: 按需截图对应的图片列表 3:覆盖式截图对应的图片
        line	否	integer	限定返回截图的个数，只能输入1-100的整数，不指定默认返回30个，type为3可忽略
        marker	否	string	上一次查询返回的标记，用于提示服务端从上一次查到的位置继续查询，不指定表示从头查询，type为3可忽略
        start	否	integer	查询开始时间(unix时间戳,单位为秒)，type为3可忽略
        end	    否	integer	查询结束时间(unix时间戳,单位秒)，type为3可忽略
    '''
    auth = QiniuMacAuth(access_key, secret_key)
    # print(access_key,secret_key,namespaceId,streamId,line,marker,start,end)
    # 请求URL
    # url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/streams/{streamId}/snapshots?type=2&start={start}&end={end}&marker={marker}&line={line}"
    url = f"http://qvs.qiniuapi.com/v1/namespaces/{namespaceId}/streams/{streamId}/snapshots?type=2&line={line}&start={start}&end={end}"
    # print(url)

    # 发起POST请求
    result, res = http._get_with_qiniu_mac(url, params=None, auth=auth)
    # print(res)
    headers = {"code": res.status_code, "reqid": res.req_id, "xlog": res.x_log, "text_body": res.text_body}
    # 格式化响应体
    # Headers = json.dumps(headers, indent=4, ensure_ascii=False)
    # result = json.dumps(ret, indent=4, ensure_ascii=False)
    return headers, json.loads(res.text_body)


def download_snapshots(access_key, secret_key, base_url, filepath):
    q = Auth(access_key, secret_key)
    # 有两种方式构造base_url的形式
    # base_url = 'http://%s/%s' % ("rfpxt0t4s.hd-bkt.clouddn.com", "")
    # 或者直接输入url的方式下载
    # base_url = 'http://domain/key'
    # 可以设置token过期时间
    private_url = q.private_download_url(base_url, expires=3600)
    urllib.request.urlretrieve(private_url, filepath)
    print("下载成功：" + filepath[filepath.rfind('\\')+1:])
    # r = requests.get(private_url)


def play_snapshots(access_key, secret_key, namespaceId, streamId):
    count = 0
    while True:
        t1 = int(time.time() - 2)
        for i in range(10):
            h, r = takeScreenshot(access_key, secret_key, namespaceId, streamId)
        time.sleep(2)
        t2 = int(time.time())

        while count < 10:
            h, r = listSnapshots(access_key, secret_key, namespaceId, streamId, 100, None, t1, t2)
            for item in r['items']:
                download_snapshots(access_key, secret_key, item['snap'], './snapshot')
                img = cv.imread('./snapshot')
                if img is not None:
                    cv.imshow('window name', img)
                    cv.resizeWindow('window name', 800, 600)
                    if cv.getWindowProperty('window name', cv.WND_PROP_VISIBLE) < 0:
                        cv.namedWindow('window name', cv.WINDOW_NORMAL)
                        cv.resizeWindow('window name', 800, 600)
                    cv.waitKey(10)
                    count += 1
            time.sleep(1)
            print(time.time() - t2)
        count = 0


def start(access_key, secret_key, namespaceId, streamId):
    # app_key = 'RofRgvw0K2egvDxKz7n75RJCH_R49e-hQLk_z1kk'
    # app_sec = 'dMj5nG4ybGwzynCeoqopytKmsN2QDzg1QVnUF277'
    # stm_id = '31011500991320020843'
    # ns_id = 'qvs'

    try:
        play_snapshots(access_key, secret_key, namespaceId, streamId)
    except KeyboardInterrupt:
        stopStreams(access_key, secret_key, namespaceId, streamId)


# if __name__ == '__main__':
#     start()








