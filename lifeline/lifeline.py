# -*- coding: utf8 -*-

import importlib 
import sys
importlib.reload(sys)
print("encoding="+sys.stdout.encoding)

import time
import calendar
import datetime # from datetime import datetime, date
import fractions # 分数模块

from FsBot.FsBot import FsBot # 引入机器人推送服务

# 现在时刻
now = list(time.localtime(time.time()))
# [2022, 12, 14, 14, 20, 56, 2, 348, 0]
# time.struct_time(tm_year=2022, tm_mon=12, tm_mday=14, tm_hour=14, tm_min=20, tm_sec=56, tm_wday=2, tm_yday=348, tm_isdst=0)夏令时
year = now[0]
month = now[1]
day = now[2]
hour = now[3]
minute = now[4]
second = now[5]
weekday = now[-3]  # 0~6 代表 周一至周日
thisyear_day_number = now[-2]  # 当年第几天

thisyear_days = 366 if calendar.isleap(int(str(year))) else 365  # 当年总天数
thismonth_days = calendar.monthrange(year, month)[1]  # 当月天数 (5, 30) 输出的是一个元组，第二个元素是这个月的天数
last_month_weekday = calendar.monthrange(year, month)[0]  # 上一个月的最后一天为星期几(0-6),星期天为0

# 上下班时间
on_work_time = "08:30"  # 这个时间不能直接用，后续会转换为“datetime.datetime”类型(通过datetime.strptime(date1, "%Y.%m.%d %H:%M:%S"))
off_work_time = "17:30"  # 这个时间不能直接用，后续会转换为“datetime.datetime”类型(通过datetime.strptime(date1, "%Y.%m.%d %H:%M:%S"))
# on_work_time_obj = datetime.datetime.strptime(on_work_time, "%H:%M")
# off_work_time_obj = datetime.datetime.strptime(off_work_time, "%H:%M")

# 工资日，每个月几号
pay_day = "25"

today = datetime.date.today()  # 今天日期 同 datetime.datetime.now().strftime('%Y-%m-%d')
yesterday = today - datetime.timedelta(days=1)  # 昨天日期
tomorrow = today + datetime.timedelta(days=1)  # 明天日期
day_of_week_en = datetime.date.today().weekday()  # 返回的0-6，代表周一到周日，同上面的weekday
day_of_week_cn = datetime.date.today().isoweekday()  # 返回1-7，代表周一到周日，当前时间所在本周第几天；

date = datetime.datetime.now().strftime('%Y-%m-%d')  # 结果同上面的today,但这是str类型，下同
time_hm = datetime.datetime.now().strftime('%H:%M')
# time_hm = '13:37'
# time_hm_obj = datetime.datetime.strptime(time_hm, "%H:%M")
time_hms = datetime.datetime.now().strftime('%H:%M:%S')
# time_hms_obj = datetime.datetime.strptime(time_hms, "%H:%M:%S")
# 在当前时间增加1小时：add_hour=datetime.datetime.now()+datetime.timedelta(hours=1)   #需要导入timedelta库
date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

"""
输出当前时间
"""
def print_time() -> str:
    msg_print_time = f'当前时间：{time_hm}\n'
    print(msg_print_time)
    return msg_print_time

"""
输出日期+日历
"""
def print_month(year, month) -> str:
    month_day_body = "\n"
    month_day_body += print_this_year_day_number(year, month)
    month_day_body += "=========================\n"
    month_day_body += print_notice_pay_day_line(pay_day, year, month, day)
    month_day_body += print_every_work_day_line(day_of_week_cn)
    month_day_body += print_month_title(year, month)
    month_day_body += print_month_body(year % 400 + 2000, month)

    # 上面的日历打印等价于
    # month_body = calendar.month(year,month)
    # month_day_body += month_body

    # run.feishu_bot("",content)

    return month_day_body

"""
输出日历头部内容
"""
def print_month_title(year, month) -> str:
    print("   ",get_month_name(month),"\t",str(year)+"年")
    print("–---" * 7)
    print("日\t一\t二\t三\t四\t五\t六")
    msg_month_title = ""
    msg_month_title += "=========================\n"
    msg_month_title += "\t" + str(get_month_name(month)) + "\t" + str(year) + "年\n"
    msg_month_title += "一\t二\t三\t四\t五\t六\t日\t\n"
    print(msg_month_title)
    return msg_month_title

