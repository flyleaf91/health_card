import os,time,re,json,logging,csv,copy,zxing,shutil
from threading import Thread
from card import Card

class Heshuan(Card):
   
    def __init__(self,img_path="核酸结果/",result_file="核酸结果解码信息.csv"):
        Card.__init__(self,img_path,result_file)

        self.catch_sum = {'img_name':None,
                'card': None, 
                'name': None,
                'sample': None, 
                'test': None, 
                'agency': None,
                'result':None,
                'text':None}
        self.header = ["图片原文件路径","行程卡","是否为绿色行程卡","手机号","行程卡更新时间","途经城市","是否带*","识别文字"]

    def get_pattern(self,text,try_others=False):
        
        pattern = None
        
        if "粤康码" in text:
            #粤康码信息匹配模式 
            pattern = re.compile(""".*?(?P<card>粤康码信息)|"""
                                 """[oO0]?(?P<name>.*?)[a-zA-Z0-9\*/]*核酸检测记录|"""
                                 """采样时间(?P<sample>(19|20)[0-9]{2}.?(0?[1-9]|1[012]).?(0?[1-9]|[12][0-9]|3[01])?[0-9]{2}.?[0-9]{2}.?[0-9]{2})|"""
                                 """检测时间(?P<test>(19|20)[0-9]{2}.?(0?[1-9]|1[012]).?(0?[1-9]|[12][0-9]|3[01])?[0-9]{2}.?[0-9]{2}.?[0-9]{2})|"""
                                 """检测机构(?P<agency>.*?)检测|"""
                                 """结果(?P<result>[阴阳]性)"""
                                )
        else:
            #核酸检测记录匹配模式
            pattern = re.compile(""".*?(?P<card>核酸检测记录)|"""
                                 """检测中(?P<name>(([a-zA-Z+\.?\·?a-zA-Z+]{2,30}?)|([\u4e00-\u9fa5+\·?\u4e00-\u9fa5+]{2,30}?)))采样|"""
                                 """采样时间(?P<sample>(19|20)[0-9]{2}.?(0?[1-9]|1[012]).?(0?[1-9]|[12][0-9]|3[01])?[0-9]{2}.?[0-9]{2}.?[0-9]{2})|"""
                                 """检测时间(?P<test>(19|20)[0-9]{2}.?(0?[1-9]|1[012]).?(0?[1-9]|[12][0-9]|3[01])?[0-9]{2}.?[0-9]{2}.?[0-9]{2})|"""
                                 """检测机构(?P<agency>(.*?))数据来源|"""
                                 """检测结果(?P<result>[阴阳]性)"""
                                )
        if try_others:   
            print("使用try_others模式清理数据")
            #港澳通行证匹配模式 
            pattern = re.compile(""".*?(?P<card>核酸检测记录)|"""
                                 """刷新(?P<name>(([a-zA-Z+\.?\·?a-zA-Z+]{2,30}?)|([\u4e00-\u9fa5+\·?\u4e00-\u9fa5+]{2,30}?)))(?P<result>[阴阳]性)证件类型|"""
                                 """采样时间[：:](?P<sample>(19|20)[0-9]{2}.?(0?[1-9]|1[012]).?(0?[1-9]|[12][0-9]|3[01])?[0-9]{2}.?[0-9]{2}.?[0-9]{2})|"""
                                 """检测时间[：:](?P<test>(19|20)[0-9]{2}.?(0?[1-9]|1[012]).?(0?[1-9]|[12][0-9]|3[01])?[0-9]{2}.?[0-9]{2}.?[0-9]{2})|"""
                                 """检测机构[：:](?P<agency>(.*?))"""
                                )
        
        return pattern

    def check_data(self,catch_sum={},show_pic=False):         
        bad = False
        if catch_sum['card'] and not catch_sum['result']: 
            #采用try_others重新清理数据
            pattern = self.get_pattern(catch_sum["text"],try_others=True)
            catch_sum = self.clean_data(pattern,catch_sum)

        if not catch_sum['card']:
            catch_sum['card'] = "请人工检查！识别不到核酸结果！"
            catch_sum['result'] = "请人工检查！识别不到核酸结果！"
            bad = True

            print("\033[31m请人工检查！识别不到核酸结果！\033[0m")
            print(catch_sum)

        elif catch_sum['card'] and not catch_sum['result']:
            catch_sum['result'] = "请人工检查！识别不到核酸结果！"
            bad = True

        if catch_sum['result'] == "阳性":
            print("\033[31m核酸结果为阳性！请人工检查！\033[0m")
            bad = True

        temp_stamp={}    
        for k in "sample","test":
            if catch_sum[k]:
                try:
                    temp = re.sub("\D", "", catch_sum[k])
                    temp = time.strptime(temp,'%Y%m%d%H%M%S')
                    catch_sum[k] = time.strftime('%Y-%m-%d %H:%M:%S',temp)                
                    temp_stamp[k] = time.mktime(temp)

                except:
                    catch_sum[k] += "异常！识别到的时间格式不对！"
                    print("\033[31m识别到的时间格式不对：",catch_sum[k],"\033[0m")        

        try:
            if catch_sum['card'] and temp_stamp["sample"] > temp_stamp["test"]:
                print("\033[31m识别到的采样时间晚于检测时间\033[0m")
                catch_sum["sample"] += "！异常！识别到的采样时间晚于检测时间"
                catch_sum["test"] += "！异常！识别到的采样时间晚于检测时间"
                bad = True

            #是否开启采样时间检查
            if self.time_check and catch_sum['card'] and not self.latest_stamp > temp_stamp["sample"] > self.early_stamp:
                print("\033[31m采样时间太早或超出当前时间\033[0m")
                catch_sum["sample"] += "异常！采样时间太早！"
                bad = True
        except Exception as e:
            print("\033[31m时间比较出错,错误信息：",e,"\033[0m")
            bad = True

        #其它非关键内容 None 改 无
        for k,v in catch_sum.items():
            if not v:                 
                catch_sum[k] = "无" 

        if bad and show_pic:
            t = Thread(target=self.show_img,args=(catch_sum["img_name"],))
            t.start()

        return catch_sum
    
