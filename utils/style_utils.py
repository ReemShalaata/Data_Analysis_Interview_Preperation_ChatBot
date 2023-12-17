
import streamlit.components.v1 as components
import streamlit as st
def format_text(text, size, color, alignment, font_family="Arial", font_weight="normal", emoji=None):
    emoji_html = f"{emoji} " if emoji else ""
    # Wrap the text inside a div element for applying text alignment
    return f'<div style="text-align: {alignment};"><span style="color: {color}; font-size: {size}px; font-family: {font_family}; font-weight: {font_weight};">{text} {emoji_html}</span></div>'



def changewidgetfontstyle(wgt_txt, font_size='12px', font_family='Arial', font_weight='normal', text_align='center'):
    htmlstr = f""""
   <script>
        var elements = window.parent.document.querySelectorAll('*');
        for (var i = 0; i < elements.length; i++) {{
            if (elements[i].innerText === '{wgt_txt}') {{
                elements[i].style.fontSize = '{font_size}';
                elements[i].style.fontFamily = '{font_family}';
                elements[i].style.fontWeight = '{font_weight}';
                elements[i].style.textAlign = '{text_align}';
                elements[i].style.fontColor= '{text_align}';
            }}
        }}
    </script>
    """
    components.html(htmlstr, height=0, width=0)


def changeradiotfontsize(wgt_txt, wch_font_size = '12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('p'), i;
                for (i = 0; i < elements.length; ++i) 
                    { if (elements[i].textContent.includes(|wgt_txt|)) 
                        { elements[i].style.fontSize ='""" + wch_font_size + """'; } }</script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)



# Function to get user answer and append it to the list
def user_answer_input(question_num,max_question_reached):
    key = f"answer{question_num}"
    print(st.session_state.user_answers_list)
    print(max_question_reached,question_num)
    # Check if the question has been reached or exceeded
    if question_num==1 and max_question_reached==1:
        user_answer = st.text_area("", key=key)      

    elif question_num <=max_question_reached:
        user_answer = st.text_area("", key=key, value=st.session_state.user_answers_list[question_num - 1])
    else:
        user_answer=st.text_area("", key=key,disabled=True)

    return user_answer

    
def set_background(color):
    # Using the provided color
    st.markdown(
        f"""1
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
