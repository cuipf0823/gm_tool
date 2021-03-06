#!/usr/bin/python
# coding=utf-8

import time
from collections import OrderedDict
from .common import *
from ..proto import gm_pb2
from ..proto import error_code_pb2 as pb_error
import logging


def timestamp_datetime(value):
    ft = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    return time.strftime(ft, value)


def format_output(header, rsp):
    if header.msg_name.decode('utf-8') == 'gms.GMQueryUnsendMailRsp':
        output = []
        for item in rsp.mail_contents:
            ft_str = "mail_id:{mail_id}\ntitle: {title}\nreceiver_type:{addressee_type} mail_type:{mail_type} " \
                     "defined_content:{defined_content}\nis_destroy:{is_destroy} show_priority:{show_priority} " \
                     "is_popping:{is_popping}\nvalid_time:{valid_time}\ndelayed_time:{delayed_time}\n" \
                     "sender: {sender}\ncontent: {content}\n".format(mail_id=item.mail_id,
                                                                     title=item.title.decode('utf-8'),
                                                                     addressee_type=item.addressee_type,
                                                                     mail_type=item.mail_type,
                                                                     defined_content=item.defined_content,
                                                                     is_destroy=item.is_destroy,
                                                                     show_priority=item.show_priority,
                                                                     is_popping=item.is_popping,
                                                                     valid_time=timestamp_datetime(item.valid_time),
                                                                     delayed_time=timestamp_datetime(item.delayed_time),
                                                                     sender=item.sender.decode('utf-8'),
                                                                     content=item.content.decode('utf-8'))
            output.append(ft_str)
        return '\n'.join(mail_info for mail_info in output)
    return rsp


def handle_response(tcp_connect, header, req):
    status_code = tcp_connect.send(Interact.encode(header, req))
    if status_code:
        logging.error('send msg {} to gm server failed !'.format(req.DESCRIPTOR.full_name))
        return QueryRet(StatusCode.SOCK_SEND_ERROR, req, StatusCode.status_desc(StatusCode.SOCK_SEND_ERROR))
    logging.debug(header)
    logging.debug(req)
    status_code, data = tcp_connect.recv()
    if status_code:
        logging.error('receive gm server response message failed !')
        return QueryRet(StatusCode.SOCK_RECEIVE_ERROR, req, StatusCode.status_desc(StatusCode.SOCK_RECEIVE_ERROR))
    header, rsp = Interact.decode(data)
    logging.debug(header)
    logging.debug(rsp)
    if header.errcode:
        err_desc = 'send msg {0} to gm server error {1}:{2}!'.format(req.DESCRIPTOR.full_name, header.errcode,
                                                                     pb_error.GMErrorCode.Name(header.errcode))
        logging.error(err_desc)
        return QueryRet(header.errcode, req, err_desc)
    if not str(rsp):
        rsp = 'GM Server return empty!'
        return QueryRet(StatusCode.SUCCESS, req, rsp)
    return QueryRet(StatusCode.SUCCESS, req, format_output(header, rsp))


# 无需参数
def list_server(user):
    req = gm_pb2.GMGetAllServerListReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    return header, req


def register_num(user):
    req = gm_pb2.GMGetServerRegisterNumberReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    return header, req


def online_status(user):
    req = gm_pb2.GMGetOnlineInSwitchReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    return header, req


def tunnel(user):
    req = gm_pb2.GMGetTunnelServerInfoReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    return header, req


# 需要uid， channel
def query_player(user, uid, channel=0):
    req = gm_pb2.GMQueryUserReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.players.uid = uid
    req.players.channel = channel
    return header, req


def query_online(user, uid, channel=0):
    req = gm_pb2.GMQueryUserOnlineReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    info = req.players.add()
    info.uid = uid
    info.channel = channel
    return header, req


def kick_player(user, uid, channel=0):
    req = gm_pb2.GMKickUserReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.uid = uid
    req.channel = channel
    return header, req


def player_detail(user, uid, channel=0):
    req = gm_pb2.GMQueryOnlineUserInfoReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.uid = uid
    req.channel = channel
    return header, req


