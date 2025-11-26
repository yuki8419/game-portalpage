import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math

# Ensure images directory exists
if not os.path.exists('images'):
    os.makedirs('images')

def create_gradient(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (y / height)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def draw_glow(draw, x, y, r, color, blur_radius=10):
    # This is a simplified glow, for a real glow we'd need to blur a separate layer
    # For now, just drawing a semi-transparent larger circle
    for i in range(blur_radius, 0, -2):
        alpha = int(100 * (1 - i/blur_radius))
        # PIL draw doesn't support alpha directly on RGB images easily without RGBA
        # So we'll skip complex glow for simplicity in this script and stick to clean shapes
        pass

def generate_othello():
    width, height = 600, 400
    # Dark green gradient
    img = create_gradient(width, height, (10, 60, 30), (5, 30, 15))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Grid
    grid_size = 40
    rows = 8
    cols = 8
    start_x = (width - cols * grid_size) // 2
    start_y = (height - rows * grid_size) // 2
    
    # Draw board background
    draw.rectangle(
        [start_x - 10, start_y - 10, start_x + cols * grid_size + 10, start_y + rows * grid_size + 10],
        fill=(20, 80, 40, 200), outline=(50, 150, 80), width=2
    )

    for i in range(rows + 1):
        y = start_y + i * grid_size
        draw.line([(start_x, y), (start_x + cols * grid_size, y)], fill=(50, 150, 80), width=1)
    for i in range(cols + 1):
        x = start_x + i * grid_size
        draw.line([(x, start_y), (x, rows * grid_size + start_y)], fill=(50, 150, 80), width=1)

    # Pieces
    pieces = [
        (3, 3, 'white'), (4, 3, 'black'),
        (3, 4, 'black'), (4, 4, 'white'),
        (2, 4, 'black'), (2, 3, 'white'), # Some gameplay
        (5, 3, 'black')
    ]
    
    for c, r, color in pieces:
        cx = start_x + c * grid_size + grid_size // 2
        cy = start_y + r * grid_size + grid_size // 2
        radius = grid_size // 2 - 4
        
        fill_color = (240, 240, 240) if color == 'white' else (20, 20, 20)
        outline_color = (200, 200, 200) if color == 'white' else (50, 50, 50)
        
        # Shadow
        draw.ellipse([cx - radius + 2, cy - radius + 4, cx + radius + 2, cy + radius + 4], fill=(0,0,0, 100))
        # Piece
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=fill_color, outline=outline_color)
        
        # Highlight
        draw.ellipse([cx - radius + 5, cy - radius + 5, cx - radius + 12, cy - radius + 10], fill=(255, 255, 255, 100) if color == 'black' else (255, 255, 255, 200))

    # Text
    # try:
    #     font = ImageFont.truetype("arial.ttf", 40)
    #     draw.text((width - 150, height - 60), "OTHELLO", fill=(200, 255, 200), font=font)
    # except:
    #     pass

    img.save('images/othello_thumbnail.png')
    print("Generated Othello thumbnail")

def generate_shooter():
    width, height = 600, 400
    # Deep space gradient
    img = create_gradient(width, height, (10, 0, 30), (0, 0, 10))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Stars
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        brightness = random.randint(100, 255)
        size = random.randint(1, 3)
        draw.ellipse([x, y, x+size, y+size], fill=(brightness, brightness, brightness))

    # Player Ship (Triangle)
    ship_x, ship_y = width // 2, height - 80
    draw.polygon([
        (ship_x, ship_y - 30),
        (ship_x - 20, ship_y + 20),
        (ship_x, ship_y + 10),
        (ship_x + 20, ship_y + 20)
    ], fill=(0, 200, 255), outline=(100, 255, 255))
    
    # Engine glow
    draw.polygon([
        (ship_x - 10, ship_y + 20),
        (ship_x + 10, ship_y + 20),
        (ship_x, ship_y + 40)
    ], fill=(255, 100, 0, 180))

    # Lasers
    draw.line([(ship_x - 15, ship_y), (ship_x - 15, 0)], fill=(255, 0, 100), width=3)
    draw.line([(ship_x + 15, ship_y), (ship_x + 15, 0)], fill=(255, 0, 100), width=3)

    # Enemy
    enemy_x, enemy_y = width // 2 - 50, 100
    draw.polygon([
        (enemy_x, enemy_y),
        (enemy_x + 40, enemy_y),
        (enemy_x + 20, enemy_y + 30)
    ], fill=(255, 50, 50), outline=(255, 150, 150))
    
    # Explosion
    exp_x, exp_y = width // 2 + 50, 80
    for _ in range(20):
        r = random.randint(5, 20)
        ox = exp_x + random.randint(-20, 20)
        oy = exp_y + random.randint(-20, 20)
        color = random.choice([(255, 200, 0), (255, 100, 0), (255, 255, 200)])
        draw.ellipse([ox-r, oy-r, ox+r, oy+r], fill=color + (200,))

    img.save('images/space_shooter_thumbnail.png')
    print("Generated Shooter thumbnail")