"""
输出日历的主体内容
"""
def print_month_body(year, month) -> str:
    start_day = get_start_day(year, month)
    # print('完整周的起始日=',start_day)
    every_month_days = get_every_month_day(year, month)
    now = list(time.localtime(time.time()))
    msg_month_body = ""
    # for i in range(start_day):
    # print(" ",end="")
    # print(" " * start_day, end='')  # 从星期几开始则空4*几个空格
    # 上个月末占用第一周的天数
    last_month_days = 7 - start_day + 1
    # 打印上个月末的占位空格
    for i in range(last_month_days):
        msg_month_body += "\t"
    for j in range(1, every_month_days + 1):
        # if j < start_day:
        # print('%d' % j, end='\t')  # 宽度控制，4+1=5
        # msg_month_body += str(j) + "\t"
        if now[0] == year and now[1] == month and now[2] == j:
            # print('\033[35;5m%s\033[m' % (j), "",end="\t")
            # msg_month_body += format(j,'2d') + "\t"
            msg_month_body += "{" + format(j, '2d') + "}" + "\t"
        else:
            # print(format(j,'4d'),end="")
            # print(j,"", end="\t")
            msg_month_body += "" + format(j, '2d') + " " + "\t"
        # 一周结束就换行
        if (j + last_month_days) % 7 == 0:
            # print(" ")
            msg_month_body += "\n"
    msg_month_body += "\n=========================\n"
    print(msg_month_body)
    return msg_month_body

"""
今日日期
今天是今年的第几天
"""
def print_this_year_day_number(year, month) -> str:
    nowprt = list(time.localtime(time.time()))
    # thisyear_day_number = nowprt[-2]
    li_next_year_day = 0
    msg_this_year_day_number = ""
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    wday = week_list[weekday]
    for l in range(1, thisyear_day_number + 1):
        if nowprt[0] == year and nowprt[1] == month and nowprt[2] == l:
            this_day = nowprt[2]
            print("现在 是 {0}".format(year),"年\033[32;1m{0}\033[m 月 \033[32;1m{1}\033[m 日".format(month,this_day))
            print("{0}".format(year),"年的第","\033[32;1m%s\033[m" %(thisyear_day_number),"天")
            msg_this_year_day_number += str(year) + "年" + str(month) + "月" + str(day) + "日," + wday + "\n"
            msg_this_year_day_number += str(year) + "年的第" + str(thisyear_day_number) + "天\n"
    # 是否闰年
    if calendar.isleap(year) == True:
        li_next_year_day = 366 - thisyear_day_number
    else:
        li_next_year_day = 365 - thisyear_day_number
        print("距 \033[35;1m{0}\033[m".format(year+1),"年还有","\033[35;1m%s\033[m" %(li_next_year_day),"天")
    msg_this_year_day_number += "距" + str(year + 1) + "年还有" + str(li_next_year_day) + "天\n"
    # msg_this_year_day_number += "__________________________\n"
    # msg_this_year_day_number += "**************************\n"
    print(msg_this_year_day_number)
    return msg_this_year_day_number

"""
获取完整周的第一天
"""
def get_start_day(year, month):
    # start_day_jan_1_1800 = 3
    # start_day_jan_1_1800 = 4
    start_day_jan_1_1800 = 7-last_month_weekday  # 每月第一周天数
    total_days = get_total_days(year, month)
    return (total_days + start_day_jan_1_1800) % 7

"""
获取当月天数
同全局变量 thismonth_days = calendar.monthrange(year, month)[1]  # 当月天数 (5, 30) 输出的是一个元组，第二个元素是这个月的天数
"""
def get_every_month_day(year, month):
    every_month_day = 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    if calendar.isleap(year) == True and month == 2:
        return 29
    else:
        return every_month_day[month - 1]

