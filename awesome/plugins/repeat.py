from nonebot import on_command, CommandSession


@on_command('repeat', aliases=('复读', '复读机'), only_to_me=False)
async def repeat(session: CommandSession):
    repeat_string = session.get('repeat_string', prompt='/复读')

    await session.send(repeat_string)


@repeat.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['repeat_string'] = stripped_arg
        return

    if not stripped_arg:

        session.pause('！！！！！！！！！！')

    session.state[session.current_key] = stripped_arg
