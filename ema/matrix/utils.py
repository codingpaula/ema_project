# auswaehlbare Farben restriktieren, je nachdem welche schon vergeben sind
# pro User
def get_user_colors(thistopic, choices, topicList):
    options = []
    # durch alle choices
    for color in choices:
        gefunden = False
        # durch alle topics
        for topic in topicList:
            if topic.color == color[0]:
                if topic == thistopic:
                    gefunden = False
                else:
                    gefunden = True
        if gefunden == False:
            options.append(color)
    return options
