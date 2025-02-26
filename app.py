import streamlit as st
import time

# Conversion configuration dictionary
CONVERSIONS = {
    'length': {
        'meters': 1,
        'kilometers': 1000,
        'centimeters': 0.01,
        'miles': 1609.34,
        'inches': 0.0254,
        'feet': 0.3048
    },
    'weight': {
        'kilograms': 1,
        'grams': 0.001,
        'pounds': 0.453592,
        'ounces': 0.0283495
    },
    'temperature': {
        'celsius': 'celsius',
        'fahrenheit': 'fahrenheit'
    },
    'volume': {
        'liters': 1,
        'milliliters': 0.001,
        'gallons': 3.78541,
        'cubic meters': 1000
    },
    'speed': {
        'meters per second': 1,
        'kilometers per hour': 0.277778,
        'miles per hour': 0.44704,
        'feet per second': 0.3048
    },
    'time': {
        'seconds': 1,
        'minutes': 60,
        'hours': 3600,
        'days': 86400,
        'weeks': 604800
    }
}

# Custom CSS for dark theme, neon effects, and animations
def inject_custom_css():
    st.markdown("""
    <style>
        :root {
            --neon-cyan: #00ffff;
            --neon-pink: #ff69b4;
            --dark-bg: #0a0a0a;
        }
        
        /* Base dark theme */
        .stApp {
            background-color: var(--dark-bg);
            color: white;
        }
        
        /* Input field styling with increased specificity */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] input,
        div[data-baseweb="number-input"] input,
        div[data-baseweb="textarea"] textarea {
            background-color: #1a1a1a !important;
            color: white !important;
            border: 1px solid var(--neon-cyan) !important;
            border-radius: 4px !important;
        }

        /* Hover states */
        div[data-baseweb="select"]:hover > div,
        div[data-baseweb="input"]:hover input,
        div[data-baseweb="number-input"]:hover input,
        div[data-baseweb="textarea"]:hover textarea {
            background-color: #222222 !important;
            border-color: var(--neon-pink) !important;
            box-shadow: 0 0 10px rgba(255, 105, 180, 0.2) !important;
        }

        /* Focus states */
        div[data-baseweb="select"]:focus-within > div,
        div[data-baseweb="input"]:focus-within input,
        div[data-baseweb="number-input"]:focus-within input,
        div[data-baseweb="textarea"]:focus-within textarea {
            background-color: #2a2a2a !important;
            border-color: var(--neon-cyan) !important;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2) !important;
        }

        /* Dropdown menu styling */
        div[role="listbox"] {
            background-color: #1a1a1a !important;
            border: 1px solid var(--neon-cyan) !important;
        }

        div[role="option"] {
            background-color: #1a1a1a !important;
            color: white !important;
        }

        div[role="option"]:hover {
            background-color: #2a2a2a !important;
        }

        /* Label styling */
        .stSelectbox label,
        .stTextInput label,
        .stNumberInput label,
        .stTextArea label {
            color: var(--neon-cyan) !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #000000 !important; /* Black background */
            border-right: 2px solid var(--neon-cyan) !important; /* Neon cyan border */
        }
        
        /* Button styling for Clear History and Submit Feedback */
        .stButton button, .stForm [data-testid="stFormSubmitButton"] button {
            background-color: #002222 !important;
            color: var(--neon-cyan) !important;
            border: 1px solid var(--neon-cyan) !important;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover, .stForm [data-testid="stFormSubmitButton"] button:hover {
            background-color: #400030 !important;
            border-color: var(--neon-pink) !important;
            color: var(--neon-pink) !important;
            box-shadow: 0 0 15px rgba(255, 105, 180, 0.3) !important;
        }
        
        .conversion-box {
            border: 2px solid var(--neon-cyan);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
            animation: fadeIn 1s ease-in-out;
        }
        
        .fun-fact {
            border-left: 4px solid var(--neon-cyan);
            padding: 10px;
            margin: 10px 0;
            background-color: #1a1a1a;
            animation: slideIn 0.5s ease-in-out;
        }
        
        .history-entry {
            border: 1px solid var(--neon-cyan);
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
            background-color: #1a1a1a;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        .feedback-box {
            border: 2px solid var(--neon-cyan);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            background-color: #1a1a1a;
            animation: fadeIn 1s ease-in-out;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: white !important; /* White color for headings */
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        /* Enhanced sidebar sections */
        .sidebar-fact, .sidebar-tip, .stats-box {
            background: linear-gradient(145deg, #0a0a0a, #1a1a1a);
            border-left: 3px solid var(--neon-cyan);
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            animation: slideIn 0.5s ease-in-out;
        }

        .sidebar-fact:hover, .sidebar-tip:hover, .stats-box:hover {
            border-color: var(--neon-pink) !important;
            border-left-color: var(--neon-pink) !important;
            box-shadow: 0 0 15px rgba(255, 105, 180, 0.2) !important;
            transform: translateX(5px);
        }

        /* Consistent form button styling */
        .stForm button[type="submit"] {
            background-color: #002222 !important;
            color: var(--neon-cyan) !important;
            border: 1px solid var(--neon-cyan) !important;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 10px;
        }

        .stForm button[type="submit"]:hover {
            background-color: #400030 !important;
            border-color: var(--neon-pink) !important;
            color: var(--neon-pink) !important;
            box-shadow: 0 0 15px rgba(255, 105, 180, 0.3) !important;
        }

        /* Enhanced stats box */
        .stats-box {
            background: linear-gradient(145deg, #0a0a0a, #1a1a1a);
            border: 1px solid var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.1);
        }

        .stats-box p {
            margin: 5px 0;
            font-size: 0.9em;
        }

        /* Conversion box hover effect */
        .conversion-box:hover {
            border-color: var(--neon-pink) !important;
            box-shadow: 0 0 20px rgba(255, 105, 180, 0.3) !important;
        }

        /* History entry hover effect */
        .history-entry:hover {
            border-color: var(--neon-pink) !important;
            box-shadow: 0 0 15px rgba(255, 105, 180, 0.2) !important;
            transform: translateX(5px);
        }

        /* Fun fact hover effect */
        .fun-fact:hover {
            border-left-color: var(--neon-pink) !important;
            box-shadow: 0 0 15px rgba(255, 105, 180, 0.2) !important;
        }

        /* Keep original cyan color for non-hover state */
        .stButton button, .stForm [data-testid="stFormSubmitButton"] button,
        .stTextInput input, .stNumberInput input, .stSelectbox select,
        .conversion-box, .history-entry, .sidebar-fact, .sidebar-tip,
        .stats-box, .fun-fact {
            border-color: var(--neon-cyan);
            transition: all 0.3s ease;
        }

        /* Ensure smooth transitions */
        * {
            transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
        }

        /* Number input styling */
        [data-testid="stNumberInput"] {
            background-color: transparent !important;
        }

        [data-testid="stNumberInput"] input {
            background-color: #1a1a1a !important;
            color: white !important;
            border: 1px solid var(--neon-cyan) !important;
            border-radius: 4px !important;
            outline: none !important;
            box-shadow: none !important;
        }

        /* Remove any additional borders from the container */
        [data-testid="stNumberInput"] > div {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }

        [data-testid="stNumberInput"] > div > div {
            border: none !important;
            outline: none !important;
        }

        /* Targeting the specific button elements with neon cyan */
        [data-testid="stNumberInput"] button[aria-label="Decrease number input"],
        [data-testid="stNumberInput"] button[aria-label="Increase number input"] {
            background-color: transparent !important;
            border: 1px solid var(--neon-cyan) !important;
            border-radius: 4px !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stNumberInput"] button[aria-label="Decrease number input"] svg,
        [data-testid="stNumberInput"] button[aria-label="Increase number input"] svg {
            fill: var(--neon-cyan) !important;
            transition: fill 0.3s ease !important;
        }

        /* Only hover color effect for +/- buttons */
         /* Enhanced hover effects for +/- buttons */
        [data-testid="stNumberInput"] button[aria-label="Decrease number input"]:hover,
        [data-testid="stNumberInput"] button[aria-label="Increase number input"]:hover {
            background-color: rgba(255, 105, 180, 0.2)!important;
            
        }
            [data-testid="stNumberInput"] button[aria-label="Decrease number input"]:hover svg,
        [data-testid="stNumberInput"] button[aria-label="Increase number input"]:hover svg {
            fill: var(--neon-pink) !important;
        }

        /* Additional specific targeting for number input buttons */
        [data-testid="stNumberInput"] div[data-baseweb="input"] div[role="spinbutton"] + div button {
            background-color: transparent !important;
            border: 1px solid var(--neon-cyan) !important;
        }
                 /* Additional specific targeting for hover effects */
        .stNumberInput button:hover {
            background-color: rgba(255, 105, 180, 0.2)!important;
           
        }

        [data-testid="stNumberInput"] div[data-baseweb="input"] div[role="spinbutton"] + div button svg {
            fill: var(--neon-cyan) !important;
        }
        [data-testid="stNumberInput"] button[aria-label="Decrease number input"]:hover svg,
        [data-testid="stNumberInput"] button[aria-label="Increase number input"]:hover svg {
            fill: var(--neon-pink) !important;
        }

        /* Remove any additional borders from the buttons */
        [data-testid="stNumberInput"] button {
            outline: none !important;
        }

        /* Override any default Streamlit styles */
        .stNumberInput button {
            background-color: transparent !important;
            border: 1px solid var(--neon-cyan) !important;
        }

        .stNumberInput button svg {
            fill: var(--neon-cyan) !important;
        }
        .stNumberInput button:hover svg {
            fill: var(--neon-pink) !important;
        }

                

        /* Textarea styling for feedback */
        .stTextArea textarea {
            background-color: #1a1a1a !important;
            color: white !important;
            border: 1px solid var(--neon-cyan) !important;
            border-radius: 4px !important;
        }

        .stTextArea textarea:hover {
            background-color: #222222 !important;
            border-color: var(--neon-pink) !important;
            box-shadow: 0 0 10px rgba(255, 105, 180, 0.2) !important;
        }
                

        .stTextArea textarea:focus {
            background-color: #2a2a2a !important;
            border-color: var(--neon-cyan) !important;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2) !important;
        }

        /* Enhanced main heading with neon effect */
        h1:first-of-type {
            color: white !important;
            text-shadow: 
                0 0 5px var(--neon-cyan),
                0 0 15px var(--neon-cyan),
                0 0 25px var(--neon-cyan),
                0 0 40px var(--neon-pink) !important;
            animation: glow 2s ease-in-out infinite alternate;
        }

        /* Glow animation for the heading */
        @keyframes glow {
            from {
                text-shadow: 
                    0 0 5px var(--neon-cyan),
                    0 0 15px var(--neon-cyan),
                    0 0 25px var(--neon-cyan),
                    0 0 40px var(--neon-pink);
            }
            to {
                text-shadow: 
                    0 0 10px var(--neon-cyan),
                    0 0 20px var(--neon-cyan),
                    0 0 30px var(--neon-cyan),
                    0 0 50px var(--neon-pink),
                    0 0 70px var(--neon-pink);
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Conversion function
def convert_units(value, from_unit, to_unit, conversion_type):
    if conversion_type == 'temperature':
        if from_unit == 'celsius' and to_unit == 'fahrenheit':
            return (value * 9/5) + 32
        elif from_unit == 'fahrenheit' and to_unit == 'celsius':
            return (value - 32) * 5/9
        else:
            return value
    else:
        factor_from = CONVERSIONS[conversion_type][from_unit]
        factor_to = CONVERSIONS[conversion_type][to_unit]
        return value * factor_from / factor_to

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []
if 'total_conversions' not in st.session_state:
    st.session_state.total_conversions = 0
if 'most_used_conversion' not in st.session_state:
    st.session_state.most_used_conversion = {'type': 'length', 'count': 0}
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# Add this function to track conversion types
def update_conversion_stats(conversion_type):
    if not hasattr(st.session_state, f'{conversion_type}_count'):
        setattr(st.session_state, f'{conversion_type}_count', 0)
    
    current_count = getattr(st.session_state, f'{conversion_type}_count') + 1
    setattr(st.session_state, f'{conversion_type}_count', current_count)
    
    if current_count > getattr(st.session_state, f'{st.session_state.most_used_conversion["type"]}_count', 0):
        st.session_state.most_used_conversion = {'type': conversion_type, 'count': current_count}

def main():

     # Add page configuration with metadata
    st.set_page_config(
        page_title="Quantum Unit Converter",
        page_icon="⇄",
       
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/YusraSaleem',
            'Report a bug': "https://github.com/YusraSaleem/quantum-converter/issues",
            'About': """
                # ⇄ Quantum Unit Converter
                A sleek, modern unit converter with neon aesthetics.
                
                ## Features
                - Multiple unit conversions
                - Real-time history tracking
                - Interactive neon interface
                - Mobile responsive design
                
                Created by Yusra Saleem
                """
        }
    )

    inject_custom_css()
    
    st.title("⇄ Quantum Unit Converter")
    st.markdown("---")
    
    # Sidebar with feedback at the bottom
    with st.sidebar:
        st.header("📜 Conversion History")
        
        # Clear all history button
        if st.button("Clear All History"):
            st.session_state.history = []
            st.session_state.total_conversions = 0
            for conv_type in CONVERSIONS.keys():
                setattr(st.session_state, f'{conv_type}_count', 0)
            st.session_state.most_used_conversion = {'type': 'length', 'count': 0}
            st.rerun()
        
        # Display and manage history entries
        for i, entry in enumerate(reversed(st.session_state.history)):
            with st.container():
                st.markdown(f"""
                <div class="history-entry">
                    <small>{entry['time']}</small>
                    <p>{entry['value']} {entry['from']} → {entry['result']:.2f} {entry['to']}</p>
                    <small>Type: {entry['conversion_type']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🗑️ Delete Entry {len(st.session_state.history) - i}"):
                    st.session_state.history.pop(-(i+1))
                    st.session_state.total_conversions -= 1
                    st.rerun()

        # Today's Unit Facts
        st.markdown("---")
        st.header("🎯 Today's Unit Facts")
        most_used = st.session_state.most_used_conversion
        st.markdown(f"""
        <div class="sidebar-fact">
            <p>Most used conversion today:</p>
            <p>- {most_used['type'].title()}: {most_used['count']} times</p>
        </div>
        """, unsafe_allow_html=True)

        # Updated Pro Tips Section
        st.markdown("---")
        st.header("🌟 Pro Tips")
        st.markdown("""
        <div class="sidebar-tip">
            <p>💡 Check history for recent conversions</p>
            <p>⚡ Use Clear History to reset all stats</p>
            <p>📊 Track your most used conversions</p>
            <p>💭 Share feedback to improve the app</p>
            <p>🎯 View stats to monitor usage</p>
        </div>
        """, unsafe_allow_html=True)

        # Live Stats Section
        st.markdown("---")
        st.header("📊 Live Stats")
        session_duration = time.time() - st.session_state.start_time
        hours = int(session_duration // 3600)
        minutes = int((session_duration % 3600) // 60)
        seconds = int(session_duration % 60)
        
        st.markdown(f"""
        <div class="stats-box">
            <p>⏰ Session Duration: {hours:02d}:{minutes:02d}:{seconds:02d}</p>
            <p>🔄 Total Conversions: {st.session_state.total_conversions}</p>
            <p>💭 Feedback Count: {len(st.session_state.feedback)}</p>
            <p>📈 Most Active Category: {most_used['type'].title()}</p>
        </div>
        """, unsafe_allow_html=True)

        # Feedback Section - Moved to the bottom
        st.markdown("---")
        st.header("💬 Feedback")
        with st.form("feedback_form", clear_on_submit=True):
            feedback = st.text_area("Share your thoughts or suggestions:")
            submitted = st.form_submit_button("Submit Feedback")
            if submitted and feedback.strip():
                st.session_state.feedback.append({
                    'time': time.strftime("%H:%M:%S"),
                    'feedback': feedback
                })
                st.success("Thank you for your feedback!")

    # Main conversion interface
    conversion_type = st.selectbox(
        "🔧 Select Conversion Type",
        ['length', 'weight', 'temperature', 'volume', 'speed', 'time']
    )
    
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox(
            "From",
            options=list(CONVERSIONS[conversion_type].keys())
        )
    with col2:
        to_unit = st.selectbox(
            "To",
            options=list(CONVERSIONS[conversion_type].keys())
        )
    
    value = st.number_input("Enter Value", min_value=0.0, step=0.1)
    
    if st.button("✨ Convert Now"):
        with st.spinner("Converting..."):
            time.sleep(0.5)
            result = convert_units(value, from_unit, to_unit, conversion_type)
            
            # Update statistics
            st.session_state.total_conversions += 1
            update_conversion_stats(conversion_type)
            
            # Add to history
            st.session_state.history.append({
                'time': time.strftime("%H:%M:%S"),
                'value': value,
                'from': from_unit,
                'to': to_unit,
                'result': result,
                'conversion_type': conversion_type
            })
            
            st.markdown(f"""
            <div class="conversion-box">
                <h3>🎉 Conversion Result</h3>
                <h2>{value:.2f} {from_unit} = {result:.2f} {to_unit}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # Popular Conversions Section
    with st.expander("🌟 Popular Conversions"):
        st.markdown("""
        **Commonly Used Conversions:**
        - **Length**: 1 meter = 3.28084 feet
        - **Weight**: 1 kilogram = 2.20462 pounds
        - **Temperature**: 0°C = 32°F
        - **Speed**: 1 mile per hour = 1.60934 kilometers per hour
        - **Time**: 1 day = 86400 seconds
        """)
    
    # Unit Facts Section
    with st.expander("📚 Unit Facts"):
        st.markdown("""
        **Interesting Facts About Units:**
        - The **meter** was originally defined as 1/10,000,000 of the distance from the equator to the North Pole.
        - The **kilogram** is the only SI base unit still defined by a physical artifact.
        - **Absolute zero** (-273.15°C) is the coldest possible temperature.
        - The **second** is defined based on the vibrations of a cesium atom.
        """)
    
    # About the App Section
    with st.expander("ℹ️ About the App"):
        st.markdown("""
        **Neon Unit Converter** is a sleek and modern tool for converting between various units. 
        - Built with **Python** and **Streamlit**.
        - Features a **dark theme** with neon accents.
        - Includes **real-time history**, **feedback submission**, and **fun facts**.
        - Designed for simplicity and ease of use.
        """)
    
    # Fun Facts Section
    with st.expander("🤯 Fun Facts"):
        st.markdown("""
        <div class="fun-fact">
            <h4>Did You Know? 🌍</h4>
            <p>The meter was originally defined as 1/10,000,000 of the distance from the equator to the North Pole!</p>
        </div>
        
        <div class="fun-fact">
            <h4>Science Fact 🔬</h4>
            <p>-273.15°C is absolute zero, the coldest possible temperature!</p>
        </div>
        
        <div class="fun-fact">
            <h4>History Note 📜</h4>
            <p>The kilogram is the only SI base unit still defined by a physical artifact!</p>
        </div>
        """, unsafe_allow_html=True)

          # Add footer at the bottom
    st.markdown("---")
    st.markdown("""
        <div style="
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #0a0a0a;
            padding: 10px;
            text-align: center;
            border-top: 1px solid var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
            z-index: 1000;
        ">
            <p style="
                color: white;
                margin: 0;
                font-size: 0.9em;
            ">
                Designed & Developed by 
                <span style="
                    color: var(--neon-cyan);
                    text-shadow: 0 0 5px var(--neon-cyan);
                ">Yusra Saleem</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()