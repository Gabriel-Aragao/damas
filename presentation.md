# Checkers Game Implementation

## Introduction

This presentation explains how our Checkers game was implemented using Python and Pygame. We'll cover the architecture, key libraries, and important code sections that bring this classic board game to life.

## Libraries Used

### Pygame
- **Purpose**: Provides graphics, input handling, and game loop functionality
- **Key Features**:
  - Rendering game elements (board, pieces)
  - Handling mouse and keyboard input
  - Managing display window and game loop

### Asyncio
- **Purpose**: Enables non-blocking operations for improved responsiveness
- **Key Features**:
  - Allows the game to yield control during AI thinking
  - Makes UI responsive when running in a browser environment
  - Powers asynchronous game loop and menu handling

## Project Architecture

The project follows the Model-View-Controller (MVC) pattern:

### Model
- Game state, board logic, and rules
- Located in `src/model/`

### View
- UI rendering and display
- Located in `src/view/`

### Controller
- Game logic, input handling, and AI
- Located in `src/controller/`

### Configuration
- Constants, settings, and configuration management
- Located in `src/config/`

## Key Code Components

### 1. Game Initialization

```python
async def main():
    pygame.init()
    # Define as dimensões da tela usando as constantes fornecidas
    screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))
    
    running = True
    while running:
        # Cede o controle para que o navegador possa atualizar
        await asyncio.sleep(0)
        # Obtém a seleção do menu
        selection = await handle_main_menu(screen)
        
        if selection == "1v1":
            # Modo Jogador contra Jogador
            await handle_game_loop(screen, mode='pvp')
        elif selection == "ai":
            # Modo Jogador contra IA
            await handle_game_loop(screen, mode='ai')
        elif selection == "exit":
            running = False
```

This code initializes Pygame, creates the game window, and sets up the main game loop that handles menu selection and starts different game modes.

### 2. Board Representation

```python
def create_board():
    """
    Cria um tabuleiro 8x8 onde cada quadrado é inicializado como '.' (vazio).
    """
    board = [['.' for _ in range(8)] for _ in range(8)]
    return board

def initialize_pieces(board):
    """
    Configura as peças iniciais no tabuleiro.
    Peças vermelhas ('r') são colocadas nas linhas inferiores e peças pretas ('b') nas linhas superiores.
    As peças ocupam apenas quadrados jogáveis ((row + col) % 2 != 0).
    """
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 != 0:
                if row < 3:
                    board[row][col] = 'b'
                elif row > 4:
                    board[row][col] = 'r'
    return board
```

The board is represented as an 8x8 2D array where:
- '.' represents empty squares
- 'r' represents red pieces
- 'b' represents black pieces
- 'R' represents red kings
- 'B' represents black kings

### 3. Move Mechanics

```python
def make_move(board, start_row, start_col, end_row, end_col):
    """
    Move uma peça de (start_row, start_col) para (end_row, end_col).
    """
    piece = board[start_row][start_col]
    board[start_row][start_col] = '.'
    dr = end_row - start_row
    dc = end_col - start_col
    abs_dr = abs(dr)
    abs_dc = abs(dc)
    
    # Verificações de movimento diagonal...
    
    # Para movimentos de dama ou qualquer movimento que abrange mais de um quadrado
    if piece.isupper() or abs_dr > 1:
        # Lógica para movimentos de dama ou capturas...
    else:
        # Para um movimento de captura simples
        if abs_dr == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            board[mid_row][mid_col] = '.'
    
    # Coloca a peça no destino
    board[end_row][end_col] = piece
    
    # Promoção para dama
    if piece == 'r' and end_row == 0:
        board[end_row][end_col] = 'R'
    elif piece == 'b' and end_row == len(board) - 1:
        board[end_row][end_col] = 'B'
```

This function handles the core mechanics of piece movement, including:
- Basic moves
- Captures
- King promotion
- Multi-square king moves

### 4. Game Loop

```python
async def handle_game_loop(screen, mode='pvp'):
    """
    Manipulador do loop principal do jogo de damas.
    Suporta modos PvP e IA.
    """
    # Inicializa o estado do jogo
    game_state = initialize_game()
    game_state['mode'] = mode
    
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        
        # Lógica da IA quando for sua vez
        if game_state.get('mode') == 'ai' and game_state['current_player'] == 'BLACK':
            handle_ai_turn(game_state)
            render_game_state(screen, game_state)
            await asyncio.sleep(0.5)
            continue
        
        # Processamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                # Menu de pausa
                if event.key == pygame.K_ESCAPE:
                    action = await handle_pause_menu(screen)
                    if action:
                        return action
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_game_input(event, game_state)
        
        # Renderização
        render_game_state(screen, game_state)
        
        # Verificação de fim de jogo
        if game_state.get('game_over'):
            draw_game_over(screen, game_state.get('winner', 'Ninguém'))
            await asyncio.sleep(2)
            return "menu"
        
        pygame.display.flip()
        await asyncio.sleep(0)
```

