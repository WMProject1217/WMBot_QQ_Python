WMBot_VersionString = "WMBot Python [Version 0.172.109]"
print(WMBot_VersionString)
print("2022 WMProject1217 Studios")
print("Elaina mirai sdk on mirai-api-http")
import sys
import os
import threading
import time
import datetime
import ctypes
import psutil
import platform
import json
import socket
import requests
import struct
import codecs
import random
import configparser
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

def WMCoin_ReadNumber(userid):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(userid) + ".json"
    return WMJson_GetValue(cfpath,"coin",fallback='0')

def WMCoin_WriteNumber(userid,newcoinnumber):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(userid) + ".json"
    WMJson_SetValue(cfpath, "coin", str(newcoinnumber))
    return 0

def WMExp_ReadNumber(userid):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(userid) + ".json"
    return WMJson_GetValue(cfpath,"exp",fallback='0')

def WMExp_WriteNumber(userid,newexpnumber):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(userid) + ".json"
    WMJson_SetValue(cfpath, "exp", str(newexpnumber))
    return 0

def WMSign_ReadInfo(userid):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(userid) + ".json"
    return WMJson_GetValue(cfpath,"signupidt",fallback='null')

def WMSign_WriteInfo(userid,coinnewint,expnewint):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(userid) + ".json"
    newids = datetime.today().date()
    coinnumber = int(WMJson_GetValue(cfpath,"coin",fallback='0')) + coinnewint
    expnumber = int(WMJson_GetValue(cfpath,"exp",fallback='0')) + expnewint
    WMJson_SetValue(cfpath, "signupidt", str(newids))
    WMJson_SetValue(cfpath, "coin", str(coinnumber))
    WMJson_SetValue(cfpath, "exp", str(expnumber))
    return 0

def WMManagement_CountGroupMessage(groupid):
    cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Group\\" + str(groupid) + ".json"
    newmsgnumtotal = int(WMJson_GetValue(cfpath,"msgnumtotal",fallback='0')) + 1
    WMJson_SetValue(cfpath, "msgnumtotal", str(newmsgnumtotal))
    return newmsgnumtotal

def WMManagement_CountGroupHotMember(groupid,memberid):
    filepath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\GroupHotMember\\" + str(groupid) + ".json"
    if os.path.exists(filepath):
        loadjsontf = {}
        with open(filepath,'r',encoding='utf-8') as jsonopenex:
            loadjsontf = json.load(jsonopenex)
        if not memberid in loadjsontf["cplist"]:
            loadjsontf["cplist"].append(memberid)
        with open(filepath, 'w', encoding='utf-8') as file_obj:
            json.dump(loadjsontf, file_obj)
        return 0
    else:
        loadjsontf = {}
        loadjsontf["cplist"] = [memberid]
        with open(filepath, 'w', encoding='utf-8') as file_obj:
            json.dump(loadjsontf, file_obj)
        return 0

