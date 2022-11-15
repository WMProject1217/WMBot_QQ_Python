WMBot_VersionString = "WMBot Python [Version 0.172.109]"
print(WMBot_VersionString)
print("2022 WMProject1217 Studios")
print("Elaina mirai sdk on mirai-api-http")
import sys
import os
import threading
import time
import ctypes
import psutil
import platform
import json
import socket
import requests
import struct
import codecs
import random
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import ImageFont
import PIL
import re
import ys_api
from ys_api import structs as ysstructs
from ys_api import UserDataMaxRetryError
from ys_api.cookie_set import timestamp_to_text
from datetime import datetime
from ela.app import Mirai
from ela.utils import run_app
from ela.message.models import Plain
from ela.message.models import Image

class WMLog4W:
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)

    def set_cmd_color(self, color, handle=std_out_handle):
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool

    def reset_color(self):
        self.set_cmd_color(0x0c | 0x0a | 0x09)

    def log_fail(self, print_text):
        timerr = time.localtime()
        timestr = str(timerr.tm_hour) + ":" + str(timerr.tm_min) + ":" + str(timerr.tm_sec)
        self.set_cmd_color(0x0c)
        print("["+timestr+"][FAIL] " + str(print_text))
        self.reset_color()

    def log_info(self, print_text):
        timerr = time.localtime()
        timestr = str(timerr.tm_hour) + ":" + str(timerr.tm_min) + ":" + str(timerr.tm_sec)
        self.set_cmd_color(0x0a)
        print("["+timestr+"][INFO] " + str(print_text))
        self.reset_color()
        
    def log_infon(self, print_text):
        timerr = time.localtime()
        timestr = str(timerr.tm_hour) + ":" + str(timerr.tm_min) + ":" + str(timerr.tm_sec)
        self.reset_color()
        print("["+timestr+"][INFO] " + str(print_text))

    def log_warn(self, print_text):
        timerr = time.localtime()
        timestr = str(timerr.tm_hour) + ":" + str(timerr.tm_min) + ":" + str(timerr.tm_sec)
        self.set_cmd_color(0x0e)
        print("["+timestr+"][WARN] " + str(print_text))
        self.reset_color()

def ConvertByteNumber(ByteNumber):
    BNL = "B"
    if ByteNumber > 1000:
        ByteNumber = ByteNumber / 1024
        BNL = "KB"
        if ByteNumber > 1000:
            ByteNumber = ByteNumber / 1024
            BNL = "MB"
            if ByteNumber > 1000:
                ByteNumber = ByteNumber / 1024
                BNL = "GB"
                if ByteNumber > 1000:
                    ByteNumber = ByteNumber / 1024
                    BNL = "TB"
                    if ByteNumber > 1000:
                        ByteNumber = ByteNumber / 1024
                        BNL = "PB"
                        if ByteNumber > 1000:
                            ByteNumber = ByteNumber / 1024
                            BNL = "EB"
    return str(format(ByteNumber,'.2f')) + BNL

def status():
    cpu_count = psutil.cpu_count(logical=False)
    xc_count = psutil.cpu_count()
    cpu_slv = round((psutil.cpu_percent(1)), 2)
    memory = psutil.virtual_memory()
    total_nc = round(( float(memory.total) / 1024 / 1024 / 1024), 2)
    used_nc = round(( float(memory.used) / 1024 / 1024 / 1024), 2)
    free_nc = round(( float(memory.free) / 1024 / 1024 / 1024), 2)
    syl_nc = round((float(memory.used) / float(memory.total) * 100), 2)
    disktotal = 0
    diskused = 0
    for disk in psutil.disk_partitions():
        if 'cdrom' in disk.opts or disk.fstype == '':
            continue
        disk_name_arr = disk.device.split(':')
        disk_name = disk_name_arr[0]
        disk_info = psutil.disk_usage(disk.device)
        disktotal = disktotal + disk_info.total
        diskused = diskused + disk_info.used
    boot_time = psutil.boot_time()
    boot_time_obj = datetime.fromtimestamp(boot_time)
    now_time = datetime.now()
    bootup_time = now_time - boot_time_obj
    return '服务器类型: '+platform.system()+' '+platform.version()+'\n已开机时间: '+str(bootup_time).split('.')[0]+'\nCPU: '+str(cpu_slv)+'% ( '+str(cpu_count)+'C'+str(xc_count)+'T )\nRAM: '+str(syl_nc)+'% ( '+str(used_nc)+'GB / '+str(total_nc)+'GB )\n磁盘总计: '+str(format(diskused/disktotal*100,'.2f'))+'% （'+str(ConvertByteNumber(diskused))+' / '+str(ConvertByteNumber(disktotal))+' )'

