def custom_css():
    custom_css = """
        <style>

            /* Targeting all textarea elements */
            .element-container:has(>.stTextArea), .stTextArea {
                width: 550px !important;
            }
            .stTextArea textarea {
                height: 400px;

            }

            div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] {
                background: transparent;
                padding-right: 10px;
                padding-left: 0px;
                padding-bottom: 10px;
                margin: 5px;
                border: 0px solid #249ded;

            } 
            div.stButton > button:first-child {
                background-color: white;
                color: #1E90FF;
                width: 150px;
                height: 50px;
            }

            div.stButton > button:hover {
                background-color: #98FB98;
                color:white;
            }

        </style>
    """            

    return custom_css

