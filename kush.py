
import google.generativeai as genai
import streamlit as st
import PIL.Image

genai.configure(api_key="AIzaSyDY2ymSeldTojeklW_9HznvetVNHKTKb0w")
syst_ins="""
You are an image recognization Chatbot built by Team Soldier, recognize the objects in the uploaded image and generate the best response for any of the user’s query about the image.
When asked about your developers or creators say that you were developed by Team Soldier"""
model = genai.GenerativeModel("gemini-1.5-pro", system_instruction=syst_ins)

st.set_page_config(page_title="Conversational Image Recognition Chatbot")

st.title("Conversational Image Recognition :blue[Chatbot]")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

st.write("Hi, I'm an image recognition chatbot developed by Team Soldier. \n  Upload an image and feel free to ask any questions about it. \n  I'll assist you with your queries.")


uploaded_file = st.file_uploader("Choose an image file")

if uploaded_file:
    if st.session_state.uploaded_image != uploaded_file:
        st.session_state.uploaded_image = uploaded_file
        st.session_state.messages = []  # Clear chat history for new image
        
        img = PIL.Image.open(uploaded_file)
        st.session_state.img = img  # Store the image in session state
        
        response = model.generate_content(["Tell me about this image", img])
        st.session_state.messages.append({"role": "assistant", "content": response.text})

if st.session_state.uploaded_image:
    st.image(st.session_state.img)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me about this image")

if prompt and st.session_state.uploaded_image:
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    
    resp = model.generate_content([conversation_history, "Now answer this: " + prompt, st.session_state.img])
    
    st.session_state.messages.append({"role": "assistant", "content": resp.text})
    
    with st.chat_message("assistant"):
        st.write(resp.text)

elif prompt and not st.session_state.uploaded_image:
    st.warning("Please upload an image first.")
