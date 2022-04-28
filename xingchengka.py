import os,time,re,json,logging,csv,copy,zxing,shutil
from threading import Thread
from card import Card

class Xingchengka(Card):
   
    def __init__(self,img_path="行程卡/",result_file="行程卡解码信息.csv"):
        Card.__init__(self,img_path,result_file)

        self.catch_sum = {'img_name':None,
                        'card': None, 
                        'green': None,
                        'phone': None, 
                        'date': None, 
                        'visit': None, 
                        'danger': None,
                        'text':None}
        self.header = ["图片原文件路径","行程卡","是否为绿色行程卡","手机号","行程卡更新时间","途经城市","是否带*","识别文字"]

    def get_pattern(self,text,try_others=False):
        
        pattern = None    
        pattern = re.compile(""".*?(?P<card>(通信大数据行程卡)|(通信行程卡))|"""
                 """(?P<green>绿色行程卡)|"""
                    """(?P<phone>\d{3}.{4}\d{4})|"""
                    """(?P<date>(19|20)[0-9]{2}[- /.](0?[1-9]|1[012])[- /.](0?[1-9]|[12][0-9]|3[01])?[0-9]{2}.?[0-9]{2}.?[0-9]{2})|"""
                     """途[径|经].(?P<visit>.*?)[ (（注)|(结果)|(地区)]|"""
                     """(?P<danger>风险地区).*"""
                )
        
        return pattern

    def check_data(self,catch_sum={},show_pic=False):         
        bad = False
        if catch_sum['card']  and not catch_sum['green'] :
            catch_sum['green'] = "非绿卡！请人工检查！"
            catch_sum['danger'] = "非绿卡！请人工检查！"
            bad = True
            print("\033[31m识别不到绿色行程卡！请人工检查！\033[0m")
            print(catch_sum)
            
        elif not catch_sum['card'] :
            catch_sum['card'] = "识别不到行程卡"
            catch_sum['green'] = "识别不到卡！请人工检查！"
            catch_sum['danger'] = "识别不到卡！请人工检查！"
            bad = True
            print("\033[31m识别不到行程卡！请人工检查！\033[0m")
            print(catch_sum)

        elif not catch_sum['danger'] :
            catch_sum['danger'] = "无风险"                               

        if catch_sum["date"]:
            try:
                temp = re.sub("\D", "", catch_sum["date"])
                temp = time.strptime(temp,'%Y%m%d%H%M%S')
                catch_sum["date"] = time.strftime('%Y-%m-%d %H:%M:%S',temp)

                #是否开启时间检测
                temp_stamp = time.mktime(temp)                       
                if self.time_check and catch_sum['card'] and not self.latest_stamp > temp_stamp > self.early_stamp:
                    print("日期太早或不正常（超出当前时间）")
                    catch_sum["date"] += "！异常！"
                    bad = True

            except:
                print("\033[31m日期格式不对：",catch_sum["date"],"\033[0m")

        #其它非关键内容空值
        for k,v in catch_sum.items():
            if not v:                 
                catch_sum[k] = "无"   

        if bad and show_pic:
            t = Thread(target=self.show_img,args=(catch_sum["img_name"],))
            t.start()

        return catch_sum
    

   