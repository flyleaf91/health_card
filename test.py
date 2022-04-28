import time
import heshuan,xingchengka,yuekangma

def check_card():
    print("check")

def clean_result():
    print("clean")
    # yuekangma.dir_clean()
    # xingchengka.dir_clean()
    # heshuan.dir_clean()

if __name__ == '__main__':
    check_card()
    clean_result()
#     heshuan = Heshuan("核酸结果少量/","核酸结果解码信息.csv")
#     xingchengka = Xingchengka("行程卡少量/","行程卡解码信息.csv")
#     yuekangma = Yuekangma("粤康码少量/","粤康码解码信息.csv")

#     start = time.time()
#     heshuan.process_text()
#     end = time.time()
#     print("time:",end-start)

#     start = time.time()
#     xingchengka.process_text()
#     end = time.time()
#     print("time:",end-start)

#     start = time.time()
#     yuekangma.process_text()
#     end = time.time()
#     print("time:",end-start)