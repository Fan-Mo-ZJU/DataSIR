# Format Transformation Logic for DataSIR
## Simple Introduction
we support the following transformation logic:
- Binary
- Octal
- Hexadecimal
- ASCII encoding
- Unicode encoding
- UTF-8 encoding
- Base64 encoding
- URL encoding
- HTML entity encoding
- Morse encoding
- Braille encoding
- Nested encoding
- Acrostic poetry
- Character decomposition
- Text inversion
- Martian text
- Simplified to traditional Chinese
- Numerical capitalization
- Inserting special characters
- Inserting Chinese characters
- Inserting English letters/numbers

You can refer to the paper **"DataSIR:A Benchmark Dataset for Sensitive Information Recognition"** for more details.
# How to use
```python
from format_transform.transform import *
input_text = "Hello World!"
output_text = Base64Transform().apply_transform(input_text)
print(output_text)
```
You can modify the code in `format_transform/config_dict.py` to expand the content of dictionary.

You can set your api key in `format_transform/config_llm.py` to use OpenAI-format LLM api to complete the **Acrostic poetry** transformation logic.
