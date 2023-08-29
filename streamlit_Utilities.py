import openai
import requests
from PIL import Image
import re
import ast
import os
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import load_tools
import tempfile
import io
import streamlit as st

openapi_key = st.secrets["open_ai_key"]
openai.api_key = openapi_key
# OpenAI = openapi_key

serpapi_api_key = st.secrets["serp_api_key"]
# SerpAPIWrapper.api_key=serpapi_api_key
print(serpapi_api_key)


#function for blog structure
def generate_Blog_Structure(topic):
    messages = [
    {"role": "system", "content": f"""You are trained to analyze a {topic} and generate the structure of a blog post depending upon the topic.First analyze the (Language) of {topic} and responsed must be in same language.If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.Response must be in the same language as the language of {topic}"""},
    {"role": "user", "content": f"""Analyze the topic and generate the structure of a blog post. The topic is {topic}
                                    First analyze the (Language) of {topic} and responsed must be in same language.If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.Generate a structure to help generate a post on that. The structure would varry on the topic.Response must be in the same language as the language of {topic}"""}
    ]

    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-16k",
                        messages=messages, 
                        max_tokens= 3000, 
                        n=1, 
                        stop=None, 
                        temperature=0.6)

    response_text = response.choices[0].message.content.strip()
    print(response_text)
    return response_text

#function for blog content
def generate_Blog_Content(topic, structure):
    messages = [
    {"role": "system", "content": f"""You are trained to analyze a {topic} and generate a blog post depending on the given {structure}.First analyze the (Language) of {topic} and {structure} and responsed must be in same language.If {topic} and {structure} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.Response should be in the same language as {topic} and {structure}"""},
    {"role": "user", "content": f"""Analyze the topic and generate a blog post. The topic is {topic}. The Structure is: {structure}
                                    The Blog post must contain 2000 to 3000 words.Strictly follow the structure given to you.First analyze the (Language) of {topic} and responsed must be in same language.If {topic} and {structure} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.Response should be in the same language as {topic} and {structure}"""}
    ]


    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-16k",
                        messages=messages, 
                        max_tokens= 3000, 
                        n=1, 
                        stop=None, 
                        temperature=0.5)

    response_text = response.choices[0].message.content.strip()

    return response_text

#function for twitter content

def generate_Twitter_content(topic):
    messages = [
    {"role": "system", "content": f"""You are trained to analyze a topic and generate a Twitter post without adding (emojis) in the post.First analyze the (Language) of {topic} and responsed must be in same language.If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.follow this instruction Rigorously.Response should be in the same language as {topic}."""},
    {"role": "user", "content": f"""Analyze the topic and generate a twitter post without any (emojis). The Topic is: {topic}.
                                    Follow the intructions:
                                    1.Response should be in the same language as {topic}.
                                    2.If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.
                                    3. Shape it like a tweet without containing any (emojis).  
                                    4. Do not Add any type of (emojis).                                                                    
                                    5. If relevant, you can include hashtags to categorize your tweet and make it more discoverable but do not add (emojis).
                                    6. It should not generate any harmful text.                             
                                    7.Rigorously follow (2) instruction."""}
    ]
    # messages = [
    # {"role": "system", "content": """You are trained to analyze a topic and generate a Twitter post."""},
    # {"role": "user", "content": f"""Analyze the topic and generate a twitter post. The Topic is: {topic}.
    #                                 Follow the intructions:
    #                                 1. Shape it like a tweet.
    #                                 2. If relevant, you can include hashtags to categorize your tweet and make it more discoverable.
    #                                 3. You can add Emojis where its relevant.
    #                                 4. It should not generate any harmful text.
    #                                 5. Do not Add the (emojis) """}
    # ]
    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages, 
                        max_tokens= 60, 
                        n=1, 
                        stop=None, 
                        temperature=0.6)

    response_text = response.choices[0].message.content.strip()

    return response_text

#function for Instagram content
def generate_Instagram_content(topic):
    messages = [
    {"role": "system", "content": f"""You are trained to analyze a topic and generate an Instagram caption without adding (emojis) in the caption.First analyze the (Language) of {topic} and responsed must be in same language.If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.follow this instruction precisely.Response must be in the same language as {topic}"""},
    {"role": "user", "content": f"""Analyze the topic and generate an instagram caption without any kind of (emojis). The Topic is: {topic}.
                                    Follow the instruction:
                                    1. Response should be in the same language as {topic}.
                                    2. If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.
                                    3. Shape it like an instagram caption without containing any (emojis).
                                    4. Do not Add the (emojis) in caption.
                                    5. Add a catchy opening line (Not more than one line, not any emojis).
                                    6. Generate text relevant to the topic.
                                    7. If relevant, you can include hashtags to categorize your post and make it more discoverable but not (emojis).
                                    8. It should not generate any harmful text.
                                    9. Rigorously Follow (2) instruction."""}
    ]

    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages, 
                        max_tokens= 440, 
                        n=1, 
                        stop=None, 
                        temperature=0.6)

    response_text = response.choices[0].message.content.strip()

    return response_text

