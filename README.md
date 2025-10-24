# Format Transformation Logic for DataSIR

## Simple Introduction

We support the following transformation logic:
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

You can refer to the paper **"DataSIR:A Benchmark Dataset for Sensitive Information Recognition"** accepted by **NeruIPS 2025** for more details.

## Dependencies and Model Configurations

### NLP Libraries and Models

| Package/Model Name | Version | Parameter Settings |
|-------------------|---------|-------------------|
| HanLP | 2.1.1 | `hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH` |
| spaCy | 3.8.4 | `en_core_web_sm` / `zh_core_web_sm` |
| NLTK | 3.8.1 | `averaged_perceptron_tagger` |
| Presidio | 2.2.359 | `hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH` / `en_core_web_sm` |

### LLM API Configurations

| Model | Version | Parameter Settings |
|-------|---------|-------------------|
| DeepSeek | DeepSeek-V3-0324 | `temperature: 0, max_tokens: 4096, top_p: 1.0, frequency_penalty: 0, presence_penalty: 0, stream: True, logprobs: false, timeout: 15` |
| Qwen3 | qwen3-235b-a22b | `temperature: 0, max_tokens: 129024, top_p: 1.0, top_k: 0, presence_penalty: 0.5, stream: True, timeout: 15, seed: 1234` |
| GPT | gpt-4.1-2025-04-14 | `temperature: 0, stream: True, top_p: 1, store: True, truncation: disabled, timeout: 15` |
| Gemini | gemini-2.5-flash-preview-04-17 | `temperature: 0, stream: True, top_p: 0.95, top_k: 64, candidateCount: 1, timeout: 15` |

## How to use

```python
from format_transform.transform import *
input_text = "Hello World!"
output_text = Base64Transform().apply_transform(input_text)
print(output_text)
```

You can modify the code in `format_transform/config_dict.py` to expand the content of dictionary.

You can set your api key in `format_transform/config_llm.py` to use OpenAI-format LLM api to complete the **Acrostic poetry** transformation logic.
