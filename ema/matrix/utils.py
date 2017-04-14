# auswaehlbare Farben restriktieren, je nachdem welche schon vergeben sind
# pro User
# TODO warum ist das hier und nicht in den Forms?
def get_user_colors(thistopic, choices, topicList):
    options = []
    # alle moeglichen Choices
    for color in choices:
        gefunden = False
        # alle Topics des Nutzers
        for topic in topicList:
            if topic.color == color[0]:
                if topic == thistopic:
                    gefunden = False
                else:
                    gefunden = True
        if gefunden == False:
            options.append(color)
    return options
