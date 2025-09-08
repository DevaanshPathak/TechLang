from typing import List, Optional
from .core import InterpreterState

try:
    from PIL import Image, ImageDraw, ImageFont  # type: ignore
except Exception:  # pragma: no cover
    Image = None
    ImageDraw = None
    ImageFont = None


class GraphicsContext:
    image = None
    draw = None
    width = 0
    height = 0


class GraphicsOpsHandler:
    """Simple in-memory canvas that can be saved on graphics_show."""

    @staticmethod
    def handle_graphics_init(state: InterpreterState, tokens: List[str], index: int) -> int:
        if Image is None:
            state.add_error("Pillow (PIL) not installed")
            return 2
        if index + 2 >= len(tokens):
            state.add_error("graphics_init requires width and height")
            return 0
        try:
            w = int(tokens[index + 1])
            h = int(tokens[index + 2])
        except ValueError:
            state.add_error("graphics_init width/height must be integers")
            return 0
        GraphicsContext.image = Image.new("RGB", (w, h), color=(255, 255, 255))
        GraphicsContext.draw = ImageDraw.Draw(GraphicsContext.image)
        GraphicsContext.width = w
        GraphicsContext.height = h
        state.add_output(f"Canvas {w}x{h} initialized")
        return 2

    @staticmethod
    def handle_graphics_draw_line(state: InterpreterState, tokens: List[str], index: int) -> int:
        if GraphicsContext.draw is None:
            state.add_error("graphics_init must be called first")
            return 0
        if index + 4 >= len(tokens):
            state.add_error("graphics_draw_line requires x1 y1 x2 y2")
            return 0
        try:
            x1 = int(tokens[index + 1]); y1 = int(tokens[index + 2])
            x2 = int(tokens[index + 3]); y2 = int(tokens[index + 4])
        except ValueError:
            state.add_error("graphics_draw_line coordinates must be integers")
            return 0
        GraphicsContext.draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=2)
        return 4

    @staticmethod
    def handle_graphics_draw_circle(state: InterpreterState, tokens: List[str], index: int) -> int:
        if GraphicsContext.draw is None:
            state.add_error("graphics_init must be called first")
            return 0
        if index + 3 >= len(tokens):
            state.add_error("graphics_draw_circle requires x y radius")
            return 0
        try:
            x = int(tokens[index + 1]); y = int(tokens[index + 2]); r = int(tokens[index + 3])
        except ValueError:
            state.add_error("graphics_draw_circle parameters must be integers")
            return 0
        bbox = (x - r, y - r, x + r, y + r)
        GraphicsContext.draw.ellipse(bbox, outline=(0, 0, 0), width=2)
        return 3

    @staticmethod
    def handle_graphics_draw_text(state: InterpreterState, tokens: List[str], index: int) -> int:
        if GraphicsContext.draw is None:
            state.add_error("graphics_init must be called first")
            return 0
        if index + 3 >= len(tokens):
            state.add_error("graphics_draw_text requires x y \"text\"")
            return 0
        try:
            x = int(tokens[index + 1]); y = int(tokens[index + 2])
        except ValueError:
            state.add_error("graphics_draw_text coordinates must be integers")
            return 0
        text_token = tokens[index + 3]
        if not (text_token.startswith('"') and text_token.endswith('"')):
            state.add_error("graphics_draw_text requires quoted text")
            return 0
        text = text_token[1:-1]
        GraphicsContext.draw.text((x, y), text, fill=(0, 0, 0))
        return 3

    @staticmethod
    def handle_graphics_show(state: InterpreterState) -> None:
        if GraphicsContext.image is None:
            state.add_error("graphics_init must be called first")
            return
        # Save to file in CWD
        out_path = "techlang_canvas.png"
        GraphicsContext.image.save(out_path)
        state.add_output(f"Canvas saved to {out_path}")


