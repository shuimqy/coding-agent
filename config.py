from langchain_openai import ChatOpenAI

api_key = ""
base_url = ""
model_name = ""

# 初始化 LLM (建议用长文本能力强的模型)
llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model=model_name,
)
