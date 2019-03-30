from nonebot import on_command, CommandSession
import dns
from dns import resolver


@on_command('dns', aliases=('域名', '查域名'), only_to_me=False)
async def dns_server(session: CommandSession):
    qname = session.get('qname', prompt='你想查询哪个域名的ip呢？')
    qname_input = await dns_requests(qname=qname)
    await session.send(qname_input)


@dns_server.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['qname'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的域名不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def dns_requests(qname: str) -> str:
    try:
        ip_address = dns.resolver.query(qname, 'A')
        ip_address_str = []
        cname_type = ip_address.response.answer[0].items[0]
        if isinstance(cname_type, dns.rdtypes.ANY.CNAME.CNAME):
            ip_address_str.append("CNAME结果:" + cname_type.to_text()+'\n')
            ip_address = resolver.query(cname_type.to_text(), 'A')
        if isinstance(ip_address.response.answer[0].items[0], dns.rdtypes.IN.A.A):
            ip_address_str.append("IP地址:\n")
            for i in ip_address.response.answer:
                for j in i.items:
                    ip_address_str.append(j.address + '\n')
            return "你要查询的域名是:{0} \n结果是 :\n{1} 耶！！！！！！！！".format(qname, "".join(ip_address_str))
        else:
            return "dns查询出错啦！！！！！！请主人检查域名是否输入规范，一般来说失败了就是暂无记录哦"
    except Exception as e:
        return "dns查询出错啦！！！！！！请主人检查域名是否输入规范，一般来说失败了就是暂无记录哦" + e.__str__()




