# auswaehlbare Farben restriktieren, je nachdem welche schon vergeben sind
# pro User
def get_user_colors(choices, topicList):
    options = []
    for color in choices:
        gefunden = False
        for topic in topicList:
            if topic.color == color[0]:
                gefunden = True
        if gefunden == False:
            options.append(color)
    return options