"""
获取当年天数
同全局变量 thisyear_days = 366 if calendar.isleap(int(str(year))) else 365  # 当年总天数
"""
def get_total_days(year, month):
    total = 0
    for i in range(1800, year):
        if calendar.isleap(i) == True:
            total += 366
        else:
            total += 365
    for j in range(1, month):
        total += get_every_month_day(year, j)
    return total

"""
获取今天是当年的第几天
同全局变量 thisyear_day_number = now[-2]  # 当年第几天
"""
def get_thisyear_day_number(year, month):
    this_day = list(time.localtime(time.time()))
    thisyearday = this_day[2]
    for k in range(1, month):
        thisyearday += get_every_month_day(year, k)
    return thisyearday

"""
获取月份名称
"""
def get_month_name(month) -> str:
    n_month_name = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
    month_name = n_month_name[int(month) - 1]
    return str(month_name)


"""
所有(特殊)时间线都是在这个方法中调用
"""
def print_lifeline(year) -> str:
    msg_lifeline = ""
    return msg_lifeline


def print_lifeline() -> str:
    msg_lifeline = ""
    # @今年已过去
    msg_lifeline += print_every_year_line(year, month, thisyear_day_number, thisyear_days)
    # @这个月已过去
    msg_lifeline += print_every_month_line(month, day, thismonth_days)
    # # @本周已过去
    # msg_lifeline += print_every_week_line(day_of_week_cn)
    # @今天是上班的第几天
    # msg_lifeline += print_every_work_day_line(day_of_week_cn)
    # # @今天已过去
    # msg_lifeline += print_every_day_line(hour)
    # # @今天上班多久了
    # msg_lifeline += print_every_work_hour_config_line(time_hm, on_work_time, off_work_time)
    # @工资日提醒
    # msg_lifeline += print_notice_pay_day_line(pay_day, year, month, day)
    return msg_lifeline


"""
今年已过去
"""
def print_every_year_line(year, month, thisyear_day_number, thisyear_days) -> str:
    rate = round(thisyear_day_number / thisyear_days, 4)  # 使用内置函数round来保留4位小数
    every_year_line = format(rate, '.2%')  # '{:.2%}'.format(f) 或 '%.2f%%'%(f*100)
    over_year_line = format(1 - rate, '.2%')
    msg_every_year_line = str(year) + "年过去了" + str(month - 1) + "个月,度过了" + str(thisyear_day_number - 1) + "天\n"
    msg_every_year_line += str(year) + "年过去了" + str(every_year_line) + ",剩余" + str(over_year_line) + "\n"
    msg_every_year_line += progress_bar(rate)
    # msg_every_year_line += "**************************\n"
    print("@今年已过去")
    print(msg_every_year_line)
    return msg_every_year_line


"""
这个月已过去
"""
def print_every_month_line(month, day, month_days) -> str:
    rate = round(day / month_days, 4)  # 使用内置函数round来保留4位小数
    every_month_line = format(rate, '.2%')  # '{:.2%}'.format(f) 或 '%.2f%%'%(f*100)
    over_month_line = format(1 - rate, '.2%')
    msg_every_month_line = str(month) + "月过去了" + str(day - 1) + "天,剩余" + str(over_month_line) + "\n"
    msg_every_month_line += progress_bar(rate)
    # msg_every_month_line += "**************************\n"
    print("@这个月已过去")
    print(msg_every_month_line)
    return msg_every_month_line


"""
本周已过去
"""
def print_every_week_line(day_of_week_cn) -> str:
    rate = round(day_of_week_cn / 7, 4)
    fenshu = fractions.Fraction(day_of_week_cn, 7)
    msg_every_week_line = ""
    # msg_every_week_line += "本周已过去" + str(rate) + "\n"
    msg_every_week_line += "今天是本周的" + str(fenshu) + ""
    if day_of_week_cn <= 5:
        msg_every_week_line += ",距离周末还有" + str(5 - day_of_week_cn + 1) + "天\n"
        msg_every_week_line += progress_bar(rate)
    else:
        msg_every_week_line += ",周末愉快哦~\n"
    # msg_every_week_line += "**************************\n"
    print("@本周已过去")
    print(msg_every_week_line)
    return msg_every_week_line