The game loop handles:
- Frame rate control
- Input processing
- AI turn management
- Game state updates
- Rendering
- Game over conditions

### 5. Rendering the Board and Pieces

```python
def draw_board(screen):
    """Desenha o padrão do tabuleiro de damas."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Calcula a posição do quadrado
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            
            # Alterna cores para o padrão do tabuleiro
            color = COLORS['BOARD_LIGHT'] if (row + col) % 2 == 0 else COLORS['BOARD_DARK']
            
            # Desenha o quadrado
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

def draw_piece(screen, piece, row, col):
    """Desenha uma peça individual."""
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
    radius = (SQUARE_SIZE // 2) - PIECE_PADDING
    
    # Determina a cor da peça
    color = COLORS['RED_PIECE'] if piece.lower() == 'r' else COLORS['BLACK_PIECE']
    
    # Desenha o círculo principal da peça
    pygame.draw.circle(screen, color, (x, y), radius)
    
    # Desenha o indicador de dama se a peça for uma dama
    if piece.isupper():
        crown_radius = radius - 10
        pygame.draw.circle(screen, COLORS['BOARD_LIGHT'], (x, y), crown_radius)
        pygame.draw.circle(screen, color, (x, y), crown_radius - 5)
```

These functions visualize the game state:
- `draw_board()` creates the checkerboard pattern
- `draw_piece()` renders individual pieces with special visualization for kings

## Game Settings and Constants

The game includes configurable settings:

```python
# Configurações do Tabuleiro
BOARD_SIZE = 8
SQUARE_SIZE = 80
PIECE_PADDING = 10  # Espaço entre a peça e a borda do quadrado

# Cores
COLORS = {
    'BOARD_LIGHT': (255, 255, 255),  # Quadrados brancos
    'BOARD_DARK': (128, 128, 128),   # Quadrados cinza escuro
    'RED_PIECE': (220, 20, 60),      # Peças vermelhas
    'BLACK_PIECE': (0, 0, 0),        # Peças pretas
    'HIGHLIGHT': (255, 255, 0, 128), # Destaque amarelo
    'VALID_MOVE': (0, 255, 0, 128),  # Pontos verdes para movimentos válidos
    'SELECTED': (0, 0, 255, 128)     # Destaque azul para peça selecionada
}

# Regras do Jogo
FORCE_CAPTURE = True  # Forçar jogador a capturar quando possível
MULTIPLE_JUMPS = False # Permitir múltiplas capturas em um turno
KINGS_MOVE_MULTIPLE = True  # Permitir que damas movam múltiplos quadrados
```

## User Interaction

```python
def handle_game_input(event, game_state):
    """Manipula a entrada do jogador durante o jogo."""
    if event.type != pygame.MOUSEBUTTONDOWN:
        return
    
    # Converte posição do mouse para coordenadas do tabuleiro
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    
    board = game_state['board']
    current_player = game_state['current_player']
    
    # Seleção e movimentação de peças
    if not game_state.get('selected_piece'):
        # Lógica de seleção de peça
        piece = board[row][col]
        if piece.lower() == current_player[0].lower():
            valid_moves = get_valid_moves(board, row, col)
            if valid_moves:
                game_state['selected_piece'] = (row, col)
                game_state['valid_moves'] = valid_moves
    else:
        # Lógica de movimentação
        start_row, start_col = game_state['selected_piece']
        
        # Verifica movimentos válidos
        valid_move = None
        for move in game_state['valid_moves']:
            if move[0] == row and move[1] == col:
                valid_move = move
                break
        
        if valid_move:
            update_game_state(game_state, valid_move)
        else:
            # Desseleciona se o movimento for inválido
            game_state['selected_piece'] = None
            game_state['valid_moves'] = []
```

This code handles:
- Converting mouse clicks to board coordinates
- Selecting pieces
- Validating and executing moves
- Updating the game state

## Conclusion

Our Checkers game demonstrates:
- Clean architecture using MVC pattern
- Effective use of Pygame for rendering
- Asynchronous programming with asyncio
- Well-structured game rules and logic
- Intuitive user interface

The code is designed to be modular, maintainable, and extensible, allowing for easy addition of features like different AI difficulties, rule variations, or visual enhancements.