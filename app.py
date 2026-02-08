import streamlit as st
import openai
import base64

st.set_page_config(page_title="Ads Funnel AI", layout="centered")
st.title("🚀 Ads Funnel AI")
st.write("আপনার প্রোডাক্টের ছবি আপলোড করুন, AI আপনার জন্য বিজ্ঞাপন লিখে দিবে।")

# সাইডবারে API Key দেওয়ার জায়গা
api_key = st.sidebar.text_input("এখানে আপনার OpenAI API Key দিন", type="password")

if api_key:
    openai.api_key = api_key
    uploaded_file = st.file_uploader("আপনার প্রোডাক্টের ছবি (JPG/PNG) দিন...", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="আপনার প্রোডাক্ট", use_container_width=True)
        
        if st.button("Generate FB Ad Now"):
            with st.spinner("AI আপনার ছবি দেখে অ্যাড তৈরি করছে..."):
                # ছবিকে প্রসেস করা
                base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "তুমি একজন এক্সপার্ট ফেসবুক অ্যাড কপিরাইটার। এই ছবিটি দেখে এর জন্য বাংলায়: ১. একটি আকর্ষণীয় হেডলাইন ২. একটি প্রাইমারি টেক্সট (ইমোজি সহ) ৩. সঠিক কাস্টমার কারা হবে এবং ৪. ৫টি হ্যাশট্যাগ লিখে দাও।"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ],
                            }
                        ],
                        max_tokens=1000,
                    )
                    st.success("আপনার বিজ্ঞাপনের কন্টেন্ট তৈরি!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("আগে বাম পাশের বক্সে আপনার OpenAI API Key-টি পেস্ট করুন।")
