import streamlit as st

def render_sidebar():
    """Renders the sidebar controls and returns the animation speed."""
    with st.sidebar:
        st.header("Controls")
        
        load_example = st.button("Load Example Puzzle", key="load_example")
        clear_board = st.button("Clear Board", key="clear")
        
        st.markdown("---")
        animation_speed = st.slider("Animation Speed (sec)", 0.0, 0.2, 0.01, key="speed")
        
    return load_example, clear_board, animation_speed

def render_main_content():
    """Renders the main buttons and returns their state."""
    col1, col2 = st.columns(2)
    with col1:
        check_button = st.button("Check Validity", use_container_width=True)
    with col2:
        solve_button = st.button("Solve", type="primary", use_container_width=True)
    return check_button, solve_button

def draw_grid(board, invalid_cell=None, key_suffix=""):

    """Draws the Sudoku grid and handles user input."""
    st.markdown("""
        <style>
        .stTextInput input {
            font-size: 1.5rem; text-align: center; height: 50px; width: 50px;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(9)
    for j in range(9):
        with cols[j]:
            for i in range(9):
                # Get the original value from the board state
                original_board_value = board[i][j]
                
                # Format the value for display (0 becomes an empty string)
                display_value = str(original_board_value) if original_board_value != 0 else ""
                
                # Determine the label (for showing validation errors)
                label = "⚠️" if invalid_cell and invalid_cell == (i, j) else " "

                # Create the text input widget
                new_text_value = st.text_input(
                            label=label,
                            value=display_value,
                            key=f"cell_{i}_{j}_{key_suffix}",
                            max_chars=1,
                        )


                # --- New, Improved Input Handling Logic ---
                # Check if the user's input has changed
                if new_text_value != display_value:
                    try:
                        # An empty string means the user cleared the cell.
                        new_int_value = 0
                        if new_text_value: # If not an empty string
                            new_int_value = int(new_text_value)

                        # Check if the number is a valid Sudoku number (1-9) or 0 for empty
                        if 0 <= new_int_value <= 9:
                            # If valid, update the board state in the session
                            st.session_state.board[i][j] = new_int_value
                        else:
                            # If it's a number but out of range (e.g., -5), reject the change by re-running.
                            st.rerun()

                    except ValueError:
                        # If the input is not a number (e.g., 'a'), reject it by re-running.
                        st.rerun()