"""
今天是上班的第几天
"""
def print_every_work_day_line(day_of_week_cn) -> str:
    # day_of_week_cn = 3
    msg_every_work_day_line = ""
    if day_of_week_cn <= 5:
        rate = round(day_of_week_cn / 7, 4)
        fenshu = fractions.Fraction(day_of_week_cn, 5)
        msg_every_work_day_line += "上班的第[" + str(day_of_week_cn) + "]/5天,距离周末还有" + str(
            5 - day_of_week_cn + 1) + "天\n"
        msg_every_work_day_line += progress_bar(rate)
    else:
        msg_every_work_day_line += "今天周末愉快哦~距离周一上班还有" + str(7 - day_of_week_cn + 1) + "天\n"
    # msg_every_work_day_line += "**************************\n"
    print("@今天是上班的第几天")
    print(msg_every_work_day_line)
    return msg_every_work_day_line


"""
今天已过去
"""
def print_every_day_line(hour) -> str:
    rate = round(hour / 24, 4)
    fenshu = fractions.Fraction(hour, 24)
    msg_every_day_line = ""
    msg_every_day_line += "今天过去大约" + str(int(hour) - 1) + "小时,还剩" + str(format(1 - rate, '.2%')) + "\n"
    msg_every_day_line += progress_bar(rate)
    # msg_every_day_line += "**************************\n"
    print("@今天已过去")
    print(msg_every_day_line)
    return msg_every_day_line


"""
每个小时提醒（为了夜间等免打扰，支持自定义时间段）
"""
def print_every_hour_config_line() -> str:
    msg_every_hour_config_line = ""
    return msg_every_hour_config_line


"""
今天上班多久了
"""
def print_every_work_hour_config_line(time_hm, on_work_time, off_work_time) -> str:
    msg_every_work_hour_config_line = ""
    # 仅在工作日才通知
    if day_of_week_cn <= 5:
        if time_hm > on_work_time and time_hm < off_work_time:
            work_hour = get_work_hour(time_hm, on_work_time)
            count_work_hour = get_count_work_hour(on_work_time, off_work_time)
            over_work_hour = get_over_work_hour(time_hm, off_work_time)
            rate = round(work_hour / count_work_hour, 4)
            # print(count_work_hour)
            # print(over_work_hour)
            msg_every_work_hour_config_line += "今天搬砖了" + str(format(rate, '.2%')) + ",还有" + str(
                over_work_hour) + "分钟下班\n"
            msg_every_work_hour_config_line += "记得喝喝水、站起来运动一下，对脊椎好~\n"
            msg_every_work_hour_config_line += progress_bar(rate)
        if time_hm >= off_work_time:
            msg_every_work_hour_config_line += "今天的砖已经搬完啦，好好休息、睡个好觉吧\n"
    # msg_every_work_hour_config_line += "**************************\n"
    print("@今天上班多久了")
    print(msg_every_work_hour_config_line)
    return msg_every_work_hour_config_line

"""
一天上班多少分钟
"""
def get_count_work_hour(on_work_time, off_work_time) -> str:
    # time_hm_obj = datetime.datetime.strptime(time_hm, "%H:%M")
    # time_hms_obj = datetime.datetime.strptime(time_hms, "%H:%M:%S")
    on_work_time_obj = datetime.datetime.strptime(on_work_time, "%H:%M")
    off_work_time_obj = datetime.datetime.strptime(off_work_time, "%H:%M")
    count_work_hour = round((off_work_time_obj - on_work_time_obj).seconds / 3600, 2)  # 总上班小时时长
    return count_work_hour

"""
已上班多少分钟了
"""
def get_work_hour(time_hm, on_work_time) -> str:
    time_hm_obj = datetime.datetime.strptime(time_hm, "%H:%M")
    on_work_time_obj = datetime.datetime.strptime(on_work_time, "%H:%M")
    work_hour = round((time_hm_obj - on_work_time_obj).seconds / 3600, 2)  # 已上班小时时长
    return work_hour