def WMJson_GetValue(filepath, itemname, fallback):
    if os.path.exists(filepath):
        loadjsontf = {}
        with open(filepath,'r',encoding='utf-8') as jsonopenex:
            loadjsontf = json.load(jsonopenex)
        if itemname in loadjsontf:
            return loadjsontf[itemname]
        else:
            return fallback
    else:
        return fallback

def WMJson_SetValue(filepath, itemname, itemvalue):
    if os.path.exists(filepath):
        loadjsontf = {}
        with open(filepath,'r',encoding='utf-8') as jsonopenex:
            loadjsontf = json.load(jsonopenex)
        loadjsontf[itemname] = str(itemvalue)
        with open(filepath, 'w', encoding='utf-8') as file_obj:
            json.dump(loadjsontf, file_obj)
        return 0
    else:
        loadjsontf = {}
        loadjsontf[itemname] = str(itemvalue)
        with open(filepath, 'w', encoding='utf-8') as file_obj:
            json.dump(loadjsontf, file_obj)
        return 0

def WMPermissionSystem_ReadMember(userid):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(userid) + ".json"
    return WMJson_GetValue(cfpath,"permission",fallback='null')

def WMPermissionSystem_WriteMember(userid,newpermission):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(userid) + ".json"
    WMJson_SetValue(cfpath, "permission", newpermission)
    return 0

def WMPermissionSystem_ReadGroup(groupid):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Group\\" + str(groupid) + ".json"
    return WMJson_GetValue(cfpath,"permission",fallback='null')

def WMPermissionSystem_WriteGroup(groupid,newpermission):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Group\\" + str(groupid) + ".json"
    WMJson_SetValue(cfpath, "permission", newpermission)
    return 0

def WMManagement_DelayAuto():
    delaytime = random.randint(128,1024)
    delaytime = delaytime / 1000
    time.sleep(delaytime)
    return 0

def elementDict(text, isOculus=False):
    elementProperty = str(re.sub(r'culus_number$', '', text)).lower()
    elementMastery = {
        "anemo": "风",
        "pyro": "火",
        "geo": "岩",
        "electro": "雷",
        "cryo": "冰",
        "hydro": "水",
        "dendro": "草",
        "none": "无",
    }
    try:
        elementProperty = str(elementMastery[elementProperty])
    except KeyError:
        elementProperty = "草"
    if isOculus:
        return elementProperty + "神瞳"
    elif not isOculus:
        return elementProperty + "属性"


def char_id_to_name(udata: ysstructs.GenshinUserData, charid: int):  # id2name.json数据不全, 我也懒得去搜集了, 故采用此邪道方法(
    chars = udata['avatars']
    for char in chars:
        if charid == char['id']:
            return char['name']
    global id2name
    if not id2name:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/id2name.json"), "r") as f:
            id2name = json.load(f)
    if str(charid) in id2name:
        return id2name[str(charid)]
    return f"{charid}"  