def WMManagement_DelayAuto():
    delaytime = random.randint(128,1024)
    delaytime = delaytime / 1000
    time.sleep(delaytime)
    return 0

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
    WMRealTime_GroupMessageNumberTotal = WMManagement_CountGroupMessage(ev.group.id)

    if str(ev.sender.id) == "才不能让你看咱的账号！":
        if str(ev.messageChain) == "!wmbot pythonrt debug sendmes sendNudge":
            await app.sendNudge(ev.sender,ev.group)
            return
        if str(ev.messageChain) == "!wmbot pythonrt debug sendmes image":
            await app.sendGroupMessage(ev.group,[Image.from_path("./debug/img0.jpg")],ev.source)
            return
        if str(ev.messageChain) == "/wm debug status":
            await app.sendGroupMessage(ev.group,[Plain(status())],ev.source)
            return
        if str(ev.messageChain)[0:29] == "/wm sudo setmemberpermission ":
            tempstra = str(ev.messageChain)[29:].split(" ")
            WMPermissionSystem_WriteMember(tempstra[0],tempstra[1])
            await app.sendGroupMessage(ev.group,[Plain("将成员 " + tempstra[0] + " 的权限设为 " + tempstra[1])],ev.source)
            return
        if str(ev.messageChain)[0:30] == "/wm sudo readmemberpermission ":
            await app.sendGroupMessage(ev.group,[Plain("成员 " + str(ev.messageChain)[30:] + " 的权限为 " + WMPermissionSystem_ReadMember(str(ev.messageChain)[30:]))],ev.source)
            return
        if str(ev.messageChain)[0:28] == "/wm sudo setgrouppermission ":
            tempstra = str(ev.messageChain)[28:].split(" ")
            WMPermissionSystem_WriteGroup(tempstra[0],tempstra[1])
            await app.sendGroupMessage(ev.group,[Plain("将群 " + tempstra[0] + " 的权限设为 " + tempstra[1])],ev.source)
            return
        if str(ev.messageChain)[0:29] == "/wm sudo readgrouppermission ":
            await app.sendGroupMessage(ev.group,[Plain("群 " + str(ev.messageChain)[29:] + " 的权限为 " + WMPermissionSystem_ReadGroup(str(ev.messageChain)[29:]))],ev.source)
            return
        if str(ev.messageChain) == "/wm debug threadcalltwp":
            WMRealTime_EndTime = time.time()
            await app.sendGroupMessage(ev.group,[Plain("WMBot Python (Main Process)"+"\n啪！(" + str(round(WMRealTime_EndTime - WMRealTime_StartTime, 4)) + " 秒)")],ev.source)
            return
        if (str(ev.messageChain)[0:15] == "/wm debug user "):
            userid = str(ev.messageChain)[15:]
            cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(userid) + ".json"
            content = "null"
            if os.path.exists(cfpath):
                with open(cfpath,'r',encoding='utf-8') as filert:
                    content=filert.read()
            await app.sendGroupMessage(ev.group,[Plain(content)],ev.source)
            return
        if (str(ev.messageChain)[0:16] == "/wm debug group "):
            userid = str(ev.messageChain)[16:]
            cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Group\\" + str(userid) + ".json"
            content = "null"
            if os.path.exists(cfpath):
                with open(cfpath,'r',encoding='utf-8') as filert:
                    content=filert.read()
            await app.sendGroupMessage(ev.group,[Plain(content)],ev.source)
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

    if WMRealTime_NowUserPermission == "root":
        if (str(ev.messageChain) == "/wm root test"):
            WMRealTime_EndTime = time.time()
            await app.sendGroupMessage(ev.group,[Plain("啪！(" + str(round(WMRealTime_EndTime - WMRealTime_StartTime, 4)) + " 秒)")],ev.source)
            return
    elif WMRealTime_NowUserPermission == "rootadmin":
        if (str(ev.messageChain) == "/wm rootadmin test"):
            WMRealTime_EndTime = time.time()
            await app.sendGroupMessage(ev.group,[Plain("啪！(" + str(round(WMRealTime_EndTime - WMRealTime_StartTime, 4)) + " 秒)")],ev.source)
            return
    elif WMRealTime_NowUserPermission == "debugadmin":
        if (str(ev.messageChain) == "/wm debugadmin test"):
            WMRealTime_EndTime = time.time()
            await app.sendGroupMessage(ev.group,[Plain("啪！(" + str(round(WMRealTime_EndTime - WMRealTime_StartTime, 4)) + " 秒)")],ev.source)
            return

    if WMRealTime_NowUserGroupPermission == "OWNER":
        if (str(ev.messageChain) == "/wm testcdsf"):
            await app.sendGroupMessage(ev.group,[Plain("OWNER")],ev.source)
            return
    elif WMRealTime_NowUserGroupPermission == "ADMINISTRATOR":
        if (str(ev.messageChain) == "/wm testcdsf"):
            await app.sendGroupMessage(ev.group,[Plain("ADMINISTRATOR")],ev.source)
            return

    WMManagement_CountGroupHotMember(ev.group.id,ev.sender.id)
    WMManagement_DelayAuto()

    if (str(ev.messageChain) == "/wm about"):
        await app.sendGroupMessage(ev.group,[Plain(WMBot_VersionString + "\n2022 WMProject1217 Studios\nElaina mirai sdk on mirai-api-http")],ev.source)
        return
    if str(ev.messageChain) == "/wm help":
        await app.sendGroupMessage(ev.group,[Image.from_path("./assets/help.jpg")],ev.source)
        return
    if str(ev.messageChain) == "立即帮助":
        await app.sendGroupMessage(ev.group,[Image.from_path("./assets/help.jpg")],ev.source)
        return
    if (str(ev.messageChain) == "/wm sign"):
        nowids = datetime.today().date()
        if (str(WMSign_ReadInfo(ev.sender.id)) == str(nowids)):
            await app.sendGroupMessage(ev.group,[Plain("您今天已经签到。")],ev.source)
            return
        else:
            coinnewdt = random.randint(1,64)
            expnewdt = random.randint(1,64)
            WMSign_WriteInfo(ev.sender.id,coinnewdt,expnewdt)
            retlist = ["大凶","凶","小吉","吉","吉","吉","吉","吉","吉","吉","吉","吉","吉","大吉"]
            retval = random.randint(0,len(retlist)-1)
            userfortune = retlist[retval]
            await app.sendGroupMessage(ev.group,[Plain("签到成功，获得 " + str(coinnewdt) + " 个硬币和 " + str(expnewdt) + " 点经验。\n今天的运势是 " + userfortune + " 。")],ev.source)
            return
    if (str(ev.messageChain) == "立即签到"):
        nowids = datetime.today().date()
        if (str(WMSign_ReadInfo(ev.sender.id)) == str(nowids)):
            await app.sendGroupMessage(ev.group,[Plain("您今天已经签到。")],ev.source)
            return
        else:
            coinnewdt = random.randint(1,64)
            expnewdt = random.randint(1,64)
            WMSign_WriteInfo(ev.sender.id,coinnewdt,expnewdt)
            retlist = ["大凶","凶","小吉","吉","吉","吉","吉","吉","吉","吉","吉","吉","吉","大吉"]
            retval = random.randint(0,len(retlist)-1)
            userfortune = retlist[retval]
            await app.sendGroupMessage(ev.group,[Plain("签到成功，获得 " + str(coinnewdt) + " 个硬币和 " + str(expnewdt) + " 点经验。\n今天的运势是 " + userfortune + " 。")],ev.source)
            return
    if (str(ev.messageChain) == "/wm user info"):
        reinfouser = "名称: " + ev.sender.memberName + " (id:" + str(ev.sender.id) + ",permission:" + WMPermissionSystem_ReadMember(ev.sender.id) + ")\n硬币数量: " + str(WMCoin_ReadNumber(ev.sender.id)) + ",经验数量: " + str(WMExp_ReadNumber(ev.sender.id)) + ",上次签到: " + str(WMSign_ReadInfo(ev.sender.id))
        await app.sendGroupMessage(ev.group,[Plain(reinfouser)],ev.source)
        return
    if (str(ev.messageChain) == "/wm user debug"):
        cfpath = os.environ["SystemDrive"] + "\\WMSystem\\database\\WMBot\\Member\\" + str(ev.sender.id) + ".json"
        content = "null"
        if os.path.exists(cfpath):
            with open(cfpath,'r',encoding='utf-8') as filert:
                content=filert.read()
        await app.sendGroupMessage(ev.group,[Plain(content)],ev.source)
        return
    if (str(ev.messageChain) == "/wm ping"):
        WMRealTime_EndTime = time.time()
        await app.sendGroupMessage(ev.group,[Plain("啪！(" + str(round(WMRealTime_EndTime - WMRealTime_StartTime, 4)) + " 秒)")],ev.source)
        return
    return

