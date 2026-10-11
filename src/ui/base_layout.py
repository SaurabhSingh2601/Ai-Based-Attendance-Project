import streamlit as st

def style_background_home():
    st.markdown("""
        <style>
                .stApp{
                    background-color:#0F172A !important;
                
                  
                }
                .stApp div[data-testid="stColumn"]{
                    background-color:#F8FAFC !important;
                    padding:1rem !important;
                    border-radius:2rem !important;
                    min-height:180px !important;
                    max-height:250px !important;
                    margin:auto !important;
                    box-shadow:0 8px 25px rgba(0,0,0,0.15) !important;
                
                }
                .stApp div[data-testid="stColumn"] h2{
                color:black !important;
            }
        </style>        
                      
          



                """,unsafe_allow_html=True)
    
def style_background_dashboard():
    st.markdown("""
        <style>
                .stApp{
                    background-color:linear-gradient(135deg,#5865F2,#7C3AED)!important;
                  
                }
        </style>        
                      
          



                """,unsafe_allow_html=True)    
    

def style_base_layout():
    st.markdown("""
        <style>
                @import url('https://fonts.googleapis.com/css2?family=Baloo+Bhai+2:wght@400..800&family=Climate+Crisis:YEAR@1979&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Baloo+Bhai+2:wght@400..800&family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
                
                #MainMenu,header,footer{
                    visibility:hidden;
                }

                .block-container{
                    padding-top:1.5rem !important;
                }

                h1{
                    font-family:'Climate Crisis',sans-serif !important;
                    font-size:2.5rem !important;
                    line-height:1.1 !important;
                    margin-bottom:0rem !important;
                    color:white !important;
                }


                h2{
                    font-family:'Climate Crisis',sans-serif !important;
                    font-size:2rem !important;
                    line-height:0.9 !important;
                    margin-bottom:0rem !important;
                    color:#F8FAFF !important;
                }

                .stApp div[data-testid="stColumn"] h3,
                .stApp div[data-testid="stColumn"] p{
                    color:#FFFFFF !important;
                }

                h3,h4,p{
                    font-family:'Outfit',sans-serif !important;
                    

                }

                button{
                    background-color:#5865F2 !important;
                    border-radius:1.5rem !important;
                    color:white !important;
                    padding: 10px 20px !important;
                    border:none !important;
                    transistion:transform 0.25s ease-in-out !important;
                

                    
                }

                button[kind="secondary"]{
                    background-color:#EB459E !important;
                    border-radius:1.5rem !important;
                    color:white !important;
                    padding: 10px 20px !important;
                    border:none !important;
                    transistion:transform 0.25s ease-in-out !important;
                

                    
                }

                button[kind="tertiary"]{
                    background-color:#000000 !important;
                    border-radius:1.5rem !important;
                    color:white !important;
                    padding: 10px 20px !important;
                    border:none !important;
                    transition:transform 0.25s ease-in-out !important;
                

                    
                }

                button:hover{
                     transform:scale(1.05) !important;
                }
        
                    
                
                
        </style>        
                    
        



                """,unsafe_allow_html=True)
    


