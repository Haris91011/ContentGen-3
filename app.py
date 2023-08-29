import streamlit as st
from streamlit_chat import message
from streamlit_Utilities import *
import pyaudio
from pathlib import Path
import pathlib
import wave
# from instadev import *

st.set_page_config(
    page_title="Ryan",
    page_icon="🐥"
)
st.sidebar.success("Select Above page")


openapi_key = st.secrets["open_ai_key"]
# openai.api_key = api_key.key
openai.api_key = openapi_key

SerpAPIWrapper.serp_api_key = st.secrets["serp_api_key"]
st.title('Content Generator Demo')
prompt = st.text_input('Write Your Topic.')
if 'instagram' not in st.session_state:
    st.session_state['instagram'] = []
    st.session_state['instagramImage'] = []
if 'twitter' not in st.session_state:
    st.session_state['twitter'] = []
    st.session_state['twitterImage'] = []
if 'facebook' not in st.session_state:
    st.session_state['facebook'] = []
    st.session_state['faceebokImage'] = []
if 'linkedin' not in st.session_state:
    st.session_state['linkedin'] = []
    st.session_state['linkedinImage'] = []
if 'blogPost' not in st.session_state:
    st.session_state['blogPost'] = []
    st.session_state['blogImage'] = []
    st.session_state['blogTitle'] = []
    st.session_state['blogStructure'] = []
    st.session_state['blogContent'] = []
    st.session_state['blogSEO'] = []
    st.session_state['blogLinks'] = []
    st.session_state['blogSave'] = []


insta_button, twitter_button, facebook_button, linkedIn_button, blog_Title,blog_structure,blog_content,blog_image,blog_SEO,blog_Links = st.columns(10)
st.sidebar.header('Side Panel')
if prompt:
    with insta_button:
        if st.sidebar.button("Instagram", use_container_width=True):
            # global prompt_
            print(prompt)
            st.session_state['instagram'] = generate_Instagram_content(prompt)
            print(st.session_state['instagram'])
            instaRefineText=TextRefine(prompt)
            print("2")
            st.session_state['instagramImage']=generate_thumbnail_background(instaRefineText)
            # newRespone=TextRefine(prompt)
    with twitter_button:
        if st.sidebar.button("Twitter", use_container_width=True):
            st.session_state['twitter'] = generate_Twitter_content(prompt)
            print(prompt)
            twiitwerRefineText=TextRefine(prompt)
            print(twiitwerRefineText)
            st.session_state['twitterImage']=generate_thumbnail_background(twiitwerRefineText)
            # newRespone=TextRefine(prompt)

    with facebook_button:
        if st.sidebar.button("Facebook", use_container_width=True):
            text= generate_Facebook_content(prompt)
            #removing left emojis
            st.session_state['facebook'] =remove_emojis(text)
            fbRefineText=TextRefine(prompt)
            st.session_state['faceebokImage']=generate_thumbnail_background(fbRefineText)
            # newRespone=TextRefine(prompt)
    with linkedIn_button:
        if st.sidebar.button("LinkedIn", use_container_width=True):
            text=generate_LinkedIn_content(prompt)
            st.session_state['linkedin'] =remove_emojis(text)
            linkedinRefineText=TextRefine(prompt)
            st.session_state['linkedinImage']=generate_thumbnail_background(linkedinRefineText)
            # newRespone=TextRefine(prompt)
    with blog_Title:
        if st.sidebar.button("Blog Title", use_container_width=True):
            st.session_state['blogTitle']=blogMultiTitleGenerator(prompt)
            # response_dict = eval(st.session_state['blogTitle'])
    with blog_structure:
        if st.sidebar.button("Blog Structure", use_container_width=True):
            st.session_state['blogStructure'] = generate_Blog_Structure(prompt)
            st.session_state['blogSave']=st.session_state['blogStructure']
    with blog_content:
        if st.sidebar.button("Blog Content", use_container_width=True):
            print("------------------")
            print(st.session_state['blogSave'])
            st.session_state['blogContent'] = generate_Blog_Content(prompt, st.session_state['blogSave'])
    with blog_SEO:
        if st.sidebar.button("Blog SEO", use_container_width=True):
            st.session_state['blogSEO']=generate_Blog_SEO(prompt)
    with blog_image:
        if st.sidebar.button("Blog Image", use_container_width=True):
            blogRefineText=blogMultiPromptGenerator(prompt,st.session_state['blogContent'])
            st.session_state['blogImage']=generate_multi_thumbnail_background(blogRefineText)
    with blog_Links:
        if st.sidebar.button("Blog Links", use_container_width=True):
            blogLink=topic_generate(prompt)
            st.session_state['blogLinks']=blog_repo_links(blogLink)
if st.session_state['twitter']:
    st.header("Twitter Post Generated")
    # st.write("Twitter")
    message(st.session_state['twitter'])
    st.image(st.session_state['twitterImage'],caption='Generated Image',use_column_width=True)
    # st.write(newRespone)
if st.session_state['instagram']:
    st.header("Instagram Post Generated")
    # st.write("Instagram")
    message(st.session_state['instagram'])
    st.image(st.session_state['instagramImage'],caption='Generated Image',use_column_width=True)
    # st.write(newRespone)
if st.session_state['facebook']:
    st.header("Facebook Post Generated")
    # st.write("Facebook")
    message(st.session_state['facebook'])
    st.image( st.session_state['faceebokImage'],caption='Generated Image',use_column_width=True)
    # st.write(newRespone)
if st.session_state['linkedin']:
    st.header("LinkedIn Post Generated")
    # st.write("LinkedIn")
    message(st.session_state['linkedin'])
    st.image(st.session_state['linkedinImage'],caption='Generated Image',use_column_width=True)
    # st.write(newRespone)
if st.session_state['blogTitle']:
    st.header("Blog Title Generated")
    # st.write("Blog Title")
    for i in range(0,len(st.session_state['blogTitle'])):
        message(st.session_state['blogTitle'][i][1:-1])
if st.session_state['blogStructure']:
    st.header("Blog Structure Generated")
    # st.write("Blog Structure")
    message(st.session_state['blogStructure'])
if st.session_state['blogContent']:
    st.header("Blog Content Generated")
    # st.write("Blog Content")
    message(st.session_state['blogContent'])
if st.session_state['blogImage']:
    st.header("Blog Image Generated")
    # st.write("Blog Image")
    for i in range(0,3): 
        st.image(st.session_state['blogImage'][i],caption='Generated Image',use_column_width=True)
if st.session_state['blogSEO']:
    st.header("Blog SEO words Generated")
    # st.write("Blog SEO")
    message(st.session_state['blogSEO'])
if st.session_state['blogLinks']:
    st.write("Blog Links")
    message(st.session_state['blogLinks'])

