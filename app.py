import colorsys
import streamlit as st
import streamlit.components.v1 as components

def generate_colors(n):
    colors = []
    for i in range(n):
        # Generate colors with varying hues
        hue = i / n
        # Use a fixed saturation and value (brightness)
        saturation = 0.7
        value = 0.9
        # Convert HSV to RGB
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        # Convert RGB to hexadecimal
        hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        colors.append(hex_color)
    return colors



def display_wheel(outcomes):

    colors = generate_colors(len(outcomes))

    div_elements = '\n'.join([
        f'            <div class="number" style="--i:{i+1};--clr:{colors[i]}"><span>{outcomes[i]}</span></div>'
        for i in range(len(outcomes))
    ])

    angle = 360/len(outcomes)
    polygon_size = angle + 14



    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Spinning wheel</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
            }}

            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: #333;
            }}

            .container {{
                position: relative;
                width: 400px;
                height: 400px;
                display: flex;
                justify-content: center;
                align-items: center;
            

                .spinBtn {{
                    position: absolute;
                    width: 60px;
                    height: 60px;
                    background: #fff;
                    border-radius: 50%;
                    z-index: 10;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-transform: uppercase;
                    font-weight: 600;
                    color: #333;
                    letter-spacing: .1em;
                    border: 4px solid rgba(0, 0, 0, 0.75);
                    cursor: pointer;
                    user-select: none;
                }}

                .spinBtn::before {{
                    content: '';
                    position: absolute;
                    top: -28px;
                    width: 20px;
                    height: 30px;
                    background: #fff;
                    clip-path: polygon(50% 0%, 15% 100%, 85% 100%);
                }}

                .wheel {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: #333;
                    border-radius: 50%;
                    overflow: hidden;
                    box-shadow: 0 0 0 5px #333,
                    0 0 0 15px #fff,
                    0 0 0 18px #111;
                    transition: transform 6s ease-in-out;
                

                    .number {{
                        position: absolute;
                        width: 50%;
                        height: 50%;
                        background: var(--clr);
                        transform-origin: bottom right;
                        transform: rotate(calc(var(--angle) * var(--i)));
                        clip-path: polygon(0 0, {polygon_size}% 0, 100% 100%, 0 {polygon_size}%);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        user-select: none;
                        cursor: pointer;
                    

                        span {{
                            position: relative;
                            transform: rotate(calc(var(--angle)));
                            font-size: 1.4em;
                            font-weight: 700;
                            color: #fff;
                            text-shadow: 3px 5px 2px rgba(0, 0, 0, 0.15);
                        }}
                    
                    }}

                }}

            }}        
        </style>
    </head>
    <body>
        <div class="container">
            <div class="spinBtn">spin</div>
            <div class="wheel">
                {div_elements}
            </div>
        </div>
        <script>
            let wheel = document.querySelector('.wheel');
            let spinBtn = document.querySelector('.spinBtn');
            let value = Math.ceil(Math.random() * 3600);

            document.addEventListener('DOMContentLoaded', function() {{
                const wheel = document.querySelector('.wheel');
                const elements = document.querySelectorAll('.number');
                const totalElements = elements.length;

                // Set CSS variables
                wheel.style.setProperty('--total-elements', totalElements);
                wheel.style.setProperty('--angle', `{angle}deg`);

            }});

            spinBtn.onclick = function() {{
                wheel.style.transform = "rotate(" + value + "deg)";
                value += Math.ceil(Math.random() * 3600);
            }}
        </script>
    </body>
    </html>"""


    components.html(html_content, height=600)



def update_outcomes():
    st.session_state.outcomes = set([elem for elem, checked in st.session_state.checkboxes.items() if checked])



st.set_page_config(
        page_title="Spinning wheel", layout="wide",
    )

st.title('Spinning wheel (click multiple times to spin faster)')


if 'outcomes' not in st.session_state:
    st.session_state.outcomes = set()


new_outcome = st.text_input('Add an outcome')

if st.button("Add"):
    if new_outcome:
        st.session_state.outcomes.add(new_outcome)
        st.rerun()
    else:
        st.warning("Please enter an outcome")


st.write("Current outcomes :")

# Display the checkboxes for each element
st.session_state.checkboxes = {}
for elem in st.session_state.outcomes:
    st.session_state.checkboxes[elem] = st.checkbox(elem, value=True, key=elem)

if st.button("Update outcomes after unticking elements"):
    update_outcomes()
    st.rerun()


if st.button('Reset outcomes'):
    st.session_state.outcomes = set()
    st.rerun()



if st.button('Spin the wheel'):

    outcomes = list(st.session_state.outcomes)

    if len(outcomes) > 3:
        display_wheel(outcomes)

    elif len(outcomes) == 3:
        st.warning('Bug for 3 outcomes : wheel is unfulfilled')
        display_wheel(outcomes)

    elif len(outcomes) == 2:
        outcomes += outcomes
        display_wheel(outcomes)

    elif len(outcomes) == 1:
        for _ in range(2):
            outcomes += outcomes
        display_wheel(outcomes)

    else:
        st.error('No outcome selected !')