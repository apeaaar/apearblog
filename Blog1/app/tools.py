import markdown


def mdToHtml(md_text):
    html_text = markdown.markdown(md_text)
    return html_text
