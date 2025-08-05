# app.py
import streamlit as st
import numpy as np
import time
from solver import solve_sudoku, check_initial_board, find_empty
from ui import render_sidebar, render_main_content, draw_grid

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Streamlit Sudoku Solver", layout="wide")
    st.title("Interactive Sudoku Solver")
    st.write("Enter a puzzle below. Leave cells blank for the solver to fill.")

    if 'board' not in st.session_state:
        st.session_state.board = np.zeros((9, 9), dtype=int).tolist()

    load_example, clear_board, animation_speed = render_sidebar()

    if load_example:
        st.session_state.board = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0], [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8], [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0], [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2], [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
        st.rerun()

    if clear_board:
        st.session_state.board = np.zeros((9, 9), dtype=int).tolist()
        st.rerun()

    grid_placeholder = st.empty()
    check_button, solve_button = render_main_content()
    message_placeholder = st.empty()

    invalid_cell_to_show = None

    if check_button:
        is_valid, cell = check_initial_board([row[:] for row in st.session_state.board])
        if is_valid:
            message_placeholder.success("The initial board is valid!")
        else:
            message_placeholder.error(f"Invalid board! Conflict at row {cell[0]+1}, col {cell[1]+1}.")
            invalid_cell_to_show = cell

    if solve_button:
        is_valid, cell = check_initial_board([row[:] for row in st.session_state.board])
        if not is_valid:
            message_placeholder.error(f"Cannot solve! Conflict at row {cell[0]+1}, col {cell[1]+1}.")
            invalid_cell_to_show = cell
        else:
            board_copy = [row[:] for row in st.session_state.board]
            solution_generator = solve_sudoku(board_copy)

            final_board = None
            for solved_board in solution_generator:
                final_board = solved_board

            if final_board and find_empty(final_board) is None:
                st.session_state.board = final_board
                message_placeholder.success("Sudoku Solved!")
                st.balloons()
            else:
                message_placeholder.warning("This puzzle is unsolvable.")

            with grid_placeholder.container():
                draw_grid(st.session_state.board)

    
    # This is the single, final draw call for the grid unless the solver is running.
    # This prevents the DuplicateWidgetID error.
    if not solve_button:
        with grid_placeholder.container():
            draw_grid(st.session_state.board, invalid_cell=invalid_cell_to_show)

if __name__ == "__main__":
    main()