"""
距离下班还有多少分钟
"""
def get_over_work_hour(time_hm, off_work_time) -> str:
    time_hm_obj = datetime.datetime.strptime(time_hm, "%H:%M")
    # time_hms_obj = datetime.datetime.strptime(time_hms, "%H:%M:%S")
    off_work_time_obj = datetime.datetime.strptime(off_work_time, "%H:%M")
    over_work_hour = int((off_work_time_obj - time_hm_obj).seconds / 60)  # 距离下班还有多少分钟
    return over_work_hour

"""
上班打卡提醒
"""
def print_notice_on_work_line(time_hm, on_work_time) -> str:
    # print(time_hm)
    # print(on_work_time)
    # 仅在工作日才通知
    if day_of_week_cn <= 5:
        # 仅在上班前才通知
        if time_hm <= on_work_time:
            time_hm_obj = datetime.datetime.strptime(time_hm, "%H:%M")
            on_work_time_obj = datetime.datetime.strptime(on_work_time, "%H:%M")
            # 距离上班还有多久时间
            over_on_work_time = int((on_work_time_obj - time_hm_obj).seconds / 60)
            msg_notice_on_work_line = f"当前时间：{time_hm}\n请注意【打卡】❗❗❗\n距离上班【{on_work_time}】还有【{over_on_work_time}】分钟⚠⚠⚠\n" \
                                      # f"================================.\n" \
                                      # f"========.,@@#,==================.\n" \
                                      # f"==========#@%====================\n" \
                                      # f"==========#@*,,==================\n" \
                                      # f"========,;#@###;,,,:::;+?%SS*====\n" \
                                      # f"====.:?S##@@S*:+%%%%#@@%?**+;====\n" \
                                      # f"====.,,:,,#@#*,==,==;@@;========.\n" \
                                      # f"======.:*%@@*======.,@@;========.\n" \
                                      # f"==.:;?S#?;#@+======.,#@+========.\n" \
                                      # f"==,?@@%:.,#@+======.,#@*========.\n" \
                                      # f"====,,.+**@@+====,,.:@@?========.\n" \
                                      # f"======.:?@@@:====:%##@@+========.\n" \
                                      # f"========.;*:======,?@#?,========.\n" \
                                      # f"================================.\n" \
                                      # f"============.,;:,================\n" \
                                      # f"============.:#@#;==============.\n" \
                                      # f"==============*@@?*%SS+==========\n" \
                                      # f"==============;@@?*+;:,==========\n" \
                                      # f"==============:@@:,,:;+*?%?+,====\n" \
                                      # f"====::::;;+**?%@@SSSSSS%%%%?:====\n" \
                                      # f"====+S##S%?*+;%@@;==============.\n" \
                                      # f"======,,======:@@;%?;,==========.\n" \
                                      # f"==============:@@:;S@@S;========.\n" \
                                      # f"==============:@@:==:?#%========.\n" \
                                      # f"==============;@@:==============.\n" \
                                      # f"==============%@@,==============.\n" \
                                      # f"==============?@S================\n" \
                                      # f"==============.+:================\n"
    print("@上班打卡提醒")
    print(msg_notice_on_work_line)
    return msg_notice_on_work_line


"""
下班打卡提醒
"""
def print_notice_off_work_line(time_hm, off_work_time) -> str:
    msg_notice_off_work_line = ""
    # 仅在工作日才通知
    if day_of_week_cn < 5:
        # 下班前，预通知即将打卡
        if time_hm < off_work_time:
            msg_notice_off_work_line += f"\n{get_over_work_hour(time_hm, off_work_time)}\n"
        # 达到下班时间，正式通知打卡
        else:
            msg_notice_off_work_line += f"当前时间：{time_hm}\n下班啦，今天的砖就搬到这了\n请注意【打卡】❗❗❗\n晚上好好休息吧( •̀ ω •́ )✧\n"
    print("@下班打卡提醒")
    return msg_notice_off_work_line


