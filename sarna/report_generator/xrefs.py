from sarna.report_generator import *

_xrefs_runs = """
<w:r>
    <w:rPr></w:rPr>
    <w:fldChar w:fldCharType="begin"></w:fldChar>
</w:r>
<w:r>
    <w:rPr></w:rPr>
    <w:instrText> REF {ref} {ops} </w:instrText>
</w:r>
<w:r>
    <w:rPr></w:rPr>
    <w:fldChar w:fldCharType="separate"/>
</w:r>
<w:r>
    <w:rPr></w:rPr>
    <w:t>[ref]</w:t>
</w:r>
<w:r>
    <w:rPr></w:rPr>
    <w:fldChar w:fldCharType="end"/>
</w:r>
"""

_bookmark = """
<w:bookmarkStart w:id="{ref}" w:name="{ref}"/>
<w:bookmarkEnd w:id="{ref}"/>
{run}
"""


def _ref_name(elem):
    return "__{}__{:010d}".format(elem.__class__.__name__, elem.id)


def xref(elem, type='number'):
    ref_name = _ref_name(elem)
    ref_ops = ""
    if type == 'number':
        ref_ops = "\\r \\h"
    elif type == 'title':
        ref_ops = "\\h"

    return _xrefs_runs.format(ref=ref_name, ops=ref_ops)


def bookmark(elem, attr):
    run = make_run('', getattr(elem, attr))
    return _bookmark.format(ref=_ref_name(elem), run=run)


__all__ = ['xref', 'bookmark']
