import re
def is_all_numbers(string: str)-> bool:
    """
    判断字符串是否只包含数字
    :param string:
    :return:
    """
    for char in string:
        if not char.isdigit():
            return False
    return True

def is_meaningless(string: str):
    """
    判断字符串是否无意义
    :param string:
    :return:
    """
    if string is None or string == '' or len(string.strip()) == 0:
        return True
    else:
        return False

def is_contain_chinese(string: str)-> bool:
    """
    判断字符串是否包含中文
    :param string:
    :return:
    """
    for char in string:
        if '\u4e00' <= char <= '\u9fa5':
            return True
    return False

def is_only_contain_english_number_common_chars(string: str)-> bool:
    """
    判断字符串是否只包含英文、数字、常用字符
    :param string:
    :return:
    """
    pattern = r'^[a-zA-Z0-9\s\.,;:!?\'"\-_@#$%&*()+=<>[\]{}/\\|~`]+$'
    return bool(re.fullmatch(pattern, string))

def is_all_chinese(string: str)-> bool:
    """
    判断字符串是否只包含中文
    :param string:
    :return:
    """
    for char in string:
        if not '\u4e00' <= char <= '\u9fa5':
            return False
    return True

def is_contain_english(string: str)-> bool:
    """
    判断字符串是否包含英文
    :param string:
    :return:
    """
    for char in string:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            return True
    return False

def is_chinese_char(char):
    """检测CJK统一汉字及扩展区字符"""
    cp = ord(char)
    return any([
        0x4E00 <= cp <= 0x9FFF,  # 基本汉字
        0x3400 <= cp <= 0x4DBF,  # 扩展A
        0x20000 <= cp <= 0x2A6DF,  # 扩展B-F
        0x2A700 <= cp <= 0x2B73F,  # 扩展G
    ])


def is_english_char(char):
    """检测大小写英文字母"""
    return char.isalpha() and char.encode().isalpha()


def is_digit(char):
    """检测标准半角数字"""
    return char.isdecimal()

def is_contain_numbers(string: str)-> bool:
    """
    判断字符串是否包含数字
    :param string:
    :return:
    """
    for char in string:
        if char.isdigit():
            return True
    return False

def is_contain_chinese_or_english(string: str)-> bool:
    """
    判断字符串是否包含中文或英文
    :param string:
    :return:
    """
    for char in string:
        if is_contain_chinese(char) or is_contain_english(char):
            return True
    return False

def keep_chinese_and_english(text: str, language: str) -> str:
    # 匹配中文和英文（包括大小写字母和数字）
    if language == "zh":
        pattern = re.compile(r'[\u4e00-\u9fa5]')
    else:
        pattern = re.compile(r'[a-zA-Z]')
    result = ''.join(pattern.findall(text))
    return result