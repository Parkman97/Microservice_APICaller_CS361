def dataParser(data):
    space_dict = data["results"]
    for story in space_dict:
        story.pop("featured", None)
        story.pop("events", None)
    
    return space_dict