#function for facebook content
def generate_Facebook_content(topic):
    # messages = [
    # {"role": "system", "content": """You are trained to analyze a topic and generate an Facebook post without containing any (emojis) in the post.follow this instruction precisely."""},
    # {"role": "user", "content": f"""Analyze the topic and generate a Facebook post. The topic is: {topic}.
    #                                 Follow the instructions:
    #                                 1. Shape it like a Facebook Post without containing any (emojis).
    #                                 2. Do not Add the (emojis)
    #                                 3. Add a Catchy opening line (Not more than one line).
    #                                 4. Generate text relevent to the topic. (Decide the size of the text depending upon the topic).
    #                                 5. If relevant, you can include hashtags to categorize your post and make it more discoverable but not (emojis).
    #                                 6. It should not generate any harmful text.
    #                                 7. Rigorously Follow (2) instruction."""}
    # ]
    messages = [
    {"role": "system", "content": f"""You are trained to analyze a topic and generate a Facebook post without containing any (emojis) in the post.First analyze the (Language) of {topic} and responsed must be in same language.If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}. Follow this instruction precisely.Response should be in the same language as {topic}"""},
    {"role": "user", "content": f"""Analyze the topic and generate a Facebook post. The topic is: {topic}.
                                    Follow the instructions:
                                    1. Response should be in the same language as {topic}.
                                    2. If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.
                                    3. Shape it like a Facebook Post without containing any kind of (emojis).
                                    4. Do not add the (emojis).
                                    5. Add a catchy opening line (Not more than one line).
                                    6. Generate text relevant to the topic. (Decide the size of the text depending upon the topic).
                                    7. If relevant, you can include hashtags to categorize your post and make it more discoverable but not (emojis).
                                    8. It should not generate any harmful text.
                                    9. Rigorously follow instruction (2)."""}
    ]

    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages, 
                        max_tokens= 3000, 
                        n=1, 
                        stop=None, 
                        temperature=0.6)

    response_text = response.choices[0].message.content.strip()

    return response_text
#function for Linkedin content
def generate_LinkedIn_content(topic):
    messages = [
    {"role": "system", "content": f"""You are trained to analyze a topic and generate an LinkedIn post.First analyze the (Language) of {topic} and responsed must be in same language.If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.And post should not contain any type of (emojis).Response should be in the same language as {topic}."""},
    {"role": "user", "content": f"""Analyze the topic and generate an LinkedIn post without any type of (emojis). The topic is: {topic}.
                                    Follow the instruction:
                                    1. Response should be in the same language as the language of {topic}.
                                    2. If {topic} is (country) specific, Do not follow the country language,Just follow the overall language of {topic}.
                                    3. Shape it like a LinkedIn Post without containing any kind of (emojis).
                                    4. Do not Add the (emojis).
                                    5. Start your post with an engaging and attention-grabbing opening sentence. This should be concise and highlight the main point or message you want to convey.
                                    6. Generate text relevent to the topic. (Decide the size of the text depending upon the topic).
                                    7. If relevant, you can include hashtags to categorize your post and make it more discoverable but not (emojis).
                                    8. It should not generate any harmful text.                                   
                                    9. Rigorously follow instruction (2)."""}
    ]

    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages, 
                        max_tokens= 600, 
                        n=1, 
                        stop=None, 
                        temperature=0.6)

    response_text = response.choices[0].message.content.strip()

    return response_text



#function for better image prompt
def TextRefine(topic):
    messages = [
    {"role": "system", "content": f"""Your role is to write the prompts that can generate stunning, realistic and high qulaity 4k images. Get the idea from {topic} and write prompts in atmost 30 words. The prompts should be relevant to {topic}."""},
    {"role": "user", "content": f"""Write a prompt that can generate the Stunning, realistic, high quality 4k photography and showcasing the beauty images based on the {topic}.Portray every detail of {topic} with stunning realism.The prompt should clearly define the image content and mention the quality of image.The prompt should clearly mention that there should not any text in the generated images. The prompt should be less than 30 words"""}
    ]

    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages, 
                        max_tokens= 3000, 
                        n=1, 
                        stop=None, 
                        temperature=1)

    response_text = response.choices[0].message.content.strip()
   # print(response_text)
    return response_text

