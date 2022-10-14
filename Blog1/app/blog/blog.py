#markdown转换
def markdownTurn(mdcontext):
    import markdown2
    html_text = markdown2.markdown(mdcontext)
    retuen html_text #用于转换md到html
