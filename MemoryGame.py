import pyxel
import random

class MemoryGame:
    def __init__(self):
        pyxel.init(128, 128, title="メモリーゲーム")
        self.initial_grid_size = 4
        self.advanced_grid_size = 8
        self.cell_size = 16
        self.grid_size = self.initial_grid_size
        self.sample_pattern = self.generate_pattern(self.grid_size)
        self.user_pattern = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.show_sample = True
        self.timer = 0
        self.error_count = 0
        self.game_over = False
        self.level = 1
        self.time_limit = 30 * 60
        self.game_started = False

        # 音響フィードバック用のサウンドを設定
        pyxel.sound(0).set("c3", "p", "3", "s", 10)
        pyxel.sound(1).set("g3", "t", "7", "n", 10)

        self.cell_highlight = None
        self.highlight_duration = 10
        self.highlight_timer = 0

        self.skip_remaining = 2  # ゲーム全体でのスキップ残数

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.grid_size = self.initial_grid_size
        self.sample_pattern = self.generate_pattern(self.grid_size)
        self.user_pattern = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.show_sample = True
        self.timer = 0
        self.error_count = 0
        self.game_over = False
        self.level = 1
        self.time_limit = 30 * 60
    # 必要に応じて他の変数もリセット


    def generate_pattern(self, size):
        return [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]

    def update(self):
        if not self.game_started:
            if pyxel.btnp(pyxel.KEY_S):
                self.game_started = True
            return
        if self.game_over:
            if self.game_over:
                if pyxel.btnp(pyxel.KEY_R):
                    self.reset_game()
                return 

        if self.cell_highlight:
            self.highlight_timer += 1
            if self.highlight_timer > self.highlight_duration:
                self.cell_highlight = None
                self.highlight_timer = 0

        if self.show_sample:
            self.timer += 1
            if self.timer > 300:
                self.show_sample = False
                self.timer = 0
        else:
            self.timer += 1
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                x, y = pyxel.mouse_x // self.cell_size, pyxel.mouse_y // self.cell_size
                if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                    if self.sample_pattern[y][x] == 0:
                        self.error_count += 1
                        pyxel.play(0, 1)
                        self.cell_highlight = (x, y, 8)
                        if self.error_count >= 3:
                            self.game_over = True
                    else:
                        self.user_pattern[y][x] = 1
                        pyxel.play(0, 0)
                        self.cell_highlight = (x, y, 11)
                        if self.check_clear():
                            self.level += 1
                            if self.level == 4:
                                self.grid_size = self.advanced_grid_size
                                self.cell_size = 128 // self.advanced_grid_size
                            self.next_level()

            if self.timer > self.time_limit:
                self.game_over = True

            # スキップ機能の処理
            if pyxel.btnp(pyxel.KEY_S) and self.skip_remaining > 0:
                self.skip_remaining -= 1
                self.next_level()

    def check_clear(self):
        return self.sample_pattern == self.user_pattern

    def next_level(self):
        self.sample_pattern = self.generate_pattern(self.grid_size)
        self.user_pattern = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.show_sample = True
        self.timer = 0
        self.error_count = 0

    def draw(self):
        if not self.game_started:
            self.draw_centered_text("MeoryGame", pyxel.height // 2 - 10, pyxel.COLOR_YELLOW)
            self.draw_centered_text("Press S to start", pyxel.height // 2 + 10, pyxel.COLOR_WHITE)
            return
        pyxel.cls(0)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                pyxel.rectb(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, pyxel.COLOR_GRAY)
                if self.show_sample and self.sample_pattern[y][x] == 1:
                    pyxel.rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, 11)
                elif self.user_pattern[y][x] == 1:
                    pyxel.rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, 7)

                if self.cell_highlight and self.cell_highlight[0] == x and self.cell_highlight[1] == y:
                    pyxel.rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, self.cell_highlight[2])

        cursor_size = 3
        cursor_x = min(pyxel.mouse_x, pyxel.width - cursor_size)
        cursor_y = min(pyxel.mouse_y, pyxel.height - cursor_size)
        pyxel.rect(cursor_x, cursor_y, cursor_size, cursor_size, pyxel.COLOR_RED)

        # スキップ残数の表示
        pyxel.text(72, 120, f"Skips left: {self.skip_remaining}", pyxel.COLOR_YELLOW)
        pyxel.text(3, 3, f"Errors Left: {3 - self.error_count}", pyxel.COLOR_YELLOW)

        if self.game_over:
            if self.game_over:
                pyxel.cls(0)  
                self.draw_centered_text("GAME OVER", pyxel.height // 2 - 10, pyxel.COLOR_RED)
                self.draw_centered_text(f"Rounds Cleared: {self.level - 1}", pyxel.height // 2, pyxel.COLOR_YELLOW)
                self.draw_centered_text("R to Restart", pyxel.height // 2 + 10, pyxel.COLOR_WHITE)

    def draw_centered_text(self, text, y, color):
        """テキストを画面中央に表示するヘルパー関数"""
        text_width = pyxel.FONT_WIDTH * len(text)
        text_x = (pyxel.width - text_width) // 2
        pyxel.text(text_x, y, text, color)


if __name__ == "__main__":
    MemoryGame()
