import random
import urllib
import json_repair
from base import BaseFormatTransform
from config_dict import ConfigDict
from config_llm import ConfigLLM
from utils import *
import base64
import leet

from openai import OpenAI


class BinaryTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        """二进制编码核心函数（保留符号，仅转换数字部分，并在二进制间加空格，每个二进制只保留后四位）"""
        s = str(data).strip()

        # 使用正则分割字符串为数字和非数字部分
        parts = re.split(r'(\D+)', s)  # \D+匹配非数字字符
        final = []

        for part in parts:
            if part.isdigit():
                # 数字部分转二进制，并在每个字符的二进制表示之间加空格，每个二进制只保留后四位
                try:
                    binary_parts = [bin(int(char))[2:].zfill(4)[-4:] for char in part]  # 去除0b前缀并填充至4位，只保留后四位
                    binary_str = ' '.join(binary_parts)
                    final.append(binary_str)
                except:
                    final.append(part)  # 异常保留原数字
            else:
                # 非数字部分直接保留
                final.append(part)

        return ''.join(final)

    def validate(self, data: str)->bool:
        return is_all_numbers(data) and not is_meaningless(data)

class OctalTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        """八进制编码核心函数（保留符号，仅转换数字部分，并在八进制间加空格）"""
        s = str(data).strip()

        # 使用正则分割字符串为数字和非数字部分
        parts = re.split(r'(\D+)', s)  # \D+匹配非数字字符
        final = []

        for part in parts:
            if part.isdigit():
                # 数字部分转八进制，并在每个字符的八进制表示之间加空格
                try:
                    octal_parts = [oct(int(char))[2:] for char in part]  # 去除0o前缀
                    octal_str = ' '.join(octal_parts)
                    final.append(octal_str)
                except:
                    final.append(part)  # 异常保留原数字
            else:
                # 非数字部分直接保留
                final.append(part)

        return ''.join(final)

    def validate(self, data: str)->bool:
        return is_all_numbers(data) and not is_meaningless(data)

class HexadecimalTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        """十六进制编码核心函数（保留符号，仅转换数字部分）"""
        s = str(data).strip()

        # 使用正则分割字符串为数字和非数字部分
        parts = re.split(r'(\D+)', s)  # \D+匹配非数字字符
        final = []

        for part in parts:
            if part.isdigit():
                # 数字部分转八进制
                try:
                    hex_num = hex(int(part))[2:]  # 去除0o前缀
                    final.append(hex_num)
                except:
                    final.append(part)  # 异常保留原数字
            else:
                # 非数字部分直接保留
                final.append(part)

        return ''.join(final)

    def validate(self, data: str)->bool:
        return is_all_numbers(data) and not is_meaningless(data)

class ASCIITransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        results = []
        for char in data:
            code = ord(char)
            if code > 127:
                # print(f"警告：非ASCII字符 '{char}' (U+{code:04X}) 被跳过")
                results.append(char)  # 使用 '?' 作为占位符
                continue
            # 格式化为0xXX的十六进制字符串
            hex_str = f"0x{code:02X}"
            results.append(hex_str)

        # 统一返回空格分隔的字符串
        return ' '.join(results)

    def validate(self, data: str)->bool:
        return is_only_contain_english_number_common_chars(data) and not is_meaningless(data)

class UnicodeTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        encoded_parts = []
        for char in data:
            # 生成Unicode转义序列，使用双反斜杠以确保输出为\u形式
            hex_code = f"\\u{ord(char):04x}"
            encoded_parts.append(hex_code)
        return "".join(encoded_parts)

    def validate(self, data: str)->bool:
        return not is_meaningless(data)

class UTF8Transform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        encoded = []
        for char in data:
            utf8_bytes = char.encode("utf-8")
            for byte in utf8_bytes:
                # 将每个字节转换为\xHH形式（HH为两位大写十六进制）
                encoded.append(f"\\x{byte:02X}")
        return "".join(encoded)

    def validate(self, data: str)->bool:
        return not is_meaningless(data)

class Base64Transform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        # 进行Base64编码
        data=data.encode("utf-8")
        encoded_data = base64.b64encode(data)
        # 返回解码为字符串的编码数据，以便于阅读或传输
        return encoded_data.decode('utf-8')

    def validate(self, data: str)->bool:
        return not is_meaningless(data)

class URLTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        return urllib.parse.quote(data)

    def validate(self, data: str)->bool:
       return not is_meaningless(data)

class HTMLEntityTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        return ''.join(f'&#x{ord(c):x};' for c in data)

    def validate(self, data: str)->bool:
        return not is_meaningless(data)

class MorseTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        return ' '.join(ConfigDict.CHARACTER_TO_MORSE_CODE_DICT.get(c.upper(), ' ') for c in data)

    def validate(self, data: str)->bool:
        return is_only_contain_english_number_common_chars(data)

class BrailleTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        return ''.join(ConfigDict.CHARACTER_TO_BRAILLE_DICT.get(c.upper(), '') for c in data)

    def validate(self, data: str)->bool:
        return is_only_contain_english_number_common_chars(data)

class NestedTransform(BaseFormatTransform):
    def transform(self, data: str) -> str:
        # 实例化可用的编码器
        transformers = [
            UnicodeTransform(),
            UTF8Transform(),
            Base64Transform(),
            HTMLEntityTransform()
        ]
        # 随机选择两个编码器
        first_transformer = random.choice(transformers)
        second_transformer = random.choice(transformers)
        # 第一次编码
        first_result = first_transformer.transform(data)
        # 第二次编码
        second_result = second_transformer.transform(first_result)
        return second_result

    def validate(self, data: str)->bool:
        return not is_meaningless(data)

class CharacterDecompositionTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        def decompose_char(char, dict_):
            """单个字符拆解函数"""
            decomposition = dict_.get(char)
            return ''.join(decomposition) if decomposition else char
        return ''.join([decompose_char(char, ConfigDict.CHINESE_CHARACTER_DECOMPOSITION_DICT) for char in str(data)])

    def validate(self, data: str)->bool:
        return is_contain_chinese(data)

class TextInversionTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        result = []
        for char in data[::-1]:
            result.append(char)
        return ''.join(result)

    def validate(self, data: str)->bool:
        return not is_meaningless(data)

class MartianTextTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        result = []
        for char in data:
            # 处理优先级：中文 > 英文 > 数字 > 符号
            if is_chinese_char(char):
                result.append(
                    ConfigDict.SIMPLIFIED_CHINESE_TO_LEET_DICT.get(char, ConfigDict.TRADITIONAL_CHINESE_TO_LEET_DICT.get(char, char))
                )
            elif is_english_char(char):
                result.append(leet.leet(char) or char)
            elif is_digit(str(char)):
                result.append(ConfigDict.NUMBER_TO_LEET_DICT.get(char, char))
            else:
                result.append(char)  # 保留所有符号

        return ''.join(result)

    def validate(self, data: str)->bool:
        return not is_meaningless(data)

class SimplifiedToTraditionalChineseTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        result = []
        for char in data:
            if is_chinese_char(char):
                result.append(
                    ConfigDict.SIMPLIFIED_CHINESE_TO_TRADITIONAL_CHINESE_DICT.get(char, ConfigDict.SIMPLIFIED_CHINESE_TO_TRADITIONAL_CHINESE_DICT.get(char, char))
                )
            else:
                result.append(char)  # 保留所有符号

        return ''.join(result)

    def validate(self, data: str)->bool:
        return is_contain_chinese(data)

class NumericalCapitalizationTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        return ''.join(ConfigDict.NUMBER_TO_CHINESE_UPPERCASE_DICT.get(c, c) for c in data)

    def validate(self, data: str)->bool:
        return is_contain_numbers(data)

class InsertingSpecialCharactersTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        mixed_pool = ConfigDict.EMOJIS_LIST + ConfigDict.SPECIAL_SYMBOLS_LIST
        num_inserts = random.randint(1, ConfigDict.MAX_INSERTS_NUM)
        text_list = list(data)

        # 随机插入符号[3,5](@ref)
        for _ in range(num_inserts):
            pos = random.randint(0, len(text_list))
            symbol = random.choice(mixed_pool)
            text_list.insert(pos, symbol)

        return ''.join(text_list)

    def validate(self, data: str)->bool:
        return not is_meaningless(data)

class InsertingChineseCharactersTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        # 找出所有英文/数字字符的位置
        candidates = [i for i, char in enumerate(data) if char.isalnum()]

        if not candidates:
            return data

        # 随机选择插入位置
        insert_pos = random.choice(candidates) + 1
        # 随机选择热词
        hotword = random.choice(ConfigDict.CHINESE_HOT_WORDS_LIST)

        return data[:insert_pos] + hotword + data[insert_pos:]

    def validate(self, data: str)->bool:
        return not is_meaningless(data)

class InsertingEnglishLettersNumbersTransform(BaseFormatTransform):
    def transform(self, data: str)-> str:
        # 找出所有汉字的位置（Unicode范围：4E00-9FFF）
        candidates = [i for i, char in enumerate(data) if '\u4e00' <= char <= '\u9fff']

        if not candidates:
            return data

        # 随机选择插入位置（在汉字之后插入）
        insert_pos = random.choice(candidates) + 1
        # 随机选择英文/数字热词
        hotword = random.choice(ConfigDict.ENGLISH_HOT_WORDS_LIST)

        return data[:insert_pos] + hotword + data[insert_pos:]

    def validate(self, data: str)->bool:
        return not is_meaningless(data)


