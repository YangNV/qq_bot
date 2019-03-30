from nonebot import on_command, CommandSession
from random import randint


@on_command('choose', aliases=('二选一', '抉择'), only_to_me=False)
async def choose_from(session: CommandSession):
    choose_result_string = session.get('choose_string', prompt='请输入候选名单')
    choose_result = await get_choose_result(choose_result_string)
    await session.send(choose_result)


@choose_from.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['choose_string'] = stripped_arg
        return

    if not stripped_arg:
        session.pause(' ')
    session.state[session.current_key] = stripped_arg


async def get_choose_result(choose_result_string: str) -> str:
    options = choose_result_string.split()
    result_option = options[randint(0, len(options) - 1)]
    return "命运的选择就是{0}啦！！！！！！！！！".format(result_option)
