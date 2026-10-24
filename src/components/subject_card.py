import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
      <div style="background:white; border-left:8px solid #EB459E; padding:20px; border:1px solid #E2E8F0; border-radius:16px; margin-bottom:18px; box-shadow:0 4px 12px rgba(0,0,0,0.06);">
      <h3 style="margin:0; color:#1E293B; font-size:1.25rem;">{name}</h3>
      <p style="margin:8px 0; color:#475569; font-size:0.95rem;">Code: <span style="background:#EEF2FF; color:#4F46E5; font-weight:600; padding:2px 8px; border-radius:6px;">{code}</span> | Section: <b>{section}</b></p>
    """
    if stats:
        html += """<div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:10px;">"""
        for icon, label, value in stats:
            html += f'<div style="background:#F1F5F9; color:#0F172A; padding:6px 14px; border-radius:12px; font-size:0.85rem; display:inline-flex; align-items:center; gap:5px;">{icon} <b>{value}</b> {label}</div>'
        html += "</div>"
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
