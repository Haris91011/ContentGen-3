import streamlit as st
from streamlit_chat import message
from streamlit_Utilities import *
import pyaudio
from pathlib import Path
import pathlib
import wave
from audio_recorder_streamlit import audio_recorder
openapi_key = st.secrets["open_ai_key"]
# openai.api_key = api_key.key
openai.api_key = openapi_key

# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
# RECORD_SECONDS = 10
if 'insta' not in st.session_state:
    st.session_state['insta'] = []
    st.session_state['instaImage'] = []
if 'twit' not in st.session_state:
    st.session_state['twit'] = []
    st.session_state['twitImage'] = []
if 'face' not in st.session_state:
    st.session_state['face'] = []
    st.session_state['faceImage'] = []
if 'linke' not in st.session_state:
    st.session_state['linke'] = []
    st.session_state['linkeImage'] = []
if 'blog' not in st.session_state:
    st.session_state['bImage'] = []
    st.session_state['bTitle'] = []
    st.session_state['bStructure'] = []
    st.session_state['bContent'] = []
    st.session_state['bSEO'] = []
    st.session_state['bLinks'] = []
    st.session_state['bSave'] = []
if 'sppechToText' not in st.session_state:
    st.session_state['SpeechToText']=[] 
if 'VoiceRecording' not in st.session_state:
    st.session_state['VoiceRecording']=[]
st.title('Speech to text')
insta_button, twitter_button, facebook_button, linkedIn_button, blog_Title,blog_structure,blog_content,blog_image,blog_SEO,blog_Links = st.columns(10)
voice,col1,speechtoText,col3,col4=st.columns(5)

# with voice:
#     if st.button("Record", use_container_width=True):
#         try:
#             st.write("Try Saying")
#             p = pyaudio.PyAudio()
#             stream = p.open(format=FORMAT,
#                             channels=CHANNELS,
#                             rate=RATE,
#                             input=True,
#                             frames_per_buffer=CHUNK)

#             frames = []
#             for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#                 data = stream.read(CHUNK)
#                 frames.append(data)
#         except Exception as e:
#             st.warning("Can't able to record your audio")
#         st.write("Done recording")
#         stream.stop_stream()
#         stream.close()
#         p.terminate()
#         root_dir = pathlib.Path.cwd()
#         filename = root_dir / Path('try1.mp3')
#         with wave.open(str(filename), 'wb') as wf:
#             wf.setnchannels(CHANNELS)
#             wf.setsampwidth(p.get_sample_size(FORMAT))
#             wf.setframerate(RATE)
#             wf.writeframes(b''.join(frames))
#             wf.close()
#         audio_file = open(str(filename), "rb")
#         with st.spinner('Converting'):
#             try:
#                 st.session_state['VoiceRecording']=speechToText(audio_file)          
#             except Exception as e:
#                 print(e)
#                 st.warning("OpenAI API key Error. Replace your key.")
st.header("press to record audio")
audio_bytes = audio_recorder(
    sample_rate=41_000,
    pause_threshold=60.0,
    text="",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_size="6x",)
if audio_bytes:
    # audio=st.audio(audio_bytes, format="audio/wav")
    with open("test.wav", "wb") as f:
        f.write(audio_bytes)
        st.success("Audio saved successfully.")
    filename="test.wav"
    audio_file = open(str(filename), "rb")
    with st.spinner('Converting'):
        try:
            st.session_state['VoiceRecording']=speechToText(audio_file)          
        except Exception as e:
            print(e)
            st.warning("OpenAI API key Error. Replace your key.")
with speechtoText:
        uploaded_file=st.sidebar.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])
        if uploaded_file:
            with open("uploaded_audio.wav", "wb") as f:
                f.write(uploaded_file.read())
            filename="uploaded_audio.wav"
            audio_file = open(str(filename), "rb")
            with st.spinner('Converting'):
                try:
                    st.session_state['SpeechToText']=speechToText(audio_file)
                except Exception as e:
                    print(e)
                    st.warning("OpenAI API key Error. Replace your key.")