def dataAnalysisLite(userid: str):
    req = ys_api.GetUserInfo()
    data = req.get_user_info(userid)
    data_abyss = req.get_user_abyss(userid)
    abyss_info = abyssAnalysis(data_abyss, data)
    Account_Info = ""
    Account_Info += "活跃天数：　　" + str(data['stats']['active_day_number']) + "\n"
    Account_Info += "达成成就数量：" + str(data['stats']['achievement_number']) + "个\n"
    Account_Info += "获得角色数量：" + str(data['stats']['avatar_number']) + "个\n"
    Account_Info += "传送点已解锁：" + str(data['stats']['way_point_number']) + "个\n"
    Account_Info += "秘境解锁数量：" + str(data['stats']['domain_number']) + "个\n"
    Account_Info += "深渊当期进度："
    if data['stats']['spiral_abyss'] != "-":
        Account_Info += data['stats']['spiral_abyss'] + "\n"
    else:
        Account_Info += "没打\n"
    text = Account_Info
    width=320
    height=180
    im=PIL.Image.new('RGB',(width,height),(255,255,255))
    dr=PIL.ImageDraw.Draw(im)
    font=PIL.ImageFont.truetype('./assets/fontex.ttf', 24)
    dr.text((5,5),text,font=font,fill='#000000')
    im.save("./temp/genshinimage.jpg")
    return

def dataAnalysisCharacter(userid: str):
    req = ys_api.GetUserInfo()
    data = req.get_user_info(userid)
    data_abyss = req.get_user_abyss(userid)
    abyss_info = abyssAnalysis(data_abyss, data)
    Character_Info = ""
    name_length = []
    Character_List = data['avatars']
    for i in Character_List:
        name_length.append(len(i['name']))
    namelength_max = int(max(name_length))
    for i in Character_List:
        Character_Type = elementDict(i['element'], isOculus=False)
        if i['name'] == "旅行者":
            if i['image'].find("UI_AvatarIcon_PlayerGirl") != -1:
                TempText = (
                    str("荧") +
                    "（" + str(i['level']) + "级，"
                        + Character_Type + "）\n"
                )
            elif i['image'].find("UI_AvatarIcon_PlayerBoy") != -1:
                TempText = (
                    str("空") +
                    "（" + str(i['level']) + "级，"
                        + Character_Type + "）\n"
                )
            else:
                TempText = (
                    i['name'] + "[?]" +
                    "（" + str(i['level']) + "级，"
                        + Character_Type + "）\n"
                )
        else:
            TempText = (
                str(i['name']) +
                "（" + str(i['level']) + "级，"
                    + str(i['actived_constellation_num']) + "命，"
                    + str(i['fetter']) + "好感度，"
                    + re.sub('^105$', '5', str(i['rarity'])) + "★，"
                    + Character_Type + "）\n"
            )
        Character_Info = Character_Info + TempText
    text = Character_Info
    width=520
    height=1280
    im=PIL.Image.new('RGB',(width,height),(255,255,255))
    dr=PIL.ImageDraw.Draw(im)
    font=PIL.ImageFont.truetype('./assets/fontex.ttf', 24)
    dr.text((5,5),text,font=font,fill='#000000')
    im.save("./temp/genshinimage.jpg")
    return