def craft_info(user, uid, channel=0):
    req = gm_pb2.GMGetPlayerCraftInfoReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.uid = uid
    req.channel = channel
    return header, req


def friend_list(user, uid, channel=0):
    req = gm_pb2.GMGetFriendListReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.uid = uid
    req.channel = channel
    return header, req


def black_list(user, uid, channel=0):
    req = gm_pb2.GMGetBlackListReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.uid = uid
    req.channel = channel
    return header, req


def push_list(user, uid, channel=0):
    req = gm_pb2.GMGetPushListReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.uid = uid
    req.channel = channel
    return header, req


def query_user_info(user, server_id):
    req = gm_pb2.GMQueryAllUserBaseInfoOnlineReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.server_id = server_id
    return header, req


def all_room(user, server_id):
    req = gm_pb2.GMGetAllServerRoomReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.server_id = server_id
    return header, req


def room_info(user, server_id, room_id):
    req = gm_pb2.GMGetRoomInfoReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.server_id = server_id
    req.room_id = room_id
    return header, req


def send_mail(user, mail_info):
    logging.debug('send mail to gm server mail info: {}'.format(mail_info))
    '''
    status = True
    if status:
        return
    '''
    req = gm_pb2.GMSendMailReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    mail = req.mail_content
    mail.gm_uid = Interact.gid
    mail.addressee_type = mail_info.get('receive_type')
    if mail.addressee_type == 1:
        for online_id in mail_info.get('receive_onlines', []):
            mail.online_ids.append(online_id)
    elif mail.addressee_type == 2:
        mail.online_ids.append(mail_info.get("receive_online", 0))
        for uid in mail_info.get('receive_uids', []):
            mail.uids.append(uid)
            mail.channels.append(0)
    mail.sender = mail_info.get('sender').encode('utf-8')
    mail.title = mail_info.get('title').encode('utf-8')
    mail.content = mail_info.get('content').encode('utf-8')
    mail.valid_time = mail_info.get('valid_time')
    mail.is_destroy = mail_info.get('is_destory')
    mail.show_priority = (gm_pb2.MailContent.Top if mail_info.get('priority')
                          else gm_pb2.MailContent.Normal)
    mail.is_popping = mail_info.get('is_popping')
    mail.delayed_time = mail_info.get('delayed_time')
    for item in mail_info.get('attachments', []):
        attachment = mail.attachment_list.add()
        attachment.id = item[0]
        attachment.count = item[1]
    if len(mail.attachment_list) != 0:
        mail.mail_type = 1
    else:
        mail.mail_type = 0
    return header, req


def unsend_mail(user):
    req = gm_pb2.GMQueryUnsendMailReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    return header, req


def del_unsend_mail(user, mail_id):
    req = gm_pb2.GMDeleteUnsendMailReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.mail_ids.append(mail_id)
    return header, req


def get_vaild_mail(user):
    req = gm_pb2.GMCheckValidMailReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    return header, req


def del_send_mail(user, mail_id):
    req = gm_pb2.GMDeleteSendMailReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name, user.gateway_session)
    req.mail_ids.append(mail_id)
    return header, req


#########################
def handle_list_server(rsp):
    servers = []
    if str(rsp):
        for item in rsp.server_items:
            if item.server_type == 2:
                servers.append(item.zone_id)
    logging.debug('handle_list_server update servers: {}'.format(servers))
    return servers


def handle_online_server(rsp):
    servers = []
    if str(rsp):
        for item in rsp.servers:
            servers.append(item.server_id)
    logging.debug('handle_online_server update servers: {}'.format(servers))
    return servers


class CallBackType:
    PARAM_NONE = 0
    PARAM_UID_CHANNEL = 1
    PARAM_SERVER_ID = 2
    PARAM_MAIL = 3
    PARAM_MAIL_ID = 4
    PARAM_ROOM_INFO = 5

    def __init__(self):
        pass


class QueryRet:
    status_code = 0
    request = None
    response = None

    def __init__(self, status_code, req, rsp):
        self.status_code = status_code
        self.request = req
        self.response = rsp