if st.session_state['VoiceRecording']:
    with insta_button:
        if st.sidebar.button("Instagram", use_container_width=True):
            # global prompt_
            st.session_state['insta'] = generate_Instagram_content(st.session_state['VoiceRecording'])
            # print(st.session_state['insta'])
            instaRefineText=TextRefine(st.session_state['VoiceRecording'])
            # print("2")
            st.session_state['instaImage']=generate_thumbnail_background(instaRefineText)
            # newRespone=TextRefine(prompt)
    with twitter_button:
        if st.sidebar.button("Twitter", use_container_width=True):
            st.session_state['twit'] = generate_Twitter_content(st.session_state['VoiceRecording'])
            # print(prompt)
            twiitwerRefineText=TextRefine(st.session_state['VoiceRecording'])
            # print(twiitwerRefineText)
            st.session_state['twitImage']=generate_thumbnail_background(twiitwerRefineText)
            # newRespone=TextRefine(prompt)

    with facebook_button:
        if st.sidebar.button("Facebook", use_container_width=True):
            text= generate_Facebook_content(st.session_state['VoiceRecording'])
            #removing left emojis
            st.session_state['face'] =remove_emojis(text)
            fbRefineText=TextRefine(st.session_state['VoiceRecording'])
            st.session_state['faceImage']=generate_thumbnail_background(fbRefineText)
            # newRespone=TextRefine(prompt)
    with linkedIn_button:
        if st.sidebar.button("Linkedin", use_container_width=True):
            text=generate_LinkedIn_content(st.session_state['VoiceRecording'])
            st.session_state['linke'] =remove_emojis(text)
            linkedinRefineText=TextRefine(st.session_state['VoiceRecording'])
            st.session_state['linkeImage']=generate_thumbnail_background(linkedinRefineText)
            # newRespone=TextRefine(prompt)
    with blog_Title:
        if st.sidebar.button("Blog Title", use_container_width=True):
            st.session_state['bTitle']=blogMultiTitleGenerator(st.session_state['VoiceRecording'])
            # response_dict = eval(st.session_state['blogTitle'])
    with blog_structure:
        if st.sidebar.button("Blog Structure", use_container_width=True):
            st.session_state['bStructure'] = generate_Blog_Structure(st.session_state['VoiceRecording'])
            st.session_state['bSave']=st.session_state['bStructure']
    with blog_content:
        if st.sidebar.button("Blog Content", use_container_width=True):
            # print("------------------")
            print(st.session_state['blogSave'])
            st.session_state['bContent'] = generate_Blog_Content(st.session_state['VoiceRecording'], st.session_state['bSave'])
    with blog_SEO:
        if st.sidebar.button("Blog SEO", use_container_width=True):
            st.session_state['bSEO']=generate_Blog_SEO(st.session_state['VoiceRecording'])
    with blog_image:
        if st.sidebar.button("Blog Image", use_container_width=True):
            blogRefineText=blogMultiPromptGenerator(st.session_state['VoiceRecording'],st.session_state['bContent'])
            st.session_state['bImage']=generate_multi_thumbnail_background(blogRefineText)
    with blog_Links:
        if st.sidebar.button("Blog Links", use_container_width=True):
            blogLink=topic_generate(st.session_state['VoiceRecording'])
            st.session_state['bLinks']=blog_repo_links(blogLink)




if st.session_state['VoiceRecording']:
    st.header("Generated Voice")
    message(st.session_state['VoiceRecording'])
if st.session_state['SpeechToText']:
    st.header("Speech to Text")
    message(st.session_state['SpeechToText'])
if st.session_state['insta']:
    st.header("Instagram Post Generated")
    # st.write("Instagram")
    message(st.session_state['insta'])
    st.image(st.session_state['instaImage'],caption='Generated Image',use_column_width=True)
    # st.write(newRespone)
if st.session_state['twit']:
    st.header("Twitter Post Generated")
    # st.write("Twitter")
    message(st.session_state['twit'])
    st.image(st.session_state['twitImage'],caption='Generated Image',use_column_width=True)
    # st.write(newRespone)
if st.session_state['face']:
    st.header("Facebook Post Generated")
    # st.write("Facebook")
    message(st.session_state['face'])
    st.image( st.session_state['faceImage'],caption='Generated Image',use_column_width=True)
    # st.write(newRespone)
if st.session_state['linke']:
    st.header("LinkedIn Post Generated")
    # st.write("LinkedIn")
    message(st.session_state['linke'])
    st.image(st.session_state['linkeImage'],caption='Generated Image',use_column_width=True)
    # st.write(newRespone)
if st.session_state['bTitle']:
    st.header("Blog Title Generated")
    # st.write("Blog Title")
    for i in range(0,len(st.session_state['bTitle'])):
        message(st.session_state['bTitle'][i][1:-1])
if st.session_state['bStructure']:
    st.header("Blog Structure Generated")
    # st.write("Blog Structure")
    message(st.session_state['bStructure'])
if st.session_state['bContent']:
    st.header("Blog Content Generated")
    # st.write("Blog Content")
    message(st.session_state['bContent'])
if st.session_state['bImage']:
    st.header("Blog Image Generated")
    # st.write("Blog Image")
    for i in range(0,3): 
        st.image(st.session_state['bImage'][i],caption='Generated Image',use_column_width=True)
if st.session_state['bSEO']:
    st.header("Blog SEO words Generated")
    # st.write("Blog SEO")
    message(st.session_state['bSEO'])
if st.session_state['bLinks']:
    st.write("Blog Links")
    message(st.session_state['bLinks'])