def abyssAnalysis(aby: ysstructs.GenshinAbyss, udata: ysstructs.GenshinUserData):
    if not aby['floors']:  # 没打
        return ""
    rettext = f"第{aby['schedule_id']}期深境螺旋信息: 开始时间: {timestamp_to_text(aby['start_time'])},结束时间: {timestamp_to_text(aby['end_time'])}" 
    rettext = rettext + f"\n最深抵达:{aby['max_floor']},胜利场次/总场次: {aby['total_win_times']}/{aby['total_battle_times']},"
    #rettext = rettext + f"出战最多: {char_id_to_name(udata, aby['reveal_rank'][0]['avatar_id'])} - {aby['reveal_rank'][0]['value']}\n\t"
    #rettext = rettext + f"击破最多: {char_id_to_name(udata, aby['defeat_rank'][0]['avatar_id'])} - {aby['defeat_rank'][0]['value']}\n\t"
    #rettext = rettext + f"最强一击: {char_id_to_name(udata, aby['damage_rank'][0]['avatar_id'])} - {aby['damage_rank'][0]['value']}\n\t"
    #rettext = rettext + f"最高承伤: {char_id_to_name(udata, aby['take_damage_rank'][0]['avatar_id'])} - {aby['take_damage_rank'][0]['value']}\n\t"
    #rettext = rettext + f"元素战技: {char_id_to_name(udata, aby['normal_skill_rank'][0]['avatar_id'])} - {aby['normal_skill_rank'][0]['value']}\n\t"
    #rettext = rettext + f"元素爆发: {char_id_to_name(udata, aby['energy_skill_rank'][0]['avatar_id'])} - {aby['energy_skill_rank'][0]['value']}\n\t"
    rettext = rettext + f"总星数: ★ {aby['total_star']}\n"

    floor_text = ""  # 层
    has_details = False
    if len(aby['floors']) >= 0:
        if len(aby['floors'][0]['levels']) > 0:
            has_details = True
            for floor in aby['floors']:  # 层
                room_text = ""  # 间
                for room in floor['levels']:  # 间
                    battle_text = ""  # 场
                    for battle in room['battles']:  # 场次
                        character_text = ""  # 角色
                        for char in battle['avatars']:  # 角色列表
                            character_text += f"/{char_id_to_name(udata, char['id'])}"
                        battle_text += f",第 {battle['index']} 场: {character_text[1:]}"

                    room_text += f",第 {room['index']} 间 (★ {room['star']}/{room['max_star']}):{battle_text}"

                floor_text += f"\n第 {floor['index']} 层:{room_text}"
    rettext = f"{rettext}楼层信息:{floor_text}" if has_details else f"{rettext}未获取到详细楼层信息"
    return rettext