@mirai_app.register("TempMessage")
async def on_tempmessage(app: Mirai, ev):
    WMLog4W().log_infon(ev)

@mirai_app.register("StrangerMessage")
async def on_strangermessage(app: Mirai, ev):
    WMLog4W().log_infon(ev)

@mirai_app.register("OtherClientMessage")
async def on_otherclientmessage(app: Mirai, ev):
    WMLog4W().log_infon(ev)

@mirai_app.register("BotInvitedJoinGroupRequestEvent")
async def on_newrequestevent(app: Mirai, ev):
    WMLog4W().log_info(ev)
        
@mirai_app.register("BotOnlineEvent")
async def on_botonlineeventt(app:Mirai, ev):
    WMLog4W().log_info(ev)

@mirai_app.register("BotOfflineEvent")
async def on_botofflineevent(app:Mirai, ev):
    WMLog4W().log_warn(ev)

@mirai_app.register("BotOfflineEventForce")
async def on_botofflineeventforce(app:Mirai, ev):
    WMLog4W().log_fail(ev)

@mirai_app.register("BotOfflineEventDropped")
async def on_botofflineeventdropped(app:Mirai, ev):
    WMLog4W().log_warn(ev)

@mirai_app.register("BotReloginEvent")
async def on_botreloginevent(app:Mirai, ev):
    WMLog4W().log_info(ev)

