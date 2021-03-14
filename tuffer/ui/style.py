from questionary import Style

custom_style = Style(
    [
        # token in front of the question
        ("qmark", "fg:#673ab7 bold"),
        # question text
        ("question", "bold"),
        # submitted answer text behind the question
        ("answer", "fg:#f44336 bold"),
        # pointer used in select and checkbox prompts
        ("pointer", "fg:#673ab7 bold"),
        # pointed-at choice in select and checkbox prompts
        ("highlighted", "fg:#673ab7 bold"),
        # style for a selected item of a checkbox
        ("selected", "fg:#cc5454"),
        # separator in lists
        ("separator", "fg:#cc5454"),
        # user instructions for select, rawselect, checkbox
        ("instruction", ""),
        # plain text
        ("text", ""),
        # disabled choices for select and checkbox prompts
        ("disabled", "fg:#858585 italic"),
    ]
)