def dataAnalysisFull(userid: str):
    req = ys_api.GetUserInfo()
    data = req.get_user_info(userid)
    data_abyss = req.get_user_abyss(userid)
    abyss_info = abyssAnalysis(data_abyss, data)

    Character_Info = "人物：\n\t"
    name_length = []
    Character_List = data['avatars']
    for i in Character_List:
        name_length.append(len(i['name']))
    namelength_max = int(max(name_length))
    for i in Character_List:
        Character_Type = elementDict(i['element'], isOculus=False)
        if i['name'] == "旅行者":
            if i['image'].find("UI_AvatarIcon_PlayerGirl") != -1:
                TempText = (
                    str("荧") +
                    "（" + str(i['level']) + "级，"
                        + Character_Type + "）\n\t"
                )
            elif i['image'].find("UI_AvatarIcon_PlayerBoy") != -1:
                TempText = (
                    str("空") +
                    "（" + str(i['level']) + "级，"
                        + Character_Type + "）\n\t"
                )
            else:
                TempText = (
                    i['name'] + "[?]" +
                    "（" + str(i['level']) + "级，"
                        + Character_Type + "）\n\t"
                )
        else:
            TempText = (
                str(i['name']) +
                "（" + str(i['level']) + "级，"
                    + str(i['actived_constellation_num']) + "命，"
                    + str(i['fetter']) + "好感度，"
                    + re.sub('^105$', '5', str(i['rarity'])) + "★，"
                    + Character_Type + "）\n\t"
            )
        Character_Info = Character_Info + TempText
    Account_Info = "账号信息：\n\t"
    Account_Info += "活跃天数：　　" + str(data['stats']['active_day_number']) + "\n\t"
    Account_Info += "达成成就数量：" + str(data['stats']['achievement_number']) + "个\n\t"
    for key in data['stats']:
        if re.search(r'culus_number$', key[0]) is not None:
            Account_Info = "{}{}已收集：{}个\n\t".format(
                Account_Info,
                elementDict(str(key[0]), isOculus=True), 
                str(key[1])
            )
        else:
            pass
    Account_Info += "获得角色数量：" + str(data['stats']['avatar_number']) + "个\n\t"
    Account_Info += "传送点已解锁：" + str(data['stats']['way_point_number']) + "个\n\t"
    Account_Info += "秘境解锁数量：" + str(data['stats']['domain_number']) + "个\n\t"
    Account_Info += "深渊当期进度："
    if data['stats']['spiral_abyss'] != "-":
        Account_Info += data['stats']['spiral_abyss'] + "\n"
    else:
        Account_Info += "没打\n"
    Account_Info = Account_Info + (
        "\n开启宝箱计数：\n\t" +
        "普通宝箱：" + str(data['stats']['common_chest_number']) + "个\n\t" +
        "精致宝箱：" + str(data['stats']['exquisite_chest_number']) + "个\n\t" +
        "珍贵宝箱：" + str(data['stats']['precious_chest_number']) + "个\n\t" +
        "华丽宝箱：" + str(data['stats']['luxurious_chest_number']) + "个\n\t" +
        "奇馈宝箱：" + str(data['stats']['magic_chest_number']) + "个\n"
    )
    Area_list = data['world_explorations']
    Prestige_Info = "区域信息：\n"
    ExtraArea_Info = "供奉信息：\n"

    for i in Area_list:
        if (i['type'] == "Reputation"):
            Prestige_Info = "{}\t{}探索进度：{}%，声望等级：{}级\n".format(
                Prestige_Info,
                i['name'] + " ",
                str(i['exploration_percentage'] / \
                          10).replace("100.0", "100"),
                str(i['level'])
            )
        else:
            Prestige_Info = "{}\t{}探索进度：{}%\n".format(
                Prestige_Info,
                i['name'] + " ",
                str(i['exploration_percentage'] / \
                          10).replace("100.0", "100")
            )
        if len(i['offerings']) != 0:
            ExtraArea_Info = "{}\t{}供奉等级：{}级，位置：{}\n".format(
                ExtraArea_Info,
                str(i['offerings'][0]['name']) + " ",
                str(i['offerings'][0]['level']),
                str(i['name'])
            )
    if len(data['homes']) > 0:
        Home_Info = "家园信息：\n\t" + "已开启区域："
        Home_List = data['homes']
        homeworld_list = []
        for i in Home_List:
            homeworld_list.append(i['name'])
        Home_Info += '、'.join(homeworld_list) + "\n\t"
        Home_Info += "最高洞天仙力：  " + \
            str(Home_List[0]['comfort_num']) + '（' + \
            Home_List[0]['comfort_level_name'] + '）\n\t'
        Home_Info += "已获得摆件数量：" + str(Home_List[0]['item_num']) + "\n\t"
        Home_Info += "最大信任等级：  " + str(Home_List[0]['level']) + '级' + "\n\t"
        Home_Info += "最高历史访客数：" + str(Home_List[0]['visit_num'])
    else:
        Home_Info = "家园信息：\n\t" + "家园暂未开启！"

    text1 = Character_Info
    text2 = Account_Info
    text3 = Prestige_Info
    text4 = ExtraArea_Info
    text5 = Home_Info
    text6 = abyss_info
    width=1280
    height=720
    im=PIL.Image.new('RGB',(width,height),(255,255,255))
    dr=PIL.ImageDraw.Draw(im)
    fonta=PIL.ImageFont.truetype('./assets/fontex.ttf', 24)
    fontb=PIL.ImageFont.truetype('./assets/fontex.ttf', 16)
    dr.text((5,5),text1,font=fonta,fill='#000000')
    dr.text((5,320),text2,font=fonta,fill='#000000')
    dr.text((430,5),text3,font=fonta,fill='#000000')
    dr.text((600,500),text4,font=fonta,fill='#000000')
    dr.text((860,5),text5,font=fonta,fill='#000000')
    dr.text((260,320),text6,font=fonta,fill='#000000')
    dr.text((880,680),"Generated by WMBot Python [Version 0.172.36]\nWMProject1217 Studios 2022",font=fontb,fill='#000000',align="right")
    im.save("./temp/genshinimage.jpg")
    return