#function to remove emojis
def remove_emojis(text):
    # Regular expression to match emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # Emoticons
                               u"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
                               u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
                               u"\U0001F700-\U0001F77F"  # Alchemical Symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A"
                               u"\U00002702-\U000027B0"  # Dingbats
                               u"\U000024C2-\U0001F251" 
                               "]+", flags=re.UNICODE)
    
    # Remove emojis from the text
    return emoji_pattern.sub(r'', text)


#Function for blog image prompt
def blogPromptGenerator(topic):
    messages = [
    {"role": "system", "content": f"""Your role is to generate some prompts that can generate stunning, realistic and high qulaity 4k images for (blog). Get the idea from {topic} of (blog) and write prompts in atmost 30 words. The prompts should be relevant to {topic}.prompt should focus on a distinct point and contribute to a cohesive set of images for (blog)'s multi-point structure.As we need 3 prompt in return.So, The list of prompt should be in the form: ['Prompt1','Prompt2','Prompt3']"""},
    {"role": "user", "content": f"""Write a prompt that can generate the Stunning, realistic, high quality 4k photography and showcasing the beauty images based on the {topic}.Portray every detail of {topic} with stunning realism because.Craft prompts to generate images that capture different facets of {topic} for (blog)'s post.The prompt should clearly define the image content and mention the quality of image.The prompt should clearly mention that there should not any text in the generated images. The prompt should be less than 30 words"""}
    ]
    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages, 
                        max_tokens= 3000, 
                        n=1, 
                        stop=None, 
                        temperature=1)

    response_text = response.choices[0].message.content.strip()
   # print(response_text)
    return response_text

    
def blogMultiPromptGenerator(topic,content):
    prompt = f"Description: {topic},{content}"
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages = [
        {"role": "system", "content": f"""Your role is to generate some prompts that can generate stunning, realistic and high qulaity 4k images for (blog) with no text. Get the idea from {topic} and {content} of (blog) and write prompts in atmost 30 words. The prompts should be relevant to {topic} and {content}.prompt should focus on a distinct point and contribute to a cohesive set of images for (blog)'s multi-point structure.The prompt should clearly mention that there should not any text in the generated images.the response must not be empty like [''].As we need 3 prompt in return.So, The list of prompt should be in the form: ['Prompt1','Prompt2','Prompt3']"""},
        {"role": "user", "content": f"""Write a prompt that can generate the Stunning, realistic, high quality 4k photography and showcasing the beauty images based on the {topic} and {content}.Portray every detail of {topic} and {content} with stunning realism.Craft prompts to generate images that capture different facets of {topic} and {content} for (blog)'s post.The prompt should clearly define the image content and mention the quality of image.The prompt should clearly mention that there should not any text in the generated images. The prompt should be less than 30 words"""}
        ],
        temperature =1
        )
    except Exception as e:
        print(f'Error : {str(e)}')
    prompt_list = response['choices'][0]['message']['content']
    prompt_list = prompt_list.split("\n")
    if prompt_list is not None:
        print(prompt_list)
        return prompt_list
        
    else:
        return None
    
#function for splitting text
def split_text(text):
    length = len(text)
    third = length // 3

    part1 = text[:third]
    part2 = text[third:2*third]
    part3 = text[2*third:]

    return part1, part2, part3

# Function for Background image Generation from Dall-E
def generate_thumbnail_background(text):
    #Refine the text for image
    # Generate the image using OpenAI's DALL-E model
    response = openai.Image.create(
        prompt=f"{text}",
        n=3,
        size = "512x512"        
        )

    # Get the image URL from the response
    image_url = response.data[0]['url']

    # Download the image and convert it to a PIL image
    image_content = requests.get(image_url).content
    image = Image.open(io.BytesIO(image_content))
    # image.show()
    # image.save("demoPic.jpg")
    return image

#function for generating multiple image for blogs

def generate_multi_thumbnail_background(text1):
    generated_images = []
    text = [item for item in text1 if item]
    for i in range(0,len(text)):
        #Refine the text for image
        # Generate the image using OpenAI's DALL-E model
        punctuation_list = '0123456789,;.:?\/"'
        text[i] = text[i].replace(text[i][:3], "")
        for punctuation in punctuation_list:
            text[i] = text[i].replace(punctuation, "")
        new=text[i]
        response = openai.Image.create(
        prompt=f"{new}",
        n=1,
        size = "512x512"        
        )

        # Get the image URL from the response
        image_url = response.data[0]['url']

        # Download the image and convert it to a PIL image
        image_content = requests.get(image_url).content
        image = Image.open(io.BytesIO(image_content))
        generated_images.append(image)
        # image.show()
        # image.save(f"Add_gen{i}.jpg")
    return generated_images


#function for multi blogs titles

