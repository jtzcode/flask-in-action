
def flattenBookmarks(marks, results):
    for link in marks:
        if 'children' in link:
            flattenBookmarks(link['children'], results)
        else:
            results.append(link)