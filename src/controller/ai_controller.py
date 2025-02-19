def handle_ai_game_loop(screen):
    game_state = initialize_game()
    while not game_state['game_over']:
        if game_state['current_player'] == 'ai':
            ai_move = calculate_ai_move(game_state)
            update_game_state(game_state, ai_move)
        else:
            handle_player_input(game_state)
        render_board(screen, game_state)
