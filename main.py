import qiniu_api
import time
import numpy as np

class Camera7niu(FlowBase):
    def __init__(self, app_setting_filename):
        super().__init__(None, app_setting_filename)

        self.app_key = self.app_setting.get_key('app_key')
        self.app_secret = self.app_setting.get_key('app_secret')
        self.stream_id = self.app_setting.get_key('stream_id')
        self.namespace_id = self.app_setting.get_key('namespace_id')
        gbid = self.stream_id
        brand = '未知'
        try:
            h, r = qiniu_api.listNamespacesInfo(self.app_key, self.app_secret, self.namespace_id, self.stream_id)
            brand = get_dict_key(r, 'vendor', default='不可用')
        except Exception as ex:
            exec(ERROR_PRINT)

        self.camera_info_for_next_stage = {
            'brand': brand,
            'model': 'Cloud',
            'camsn': self.stream_id,
            'fixsn': self.namespace_id,
            'name': get_app_title_without_html(self.app_setting, marker='_'),
            'sub_ext': '',
            'url': '',
            'extra': get_extra_dict(self.app_setting.get_key('extra'))
        }

    def close_camera(self):
        try:
            h, r = qiniu_api.stopDevice(self.app_key, self.app_secret, self.namespace_id, self.stream_id)
            if h['code'] == 200:
                self.log('正确关闭设备')
            else:
                self.log(f"关闭设备错误：{get_dict_key(h, 'text_body', default='未知错误')}")

            h, r = qiniu_api.stopStreams(self.app_key, self.app_secret, self.namespace_id, self.stream_id)
            if h['code'] == 200:
                self.log('正确关闭推流')
            else:
                self.log(f"关闭推流错误：{get_dict_key(h, 'text_body', default='未知错误')}")

        except Exception as ex:
            exec(ERROR_PRINT)

    def capture(self, customer):
        customer.send(None)
        # 使能流
        max_trial = 5
        wait_time = 2

        enable_stream_ok = False
        start_stream_ok = False
        goto_preset_ok = False
        cap_ok = False
        pic_ok = False

        start_cap_time = 0
        end_cap_time = 0

        rtmp_url = ''

        for try_time in range(max_trial):
            try:
                h, r = qiniu_api.enableStreams(self.app_key, self.app_secret, self.namespace_id, self.stream_id)
                if h['code'] != 200:
                    self.log(f"使能流错误：{get_dict_key(h, 'text_body', default='未知错误')}")
                    time.sleep(wait_time)
                else:
                    self.log(f"已经使能推流")
                    enable_stream_ok = True
                    break
            except Exception as ex:
                exec(ERROR_PRINT)

        # 启动设备
        if enable_stream_ok:
            for try_time in range(max_trial):
                try:
                    h, r = qiniu_api.startDevice(self.app_key, self.app_secret, self.namespace_id, self.stream_id)
                    if h['code'] != 200:
                        self.log(f"设备启动错误：{get_dict_key(h, 'text_body', default='未知错误')}")
                        time.sleep(wait_time)
                    else:
                        self.log(f"已经打开设备")
                        start_stream_ok = True
                        break
                except Exception as ex:
                    exec(ERROR_PRINT)

        # 回预置点
        if start_stream_ok:
            for try_time in range(max_trial):
                try:
                    h, r = qiniu_api.controlPresetBit(self.app_key, self.app_secret, self.namespace_id, self.stream_id,
                                                      {'cmd': 'goto', 'name': '预置点1', 'presetId': 1})
                    if h['code'] != 200:
                        self.log(f"回预置点错误：{get_dict_key(h, 'text_body', default='未知错误')}")
                        time.sleep(wait_time)
                    else:
                        self.log(f"相机回到预置点")
                        goto_preset_ok = True
                        time.sleep(wait_time * 2)
                        break
                except Exception as ex:
                    exec(ERROR_PRINT)

        # 截图
        if goto_preset_ok:
            # start_cap_time = int(time.time() - 2)
            for try_time in range(max_trial):
                try:
                    h, r = qiniu_api.getStreamUrl(self.app_key, self.app_secret, self.namespace_id, self.stream_id)
                    if h['code'] != 200:
                        self.log(f"获取URL失败：{get_dict_key(h, 'text_body', default='未知错误')}")
                        time.sleep(wait_time)
                    else:
                        rtmp_url = get_dict_key(r, 'playUrls.hls', default='')
                        if rtmp_url != '':
                            cap_ok = True
                            self.log(f"获取图像地址")
                            break
                        else:
                            self.log(f"获取URL失败：没有获取到URL", GREEN)

                except Exception as ex:
                    exec(ERROR_PRINT)

        # 获取图像列表和获取图像
        if cap_ok and rtmp_url != '':
            for try_time in range(max_trial):
                try:
                    # print(rtmp_url)
                    cap = cv.VideoCapture(rtmp_url)
                    while cap.isOpened() is False and time.time() - start_cap_time < wait_time * max_trial:
                        time.sleep(0.1)

                    if cap.isOpened() is False:
                        # 图像获取存在问题, 继续获取下一张图
                        self.log('图像地址无法打开', RED)
                        continue
                    is_ok, frame = cap.read()
                    if is_ok is False:
                        continue
                    while self.is_empty_image(frame) and time.time() - start_cap_time < wait_time * max_trial:
                        is_ok, frame = cap.read()

                    if self.is_empty_image(frame) is True:
                        self.log('图像获取但是内容为空白', RED)
                        continue
                    else:
                        self.log('图像正确获取！', GREEN)
                        self.image = frame
                        customer.send([self.camera_info_for_next_stage, {ORI_IMG: self.image}])
                        break
                except Exception as ex:
                    exec(ERROR_PRINT)

        self.close_camera()

    def run(self):
        customer = self.next_stage()
        self.capture(customer)

    def is_empty_image(frame):
        try:
            frame = cv.resize(frame, (1280, 720))
            frame_64 = frame.astype(np.int64)
            avg_0, avg_1, avg_2 = int(sum(sum(frame_64[:, :, 0]) / (1280 * 720))), \
                                  int(sum(sum(frame_64[:, :, 1])) / (1280 * 720)), \
                                  int(sum(sum(frame_64[:, :, 2])) / (1280 * 720))
    
            diff_0, diff_1, diff_2 = int(
                sum(sum(abs(frame_64[:, :, 0] - avg_0))) / (1280 * 720)), \
                                     int(sum(sum(abs(frame_64[:, :, 1] - avg_1))) / (
                                             1280 * 720)), \
                                     int(sum(sum(abs(frame_64[:, :, 2] - avg_2))) / (
                                             1280 * 720))
    
            if diff_0 + diff_1 + diff_2 < 32:
                return True
            else:
                return False
        except:
            return True
if __name__ == '__main__':
    Camera7niu()