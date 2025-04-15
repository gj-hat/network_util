
"""
 @author：     JiaGuo
 @emil：       1520047927@qq.com
 @date：       Created in 2025/4/9 17:27
 @description： banner工具类
 @modified By：
 @version:     1.0
"""

from wcwidth import wcswidth
class Banner:
    def __init__(self, width: int, border_char: str = '*'):
        if width < 4:
            raise ValueError("宽度不能小于4")
        if len(border_char) != 1:
            raise ValueError("边框字符只能是一个字符")
        self.width = width
        self.border_char = border_char

    def display_width(self, text: str) -> int:
        return wcswidth(text)

    def create(self, lines: list[str]) -> str:
        content_width = self.width - 2  # 去掉左右边框
        banner_lines = []

        # 顶部边框
        banner_lines.append(self.border_char * self.width)

        for line in lines:
            line = line.strip()
            line_display_width = self.display_width(line)

            if line_display_width > content_width:
                # 截断到刚好不超过宽度（需逐个字符判断）
                truncated = ''
                total = 0
                for ch in line:
                    ch_width = self.display_width(ch)
                    if total + ch_width > content_width:
                        break
                    truncated += ch
                    total += ch_width
                line = truncated
                line_display_width = total

            padding_total = content_width - line_display_width
            left_padding = padding_total // 2
            right_padding = padding_total - left_padding

            content_line = (
                self.border_char +
                ' ' * left_padding +
                line +
                ' ' * right_padding +
                self.border_char
            )
            banner_lines.append(content_line)

        # 底部边框
        banner_lines.append(self.border_char * self.width)

        return '\n'.join(banner_lines)


if __name__ == "__main__":
    banner = Banner(width=40, border_char='#')
    lines = ["欢迎使用", "Python Banner 工具", "祝你编程愉快!"]
    print(banner.create(lines))