@mirai_app.register("FriendInputStatusChangedEvent")
async def on_friendinputstatuschangedevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("FriendNickChangedEvent")
async def on_friendnickchangedevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("FriendRecallEvent")
async def on_friendrecallevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("BotGroupPermissionChangeEvent")
async def on_botgrouppermissionchangeevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("BotMuteEvent")
async def on_botmuteevent(app:Mirai, ev):
    WMLog4W().log_warn(ev)

@mirai_app.register("BotUnmuteEvent")
async def on_botunmuteevent(app:Mirai, ev):
    WMLog4W().log_info(ev)

@mirai_app.register("BotJoinGroupEvent")
async def on_botjoingroupevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("BotLeaveEventActive")
async def on_botleaveeventactive(app:Mirai, ev):
    print(ev)

@mirai_app.register("BotLeaveEventKick")
async def on_botleaveeventkick(app:Mirai, ev):
    WMLog4W().log_warn(ev)

@mirai_app.register("GroupRecallEvent")
async def on_grouprecallevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("GroupNameChangeEvent")
async def on_groupnamechangeevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("GroupEntranceAnnouncementChangeEvent")
async def on_groupentranceannouncementchangeevent(app:Mirai, ev):
    print(ev)
    
@mirai_app.register("GroupMuteAllEvent")
async def on_groupmuteallevent(app:Mirai, ev):
    WMLog4W().log_warn(ev)
    
@mirai_app.register("GroupAllowAnonymousChatEvent")
async def on_groupallowanonymouschatevent(app:Mirai, ev):
    print(ev)
    
@mirai_app.register("GroupAllowConfessTalkEvent")
async def on_groupallowconfesstalkevent(app:Mirai, ev):
    print(ev)
    
@mirai_app.register("GroupAllowMemberInviteEvent")
async def on_groupallowmemberinviteevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("MemberJoinEvent")
async def on_memberjoinevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("MemberLeaveEventKick")
async def on_memberleaveeventkick(app:Mirai, ev):
    WMLog4W().log_info(ev)

@mirai_app.register("MemberLeaveEventQuit")
async def on_memberleaveeventquit(app:Mirai, ev):
    print(ev)

@mirai_app.register("MemberCardChangeEvent")
async def on_membercardchangeevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("MemberSpecialTitleChangeEvent")
async def on_memberspecialtitlechangeevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("MemberPermissionChangeEvent")
async def on_memberpermissionchangeevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("MemberMuteEvent")
async def on_membermuteevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("MemberUnmuteEvent")
async def on_memberunmuteevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("MemberHonorChangeEvent")
async def on_memberhonorchangeevent(app:Mirai, ev):
    print(ev)

@mirai_app.register("NudgeEvent")
async def on_NudgeEvent(app:Mirai, ev):
    WMLog4W().log_info(ev)

if __name__ == '__main__':
    WMLog4W().log_info("Done.")
    run_app(mirai_app)