mirai_app = Mirai("http://127.0.0.1:12181/", qq=才不能让你看咱的账号！, verify_key="才不能让你看咱的密钥！")

@mirai_app.register("FriendMessage")
async def on_friendmessage(app: Mirai, ev):
    WMLog4W().log_infon(ev)

@mirai_app.register("GroupMessage")
async def on_groupmessage(app: Mirai, ev):
    WMRealTime_StartTime = time.time()
    WMLog4W().log_infon(ev)
    WMRealTime_NowUserPermission = WMPermissionSystem_ReadMember(ev.sender.id)
    WMRealTime_NowGroupPermission = WMPermissionSystem_ReadGroup(ev.group.id)
    WMRealTime_NowUserGroupPermission = ev.sender.permission
    
    if str(ev.sender.id) == "2070343282":
        if str(ev.messageChain) == "/wm debug threadcalltwp":
            WMRealTime_EndTime = time.time()
            await app.sendGroupMessage(ev.group,[Plain("WMBot Python (Thread#1 Process)"+"\n啪！(" + str(round(WMRealTime_EndTime - WMRealTime_StartTime, 4)) + " 秒)")],ev.source)
            return

    if WMRealTime_NowGroupPermission == "ban":
        return
    if WMRealTime_NowGroupPermission == "blocked":
        return
    if WMRealTime_NowGroupPermission == "null":
        return

    if WMRealTime_NowUserPermission == "ban":
        return
    if WMRealTime_NowUserPermission == "blocked":
        return

    WMManagement_DelayAuto()

    if (str(ev.messageChain) == "/wm getrandomimage"):
        rtpath = './rndimgdb'
        retlist = []
        for file_name in os.listdir(rtpath):
            retlist.append(file_name)
        retval = random.randint(0,len(retlist)-1)
        await app.sendGroupMessage(ev.group,[Image.from_path(rtpath+"/"+retlist[retval])],ev.source)
    if (str(ev.messageChain) == "立即随机图片"):
        rtpath = './rndimgdb'
        retlist = []
        for file_name in os.listdir(rtpath):
            retlist.append(file_name)
        retval = random.randint(0,len(retlist)-1)
        await app.sendGroupMessage(ev.group,[Image.from_path(rtpath+"/"+retlist[retval])],ev.source)
    if str(ev.messageChain)[0:24] == "/wm getgenshininfo lite ":
        tempuseruid = str(ev.messageChain)[24:]
        dataAnalysisLite(tempuseruid)
        await app.sendGroupMessage(ev.group,[Image.from_path("./temp/genshinimage.jpg")],ev.source)
        os.remove("./temp/genshinimage.jpg")
        return
    if str(ev.messageChain)[0:29] == "/wm getgenshininfo character ":
        tempuseruid = str(ev.messageChain)[29:]
        dataAnalysisCharacter(tempuseruid)
        await app.sendGroupMessage(ev.group,[Image.from_path("./temp/genshinimage.jpg")],ev.source)
        os.remove("./temp/genshinimage.jpg")
        return
    if str(ev.messageChain)[0:24] == "/wm getgenshininfo full ":
        tempuseruid = str(ev.messageChain)[24:]
        dataAnalysisFull(tempuseruid)
        await app.sendGroupMessage(ev.group,[Image.from_path("./temp/genshinimage.jpg")],ev.source)
        os.remove("./temp/genshinimage.jpg")
        return
    return

if __name__ == '__main__':
    WMLog4W().log_info("Done.")
    run_app(mirai_app)