class Operations:
    # send message without params
    OPT_LIST_SERVER = 'list'
    OPT_ONLINES_SERVER = 'list_onlines'
    OPT_REGISTER_NUM = 'reg_num'
    OPT_TUNNEL_INFO = 'tunnel'
    OPT_QUERY_PLAYER = 'query_player'
    OPT_PLAYER_DETAIL = 'player_detail'
    OPT_CRAFT_INFO = 'craft_info'
    OPT_FRIEND_LIST = 'friend_list'
    OPT_BLACK_LIST = 'black_list'
    OPT_PUSH_LIST = 'push_list'
    OPT_KICK_PLAYER = 'kick_player'
    OPT_ALL_PLAYERS = 'all_players'
    OPT_ALL_ROOMS = 'all_rooms'
    OPT_ROOM_INFO = 'room_info'
    OPT_SEND_MAIL = 'send_mail'
    OPT_UNSEND_MAIL = 'unsend_mail'
    OPT_VALID_MAIL = 'vaild_mail'
    OPT_DEL_UNSEND_MAIL = 'del_unsend_mail'
    OPT_DEL_SEND_MAIL = 'del_send_mail'

    operations_desc = OrderedDict()
    operations_rsps = OrderedDict()
    operations_desc[OPT_LIST_SERVER] = ('查询全部有效服务器', list_server, CallBackType.PARAM_NONE)
    operations_desc[OPT_ONLINES_SERVER] = ('查询全部online信息', online_status, CallBackType.PARAM_NONE)
    operations_desc[OPT_REGISTER_NUM] = ('查询注册人数', register_num, CallBackType.PARAM_NONE)
    operations_desc[OPT_TUNNEL_INFO] = ('查询tunnel信息', tunnel, CallBackType.PARAM_NONE)

    operations_desc[OPT_QUERY_PLAYER] = ('查询玩家所在服务器', query_player, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_PLAYER_DETAIL] = ('查询玩家详细信息', player_detail, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_CRAFT_INFO] = ('查询玩家星球信息', craft_info, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_FRIEND_LIST] = ('查询玩家好友列表', friend_list, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_BLACK_LIST] = ('查询玩家黑名单列表', black_list, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_PUSH_LIST] = ('查询玩家推送列表', push_list, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_KICK_PLAYER] = ('强制玩家下线', kick_player, CallBackType.PARAM_UID_CHANNEL)

    operations_desc[OPT_ALL_PLAYERS] = ('查询所有在线用户', query_user_info, CallBackType.PARAM_SERVER_ID)
    operations_desc[OPT_ALL_ROOMS] = ('查询当前所有房间', all_room, CallBackType.PARAM_SERVER_ID)
    operations_desc[OPT_ROOM_INFO] = ('查询房间信息', room_info, CallBackType.PARAM_ROOM_INFO)
    operations_desc[OPT_SEND_MAIL] = ('发送官方邮件', send_mail, CallBackType.PARAM_MAIL)
    operations_desc[OPT_UNSEND_MAIL] = ('获取未发送邮件', unsend_mail, CallBackType.PARAM_NONE)
    operations_desc[OPT_VALID_MAIL] = ('获取全部有效邮件', get_vaild_mail, CallBackType.PARAM_NONE)
    operations_desc[OPT_DEL_UNSEND_MAIL] = ('删除未发送邮件', del_unsend_mail, CallBackType.PARAM_MAIL_ID)
    operations_desc[OPT_DEL_SEND_MAIL] = ('删除已发送邮件', del_send_mail, CallBackType.PARAM_MAIL_ID)

    operations_rsps[OPT_LIST_SERVER] = handle_list_server
    operations_rsps[OPT_ONLINES_SERVER] = handle_online_server

    def __init__(self):
        pass

    @classmethod
    def operations(cls):
        return cls.operations_desc

    @classmethod
    def callback(cls, opt, user, **kwargs):
        opt_info = cls.operations_desc.get(opt, None)
        if opt_info is None:
            return None
        header, req = opt_info[1](user, **kwargs)
        return handle_response(user.connect_gm, header, req)

    @classmethod
    def rsp_callback(cls, opt, rsp):
        cb = cls.operations_rsps.get(opt, None)
        if cb is None:
            return None
        return cb(rsp)
