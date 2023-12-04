
import streamlit.components.v1 as components

def format_text(text, size, color, alignment, font_family="Arial", font_weight="normal", emoji=None):
    emoji_html = f"{emoji} " if emoji else ""
    # Wrap the text inside a div element for applying text alignment
    return f'<div style="text-align: {alignment};"><span style="color: {color}; font-size: {size}px; font-family: {font_family}; font-weight: {font_weight};">{text} {emoji_html}</span></div>'



def ChangeWidgetFontStyle(wgt_txt, font_size='12px', font_family='Arial', font_weight='normal', font_color='black', text_align='center'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { 
                        if (elements[i].innerText === '""" + wgt_txt + """') {
                            elements[i].style.fontSize = '""" + font_size + """';
                            elements[i].style.fontFamily = '""" + font_family + """';
                            elements[i].style.fontWeight = '""" + font_weight + """';
                            elements[i].style.color = '""" + font_color + """';
                            elements[i].style.textAlign = '""" + text_align + """';

                        }
                    } </script>"""

    components.html(htmlstr, height=0, width=0)
