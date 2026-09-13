from google import genai
import streamlit as st

# पेज की सेटिंग
st.set_page_title(
    page_title="French Learning & Linguistic Bot",
    page_icon="🇫🇷",
    layout="wide",
)

st.title("🇫🇷 फ्रेंच भाषा शिक्षण, रोलप्ले और मशीन ट्रांसलेशन बॉट")
st.write(
    "यह ऐप आपकी फ्रेंच प्रैक्टिस, ग्रामर करेक्शन, मूल रूप (Lemma), काल, और"
    " लिप्यंतरण (Transliteration) में मदद करेगा।"
)

# साइडबार में API Key इनपुट
api_key = st.sidebar.text_input(
    "अपनी Google Gemini API Key दर्ज करें:", type="password"
)

if api_key:
  client = genai.Client(api_key=api_key)

  # दो अलग-अलग टैब: 1. चैट और रोलप्ले, 2. डीप ट्रांसलेशन और विश्लेषण
  tab1, tab2 = st.tabs(
      ["💬 फ्रेंच चैट और रोलप्ले", "🔄 मशीन ट्रांसलेशन और लिंग्विस्टिक विश्लेषण"]
  )

  # --- टैब 1: चैटबॉट & रोलप्ले ---
  with tab1:
    st.subheader("फ्रेंच बातचीत और अभ्यास (A2 Level)")
    st.write(
        "यहाँ आप फ्रेंच में चैट कर सकते हैं। बॉट आपकी गलतियां सुधारेगा और"
        " हिंदी/अंग्रेजी में सहायता करेगा।"
    )

    system_instruction_chat = """
        You are a friendly French language tutor and roleplay partner tailored for an A2 level learner. 
        Engage in natural French conversation, gently correct grammar mistakes, explain tenses, 
        and provide Hindi/English meanings or Devanagari transliteration when helpful.
        """

    if "french_chat_session" not in st.session_state:
      st.session_state.french_chat_session = client.chats.create(
          model="gemini-2.5-flash",
          config={"system_instruction": system_instruction_chat},
      )

    if "french_messages" not in st.session_state:
      st.session_state.french_messages = []

    for msg in st.session_state.french_messages:
      with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

    if user_prompt := st.chat_input(
        "फ्रेंच में कुछ लिखें या सवाल पूछें..."
    ):
      st.session_state.french_messages.append(
          {"role": "user", "content": user_prompt}
      )
      with st.chat_message("user"):
        st.markdown(user_prompt)

      with st.chat_message("assistant"):
        with st.spinner("सोच रहा है..."):
          try:
            response = st.session_state.french_chat_session.send_message(
                user_prompt
            )
            st.markdown(response.text)
            st.session_state.french_messages.append(
                {"role": "assistant", "content": response.text}
            )
          except Exception as e:
            st.error(f"एरर: {e}")

  # --- टैब 2: मशीन ट्रांसलेशन और लिंग्विस्टिक विश्लेषण ---
  with tab2:
    st.subheader("मशीन ट्रांसलेशन और व्याकरणिक विश्लेषण टूल")
    st.write(
        "यहाँ कोई भी फ्रेंच वाक्य या शब्द दर्ज करें और उसका विस्तृत विश्लेषण"
        " प्राप्त करें।"
    )

    french_text = st.text_area(
        "फ्रेंच टेक्स्ट यहाँ लिखें:",
        placeholder=(
            "जैसे: Je suis allé au marché hier pour acheter des fruits."
        ),
    )

    if st.button("विश्लेषण और अनुवाद करें"):
      if french_text.strip():
        with st.spinner("विश्लेषण किया जा रहा है..."):
          try:
            analysis_prompt = f"""
                        Analyze the following French text thoroughly for a research scholar and language learner. Provide details in Hindi/English:
                        1. **Machine Translation (मशीन अनुवाद):** Accurate Hindi and English translation.
                        2. **Tense & Structure (काल और वाक्य संरचना):** Identify the tense, mood, and sentence structure.
                        3. **Word-by-Word / Key Term Breakdown (शब्द विश्लेषण):** For key verbs or words, provide:
                           - Grammatical Category (व्याकरणिक कोटि / Part of Speech, e.g., Noun, Verb, Adjective)
                           - Base/Root Form / Lemma (मूल रूप / infinitive form, e.g., 'être' for 'suis', 'aller' for 'allé')
                           - Devanagari Transliteration (देवनागरी लिपि में सटीक उच्चारण/लिप्यंतरण)
                        
                        French Text: {french_text}
                        """
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=analysis_prompt
            )
            st.success("विश्लेषण सफल!")
            st.markdown(response.text)
          except Exception as e:
            st.error(f"एरर: {e}")
      else:
        st.warning("कृपया पहले कुछ फ्रेंच टेक्स्ट लिखें।")

else:
  st.info(
      "कृपया ऐप का उपयोग शुरू करने के लिए साइडबार में अपनी Gemini API Key दर्ज"
      " करें।"
  )