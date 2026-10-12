import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    """Renders a styled subject card with course stats and custom footer action."""
    html = f"""
        <div style="background:white; border-left: 8px solid #EB459E; padding:25px; border-radius: 20px; border: 1px solid #e2e8f0; margin-bottom:20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <h3 style="margin:0; color: #1e293b; font-size: 1.5rem; font-weight:700;">{name}</h3>
            <p style="color:#64748b; margin:10px 0;">Code: <span style="background:#E0E3FF; color:#5865F2; padding:2px 8px; border-radius:5px; font-weight:600;">{code}</span> | Section: <b>{section}</b></p>
    """

    if stats:
        html += """<div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:12px;">"""
        for icon, label, value in stats:
            html += f'<div style="background: #EB459E15; color:#EB459E; padding:5px 12px; border-radius:12px; font-size:0.9rem; font-weight:600;">{icon} <b>{value}</b> {label}</div>'
        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
