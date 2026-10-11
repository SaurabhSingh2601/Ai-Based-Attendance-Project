import streamlit as st

def subject_card(name,code,section,stats=None,footer_callback=None):
    html=f"""
      <div style="background:white; border-left:8px solid #EB459E ; padding:25px ; border:1px solid black;border-radius:20px;margin-bottom:20px">
      <h3 style="margin:0; color:black; font-size:1.25rem">{name}</h3>
      <p style="margin:10px 0;color:black">Code:<span style="background:#E0E3FF;color:black;padding:2px 8px;border-radius:4px">{code }</span> | Section:{section}</p>
      """
    if stats:
        html+="""
         <div style="display:flex;gap:8px;flex-wrap:wrap">"""
        for icon,label,value in stats:
            html+=f'<div style="background:#EB49E10;color:black;padding:5px 12px;border-radius:12px;font-size:0.5rem">{icon} <b>{value}</b> {label}</div>'
        html+="</div>"

    st.markdown(html,unsafe_allow_html=True)

    if footer_callback:
        footer_callback()