class AcrosticPoetryTransform(BaseFormatTransform):
    chinese_system = """
    你是一个擅长使用中文生成藏头诗的汉语言文学大师。
    """
    chinese_user = """
    根据输入文字生成藏头诗，要求：
    1.每句首字按顺序使用输入文字每句7个字
    2.句子的个数与输入中汉字文字的字数相同，例如输入是3个汉字，你生成的输出句子应该只有3句。
    3.你只需要关注输入的中文即可，输出的句子的首个字的顺序与输入的中文汉字的顺序一致。
    
    [输出格式]
    以json格式输出
    {   
        "split_characters_in_order": list[str] //输入的中文汉字顺序拆分至list中
        "sentences": list[str] //生成的藏头诗句子，每个句子一个list元素，每个句子7个字
    }
    
    示例：
    输入：人工智能
    提示：人工智能，split_characters_in_order：["人","工","智","能"]，请严格参考
    输出：
    {   
        "split_characters_in_order": ["人","工","智","能"],
        "sentences": list["人寰万象入云巅","工巧难量道德边","智启星河应有度","能持玉衡守方圆"]
    }
    
    输入为：$input
    提示：$input，split_characters_in_order：$split_filter_characters_in_order，请严格参考
    输出：
    """
    english_system = """
    You are a poet skilled at crafting English acrostic poems.
    """
    english_user = """
    Generate an English acrostic poem where:
    1.The English acrostic poem should begin with each letter of input, generating one sentence per letter.
    2.The number of sentences should match the number of letters in the input. For example, if the input contains 3 letters, your output should consist of exactly 3 sentences.
    3.You only need to focus on the input letters—the first character of the output sentences must follow the exact order of the input letters.
    4. dont pay attention to the meaning of the input, just generate a poem based on the letters. dont let spaces or other Non-English characters between letters affect the output.
    
    [output format]
    write in json format
    {   
        "split_characters_in_order": list[str] //The input letters should be split into a list in the order they appear.
        "sentences": list[str] //The generated acrostic poem lines should each be a separate element in a list.
    }
    
    Example: 
    input: Hope
    hint: Hope, split_characters_in_order: ["H","o","p","e"], Please refer strictly.
    Output:
    {   
        "split_characters_in_order": ["H","o","p","e"],
        "sentences": ["Holding on through the darkest nights","Opening hearts to let in the light","Pushing forward, step by steady step","Embracing dreams that never sleep"]
    }
    
    input: zhang 3san feng
    hint: zhang 3san feng, split_characters_in_order: ["z","h","a","n","g","s","a","n","f","e","n","g"], Please refer strictly.
    Output:
    {   
        "split_characters_in_order"： ["z","h","a","n","g","s","a","n","f","e","n","g"],
        "sentences": [
            "Zen-like wisdom, calm yet deep",
            "Harmony in motion, soft yet steep",
            "Art of balance, fist and flow",
            "Nature’s rhythm, fast then slow",
            "Grandmaster’s touch—gentle, strong",
            "Still as mountains, patient long",
            "Alchemy of mind and breath",
            "Neutral force defies death",
            "Floating clouds, his palm’s embrace",
            "Eternal Dao, time and space",
            "No desire, yet all achieved",
            "Grace in stillness—truth perceived"
        ]
    }
    
    input: $input
    hint: $input, split_characters_in_order: $split_filter_characters_in_order, Please refer strictly.
    output:
    """

    def poem_generator(self, input_str: str, language: str) -> str:
        """
        Generate a poem based on the input string and language.
        """
        client = OpenAI(
            api_key=ConfigLLM.API_KEY,
            base_url=ConfigLLM.BASE_URL
        )
        try:
            if language == "zh":
                system = self.chinese_system
                user = self.chinese_user
            else:
                system = self.english_system
                user = self.english_user

            response = client.chat.completions.create(
                model=ConfigLLM.MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user.replace("$input", input_str).replace("$split_filter_characters_in_order", str(list(keep_chinese_and_english(input_str, language))))+" /no_think"},
                ],
                stream=False
            )

            content = response.choices[0].message.content
            content_json = json_repair.loads(content)
        except:
            content_json = {
                "split_characters_in_order": ["$error$"],
                "sentences": ["$error$"]
            }
        if "sentences" in content_json and isinstance(content_json["sentences"], list):
            return "\n".join(content_json["sentences"])
        else:
            raise ValueError("'sentences' not found in the response.")

    def transform(self, data: str)-> str:
        language = "en"
        if is_contain_chinese(data):
            language = "zh"
        return self.poem_generator(data, language)

    def validate(self, data: str)->bool:
        return is_contain_chinese_or_english(data)