def generate_tetris():
    width, height = 600, 400
    # Dark background
    img = Image.new('RGB', (width, height), (20, 20, 25))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Grid lines (subtle)
    block_size = 30
    for x in range(0, width, block_size):
        draw.line([(x, 0), (x, height)], fill=(40, 40, 50), width=1)
    for y in range(0, height, block_size):
        draw.line([(0, y), (width, y)], fill=(40, 40, 50), width=1)

    colors = [
        (0, 240, 240), # Cyan
        (0, 0, 240),   # Blue
        (240, 160, 0), # Orange
        (240, 240, 0), # Yellow
        (0, 240, 0),   # Green
        (160, 0, 240), # Purple
        (240, 0, 0)    # Red
    ]

    # Draw some blocks at the bottom
    for x in range(0, width, block_size):
        if random.random() > 0.3:
            height_blocks = random.randint(1, 5)
            for i in range(height_blocks):
                y = height - (i + 1) * block_size
                color = random.choice(colors)
                # Block body
                draw.rectangle([x+1, y+1, x+block_size-1, y+block_size-1], fill=color)
                # Highlight
                draw.line([(x+1, y+1), (x+block_size-1, y+1)], fill=(255, 255, 255, 150), width=2)
                draw.line([(x+1, y+1), (x+1, y+block_size-1)], fill=(255, 255, 255, 150), width=2)
                # Shadow
                draw.line([(x+block_size-1, y+1), (x+block_size-1, y+block_size-1)], fill=(0, 0, 0, 100), width=2)
                draw.line([(x+1, y+block_size-1), (x+block_size-1, y+block_size-1)], fill=(0, 0, 0, 100), width=2)

    # Falling piece (T-shape)
    fx, fy = width // 2, 100
    f_color = (160, 0, 240) # Purple
    
    # T shape coordinates relative to center
    t_blocks = [(0, 0), (-1, 0), (1, 0), (0, -1)]
    
    for dx, dy in t_blocks:
        bx = fx + dx * block_size
        by = fy + dy * block_size
        draw.rectangle([bx+1, by+1, bx+block_size-1, by+block_size-1], fill=f_color)
        # Highlight/Shadow for falling piece
        draw.line([(bx+1, by+1), (bx+block_size-1, by+1)], fill=(255, 255, 255, 200), width=2)
        draw.line([(bx+1, by+1), (bx+1, by+block_size-1)], fill=(255, 255, 255, 200), width=2)
        draw.line([(bx+block_size-1, by+1), (bx+block_size-1, by+block_size-1)], fill=(0, 0, 0, 100), width=2)
        draw.line([(bx+1, by+block_size-1), (bx+block_size-1, by+block_size-1)], fill=(0, 0, 0, 100), width=2)
        
        # Glow effect (simple)
        draw.rectangle([bx-2, by-2, bx+block_size+2, by+block_size+2], outline=f_color, width=1)

    img.save('images/tetris_thumbnail.png')
    print("Generated Tetris thumbnail")

if __name__ == "__main__":
    generate_othello()
    generate_shooter()
    generate_tetris()