"""
工资日提醒
"""
def print_notice_pay_day_line(pay_day, year, month, day) -> str:
    msg_pay_day_line = ""
    # day = 30
    # 设定的工资日并不一定就是本月实际的发薪日，可能是最近的周五发
    # 获取设定工资日的星期几
    pay_day_weekday = get_week_day(year, month, pay_day);
    # 实际发薪日
    actual_pay_day = int(pay_day) if pay_day_weekday <= 5 else int(pay_day) - (pay_day_weekday - 5)
    # print(type(pay_day))
    # print(type(day))
    # print((actual_pay_day))
    # 工资日之前
    if day <= int(actual_pay_day):
        # 今天是工资日
        if day == actual_pay_day:
            # print(type(pay_day))
            # print(type(day))
            # print(type(actual_pay_day))
            msg_pay_day_line += "今天是工资日，坐等发钱吧~耐心等等~\n"
            msg_pay_day_line += progress_bar(1)
        # 没到本月工资日
        elif day < actual_pay_day:
            over_pay_day = actual_pay_day - day
            msg_pay_day_line += "距离工资日[%s-%s]还有%s天\n" % (month, actual_pay_day, over_pay_day)
            msg_pay_day_line += progress_bar((30 - over_pay_day) / 30)
    # 过了本月工资日
    else:
        # 跨年了
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        # 下一月发薪日的星期几
        pay_day_weekday = get_week_day(year, month, pay_day)
        next_pay_day = int(pay_day) if pay_day_weekday <= 5 else int(pay_day) - (pay_day_weekday - 5)
        count_pay_day = thismonth_days - actual_pay_day + next_pay_day
        over_pay_day = thismonth_days - day + next_pay_day
        # print((thismonth_days))
        # print((day))
        # print((next_pay_day))
        # print((count_pay_day))
        # print((over_pay_day))
        msg_pay_day_line += "距离工资日[%s-%s]还有%s天\n" % (month, next_pay_day, over_pay_day)
        msg_pay_day_line += progress_bar((count_pay_day - over_pay_day) / count_pay_day)
    print("@工资日提醒")
    print(msg_pay_day_line)
    return msg_pay_day_line


"""
获取指定日期的星期(直接整个字符串传入)
"""
def get_week_day(date_str) -> str:
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    week_index = time.strptime(date_str, '%Y-%m-%d').tm_wday  # 获取指定时间的星期,0-6:日-六
    # week_day = week_list[week_index]
    return week_index + 1


"""
获取指定日期的星期(按需参数传入)
"""
def get_week_day(year, month, day) -> str:
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    week_index = time.strptime(str(year) + "-" + str(month) + "-" + str(day), '%Y-%m-%d').tm_wday  # 获取指定时间的星期,0-6:日-六
    # week_day = week_list[week_index]
    return week_index + 1


"""
进度条样式（不覆盖显示进度条）

# import sys
# import time
def progress_bar(iteration, total, prefix='', suffix='', decimals=1, barLength=100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))  # 5.0  10.0
    filledLength = round(barLength * iteration / float(total))  # 则四舍五入到最接近的整数
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    # sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix))
    print('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix))
    if iteration == total:
        # sys.stdout.write('\n')
    # sys.stdout.flush()  # 实时输出
    # time.sleep(1)
# TEST_NUM = 30
# for i in range(1, TEST_NUM + 1):
#     inf_progress(i, TEST_NUM, 'Progress', 'Complete', 1, 50)
"""

"""
进度条样式（单一输出）
"""
def progress_bar(rate) -> str:
    prefix = ''  # 前缀
    suffix = ''  # 后缀
    fill_block = '▪'
    null_block = '▫'
    decimals = 2  # 小数位数
    barLength = 25  # 进度条总长度
    formatStr = "{0:." + str(decimals) + "f}"  # 格式化小数
    ### rate = round(thisyear_day_number/year_days, 4) # 使用内置函数round来保留4位小数
    ### every_year_line = format(rate,'.2%') # '{:.2%}'.format(f) 或 '%.2f%%'%(f*100)
    percent = formatStr.format(100 * rate)  # 5.0  10.0
    # percent = rate  # 5.0  10.0
    # filledLength = round(barLength * iteration / float(total))  # 已填充长度 则四舍五入到最接近的整数
    filledLength = round(barLength * rate)  # 已填充长度 则四舍五入到最接近的整数
    bar = fill_block * filledLength + null_block * (barLength - filledLength)
    # sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix))
    out = '\r%s|%s|%s%s%s\n' % (prefix, bar, percent, '%', suffix)
    # print(out)
    return out


