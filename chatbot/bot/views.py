from django.shortcuts import render
from .forms import BotForm
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import os

def home(request):
    return render(request, 'bot/home.html', {'title': 'Home'})



def botpage(request):

    os.environ["OPENAI_API_KEY"] = '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'

    def construct_index(directory_path):
        max_input_size = 4096
        num_outputs = 512
        max_chunk_overlap = 20
        chunk_size_limit = 600

        prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

        documents = SimpleDirectoryReader(directory_path).load_data()

        index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

        index.save_to_disk('index.json') 

        return index

    index = construct_index("/home/shaun/chatbot/chatbot/bot/docs")

    def chatbot(input_text):
        index = GPTSimpleVectorIndex.load_from_disk('index.json')
        response = index.query(input_text, response_mode="compact")
        return response.response

    message = ''
    if request.method == "POST":
        form = BotForm(request.POST)
        if form.is_valid():
            message = chatbot(form.cleaned_data["message"])
    else:
        form = BotForm()

        
    context = {
        'title': 'Bot Page',
        'form': form,
        'message': message,
    }

    return render(request, 'bot/bot-page.html', context)