def blogMultiTitleGenerator(topic):
    prompt = f"Description: {topic}"
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
        {"role": "system", "content": f"""You are trained to analyze a {topic} and generate some (Titles) of a blog post depending upon the {topic}. Get the idea from {topic} of (blog) and write some (Titles). The Titles should be relevant to {topic}.As we need 5 Title in return.So, The List of Title should be in the form: ["Title1","Title2","Title3","Title4","Title5"]. Do not add (\) in Titles.Response should be in the same language as {topic} """},
        {"role": "user", "content": f"""Analyze the {topic} and generate some Titles of a blog post. The topic is {topic}
                                        All 5 (Titles) should be vary from each other.The Titles should be relevant to {topic}.Do not add (\) in response.Response should be in the same language as {topic}"""}
        ],
        temperature =1
        )
    except Exception as e:
        print(f'Error : {str(e)}')
    prompt_list = response['choices'][0]['message']['content']
    prompt_list = prompt_list.replace("\\","")
    prompt_list = prompt_list.split("\n")
    # response_without_backslashes = prompt_list.replace("\\", "")
    if prompt_list is not None:
        print(response)
        return prompt_list
        
    else:
        return None

#Seo keywords generation for Blog
def generate_Blog_SEO(topic):
    messages = [
    {"role": "system", "content": f"""You are trained to analyze a {topic} and generate (8) (SEO) keywords of a blog post depending upon the topic.Only generate (SEO) keywords.Response should be in the same language as {topic}"""},
    {"role": "user", "content": f"""Analyze the topic and generate the (SEO) of a blog post. The topic is {topic}
                                    Generate (8) (SEO) keywords for blog post.The (SEO) keywords would varry on the topic.And generate Seo keywords in the form of this '#SEO,#SEO,#SEO'.Only generate (SEO) keywords.Response should be in the same language as {topic}"""}
    ]

    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages, 
                        max_tokens= 3000, 
                        n=1, 
                        stop=None, 
                        temperature=0.6)

    response_text = response.choices[0].message.content.strip()
    print(response_text)
    return response_text


#function for repos and blog topic
def topic_generate(prompt):
    messages = [
    {"role": "system", "content": f"""Your role is to Analyze the {prompt} and generate (one) main (Topic) related to {prompt}. Get the idea from {prompt} and write (Topic).The (Topic) should be relevant to {prompt}.And (Topic) must be only (one).Response should contain only topic and focus on the main (topic) of {prompt}.Response contain at most 2 words."""},
    {"role": "user", "content": f"""Write a (one) main (Topic) based on the {prompt}.Craft Topic facets of {prompt}.And (Topic) must be only (one).Response should focus on the main (topic) of {prompt}.Response contain at most 2 words."""}
    ]
    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages, 
                        max_tokens= 3000, 
                        n=1, 
                        stop=None, 
                        temperature=0.6)

    response_text = response.choices[0].message.content.strip()
    print(response_text)
    return response_text

def blog_repo_links(topic):
    llm = OpenAI(temperature=0, 
                 openai_api_key=openapi_key)
    search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)
    tools = [Tool(
                name="Intermediate Answer",
                func=search.run,
                description="useful for when you need to ask with search",)]
    self_ask_with_search = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
    response = self_ask_with_search.run(f"Give me valid http links for news articles,videos,blog posts on the topic {topic}")
    # tools = load_tools(["serpapi"], llm=llm )
    # agent = initialize_agent(search ,llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
    # response=agent.run(f"Give me http links for news articles, blog posts on the topic {topic}")
    print(response)
    return response


#speech to text
def speechToText(filename):
    transcribed_text = openai.Audio.transcribe("whisper-1", filename)
    return transcribed_text['text']



#function for comment replier
def commentReplier(comment):
    messages = [
    {"role": "system", "content": f"""You are trained for Auto reply the {comment}.First analyze a {comment} (Tone) and (Topic) and generate (Reply) according to {comment}.Response only contain (Reply) with no heading.Response should be in the same language as {comment}"""},
    {"role": "user", "content": f"""Analyze the {comment} and generate Reply.The comment is: {comment}.
                                    Follow the instruction:
                                    1. Response should be in the same language as {comment}
                                    2. If {comment} is (Rude) than (reply) should be (neutral).
                                    3. If {comment} is (Jolly) than (reply) should be (Jolly). 
                                    4. If {comment} is (Neutral) than (reply) should be (Neutral)
                                    5. Ananlyze the (Topic) and (Tone) of {comment} properly.
                                    6. Reply Should be (Concise) and to the point.
                                    7. Reply should contain (At most) 20 words.
                                    8. Response only contain (Reply) with no (heading) Like (Reply:).
                                    9. It should not generate any harmful text.                                   
                                    """}
    ]

    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages, 
                        max_tokens= 600, 
                        n=1, 
                        stop=None, 
                        temperature=0.6)

    response_text = response.choices[0].message.content.strip()
    print(response_text)
    return (response_text)