"""
控制台打印变量和结果，方便调试
"""
def print_all():
    print("now=", now)
    print("year=", year)
    print("month=", month)
    print("day=", day)
    print("hour=", hour)
    print("minute=", minute)
    print("second=", second)
    print("weekday=", weekday)
    print("thisyear_day_number=", thisyear_day_number)
    print("year_days=", thisyear_days)
    print("month_days=", thismonth_days)
    print("last_month_weekday=", last_month_weekday)
    print("on_work_time=", on_work_time)
    # print("on_work_time_obj=", on_work_time_obj)
    print("off_work_time=", off_work_time)
    # print("off_work_time_obj=", off_work_time_obj)
    print("pay_day=", pay_day)
    print("today=", today)
    print("yesterday=", yesterday)
    print("tomorrow=", tomorrow)
    print("day_of_week_en=", day_of_week_en)
    print("day_of_week_cn=", day_of_week_cn)
    print("date=", date)
    print("time_hm=", time_hm)
    # print("time_hm_obj=", time_hm_obj)
    print("time_hms=", time_hms)
    # print("time_hms_obj=", time_hms_obj)
    print("date_time=", date_time)
    # print_month(year, month)
    # print(print_every_year_line(year, month, thisyear_day_number, thisyear_days))


def main(event, context):
    print(sys.getdefaultencoding()) # 默认utf-8

    print_all()

    title = ""
    content = ""
    # 仅在工作日才通知
    if day_of_week_cn <= 5:
        if time_hm <= on_work_time:
            title = "❗上班【打卡】提醒⚠"
            content = print_notice_on_work_line(time_hm, on_work_time)
            print(f"@print_notice_on_work_line=={content}")
        elif time_hm >= off_work_time:
            title = "⚠下班【打卡】提醒❗"
            content = print_notice_off_work_line(time_hm, off_work_time)
            print(f"@print_notice_off_work_line=={content}")
        else:
            title = "⌚时间进度条👻"
            content = ""
            content += print_time()
            content += print_every_work_hour_config_line(time_hm, on_work_time, off_work_time)
            # content += print_notice_pay_day_line(pay_day, year, month, day)
            content += print_month(year, month)
            content += print_lifeline()
            print(f"content=={content}")

        content += "\n来自Tencent_云函数SCF的支持\n"

        # 推送机器人内测群
        WEBHOOK_URL_1 = "your-webhook-url"
        # 安全校验,需要在机器人=>安全设置=>签名校验 详见 https://getfeishu.cn/hc/zh-cn/articles/360024984973-%E5%9C%A8%E7%BE%A4%E8%81%8A%E4%B8%AD%E4%BD%BF%E7%94%A8%E6%9C%BA%E5%99%A8%E4%BA%BA
        WEBHOOK_SECRET_1 = "your-webhook-secret"
        # run.feishu_bot(title,content)
        # run.wecom_app(title,content)
        bot1 = FsBot(webhook_url=WEBHOOK_URL_1, webhook_secret=WEBHOOK_SECRET_1).send_text(title, content)

if __name__ == '__main__':
    event=""
    context=""
    main(event, context)

# todo: 每小时提醒
# todo: 上下班提示
# todo: 实时天气提醒
# todo: 定时推送
# todo: 工资日提醒
# todo: 增加进度条样式
# todo: tm_wday
# todo: get_week_day
# todo: 工资日遇到春节等假期，需要再提前
# todo: 把一些公共代码抽成方法
# todo: 把依赖提取为requirements.txt
# todo: 支持显示图片
# todo: 修改上下班的banner
# todo: 打卡提醒的频率需要优化，仅8点和8点半提醒，容易错过打卡
#   上班期间    0 30 9,11,16 * * *
#   非上班  0 25 8 * * *   0 35 17 * * *
# todo: 上班打卡的文案需要优化
# todo: 中午提示吃饭和午休
# todo: 把日历中的日期显示抽成方法
# todo: 记得喝喝水、站起来运动一下，对脊椎好~
