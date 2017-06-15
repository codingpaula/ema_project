"""Auswaehlbare Farben restriktieren, je nachdem welche schon vergeben sind."""


def get_user_colors(thistopic, choices, topicList):
    """Pro User diese Topic bekommt Farben, welche noch nicht vergeben sind."""
    # TODO warum ist das hier und nicht in den Forms?
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
        if not gefunden:
            options.append(color)
    return options
