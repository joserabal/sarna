from typing import *

import mistletoe
from docxtpl import DocxTemplate
from mistletoe.base_renderer import BaseRenderer

from report_generator.style import RenderStyle
from sarna.report_generator import *


class DOCXRenderer(BaseRenderer):
    """
    DOCX renderer class.

    See mistletoe.base_renderer module for more info.
    """

    def __call__(self, *args, **kwargs):
        self.warnings = set()
        return self

    def __init__(self, docx: DocxTemplate, img_path_trans: Callable):
        """
        Args:
            extras (list): allows subclasses to add even more custom tokens.
        """
        self.warnings = set()
        self.style = None
        self._tpl = docx
        self._img_path = img_path_trans
        self._suppress_ptag_stack = [False]
        self._suppress_rtag_stack = [False]
        self._list_style_stack = []
        self._mod_pstyle_stack = []
        self._list_level = -1
        super().__init__()

    def set_style(self, style: RenderStyle):
        self.style = style

    def render_strong(self, token):
        self._suppress_rtag_stack.append(True)
        render = make_run(self.style.strong, self.render_inner(token))
        self._suppress_rtag_stack.pop()
        return str(render)

    def render_emphasis(self, token):
        self._suppress_rtag_stack.append(True)
        render = make_run(self.style.italic, self.render_inner(token))
        self._suppress_rtag_stack.pop()
        return str(render)

    def render_inline_code(self, token):
        self.warnings.add('Marckdown inline code is not implemented. It will be ignored')
        return ''

    def render_strikethrough(self, token):
        self._suppress_rtag_stack.append(True)
        render = make_run(self.style.strike, self.render_inner(token))
        self._suppress_rtag_stack.pop()
        return str(render)

    def render_image(self, token):
        inner = self.render_inner(token)
        section = self._tpl.docx.sections[0]

        path = self._img_path(token.src)

        pic = self._tpl.docx._part.new_pic_inline(
            path,
            width=section.page_width.emu - section.left_margin.emu - section.right_margin,
            height=None
        ).xml
        self._mod_pstyle_stack.append(self.style.image_caption)
        return '<w:r><w:drawing>{}</w:drawing></w:r><w:br/>'.format(pic) + inner

    def render_link(self, token):
        target = escape_url(token.target)

        self._suppress_rtag_stack.append(True)
        inner = self.render_inner(token)
        self._suppress_rtag_stack.pop()
        return make_run(self.style.href_caption, inner + " - ") + make_run(self.style.href_url, target)

    def render_raw_text(self, token):
        text = docx_escape(token.content).rstrip('\n').rstrip('\a')
        if self._suppress_rtag_stack[-1]:
            return text
        else:
            return make_run('', text)

    def render_heading(self, token):
        self.warnings.add('Markdown Headings are not implemented yet. It will be ignored')
        return ''

    def render_paragraph(self, token):
        inner = self.render_inner(token)

        try:
            style = self._mod_pstyle_stack.pop()
        except IndexError:
            style = self.style.paragraph

        if self._suppress_ptag_stack[-1]:
            return inner

        return make_paragraph(style, inner)

    def render_block_code(self, token):
        style = self.style.code
        return make_paragraph(style, self.render_inner(token))

    def render_list(self, token):
        if token.start:
            self._list_style_stack.append(self.style.ol)
        else:
            self._list_style_stack.append(self.style.ul)
        self._list_level += 1

        inner = self.render_inner(token)

        self._list_level -= 1
        self._list_style_stack.pop()
        return inner

    def render_list_item(self, token):
        style = self._list_style_stack[-1]
        self._suppress_ptag_stack.append(True)
        inner = self.render_inner(token)
        self._suppress_ptag_stack.pop()
        return make_paragraph(list_level_style(style, self._list_level), inner, self._list_level > 0)

    def render_table(self, token):
        self.warnings.add('Markdown Table is not implemented. It will be ignored')
        return ''

    def render_table_row(self, token, is_header=False):
        return ''

    def render_table_cell(self, token, in_header=False):
        return ''

    @staticmethod
    def render_separator(token):
        return '<w:p></w:p>'

    def render_document(self, token):
        self.footnotes.update(token.footnotes)
        ret = self.render_inner(token)
        self.warnings = self.warnings | self.style._warnings

        return ret


def markdown_to_docx(markdown, render: DOCXRenderer):
    ret = mistletoe.markdown('\n'.join(markdown.split('\r\n')), render)
    for warn in render.warnings:
        # TODO: something
        print(warn)

    return ret
