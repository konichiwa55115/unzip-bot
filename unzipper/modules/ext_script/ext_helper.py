# Copyright (c) 2023 EDM115
import os
from asyncio import get_running_loop
from functools import partial
from subprocess import PIPE
from subprocess import Popen

from pykeyboard import InlineKeyboard
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton

from unzipper import LOGGER


def __run_cmds_unzipper(command):
    ext_cmd = Popen(command["cmd"], stdout=PIPE, stderr=PIPE, shell=True)
    ext_out = ext_cmd.stdout.read()[:-1].decode("utf-8")
    LOGGER.info(ext_out)
    return ext_out


async def run_cmds_on_cr(func, **kwargs):
    loop = get_running_loop()
    return await loop.run_in_executor(None, partial(func, kwargs))


# Extract with 7z
async def _extract_with_7z_helper(protected, path, archive_path, password=None):
    if password:
        command = f'7z x -o{path} -p"{password}" {archive_path} -y'
    else:
        testcommand = f'7z t {archive_path} -p"IAmVeryProbablySureThatThisPasswordWillNeverBeUsedElseItsVeryStrangeAAAAAAAAAAAAAAAAAAA" -y' # skipcq: FLK-E501
        testoutput = await run_cmds_on_cr(__run_cmds_unzipper, cmd=testcommand)
        if "Everything is Ok" in testoutput:
            command = f"7z x -o{path} {archive_path} -y"
        else:
            command = "echo 'This archive is password protected'"
            protected = True
    return await run_cmds_on_cr(__run_cmds_unzipper, cmd=command)


# Extract with zstd (for .zst files)
async def _extract_with_zstd(path, archive_path):
    command = f"zstd -f --output-dir-flat {path} -d {archive_path}"
    return await run_cmds_on_cr(__run_cmds_unzipper, cmd=command)


# Main function to extract files
async def extr_files(protected, path, archive_path, password=None):
    file_path = os.path.splitext(archive_path)[1]
    if file_path == ".zst":
        os.mkdir(path)
        ex = await _extract_with_zstd(path, archive_path)
        return ex
    ex = await _extract_with_7z_helper(protected, path, archive_path, password)
    return ex


# Split files
async def split_files(iinput, ooutput):
    # Workaround : https://ccm.net/computing/linux/4327-split-a-file-into-several-parts-in-linux/
    command = f"split -a 3 -e --numeric-suffixes=001 -b 2GB {iinput} {ooutput}"
    await run_cmds_on_cr(__run_cmds_unzipper, cmd=command)
    spdir = ooutput.replace("/" + ooutput.split("/")[-1], "")
    splittedfiles = await get_files(spdir)
    LOGGER.info(splittedfiles)
    return splittedfiles


# Get files in directory as a list
async def get_files(path):
    path_list = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)] for val in sublist] # skipcq: FLK-E501
    return sorted(path_list)


# Make keyboard
async def make_keyboard(paths, user_id, chat_id):
    num = 0
    i_kbd = InlineKeyboard(row_width=1)
    data = []
    data.append(InlineKeyboardButton(
        "Upload all 📤", f"ext_a|{user_id}|{chat_id}"))
    data.append(InlineKeyboardButton("❌ Cancel", "cancel_dis"))
    for file in paths:
        if num > 96:
            break
        data.append(
            InlineKeyboardButton(
                f"{num} - {os.path.basename(file)}".encode(
                    "utf-8").decode("utf-8"),
                f"ext_f|{user_id}|{chat_id}|{num}",
            )
        )
        num += 1
    i_kbd.add(*data)
    return i_kbd


async def make_keyboard_empty(user_id, chat_id):
    i_kbd = InlineKeyboard(row_width=2)
    data = []
    data.append(InlineKeyboardButton(
        "Upload all 📤", f"ext_a|{user_id}|{chat_id}"))
    data.append(InlineKeyboardButton("❌ Cancel", "cancel_dis"))
    i_kbd.add(*data)
    return i_kbd
