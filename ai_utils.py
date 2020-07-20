

def turn_start_decision(ai_function, singles=True, **kwargs):
    """:argument
    ai_function: a function returning either two strings or two lists.
        If two strings, the first one is the action to perform (either "move" or "switch")
        and the second is the target of the action (an attack name if "move" or a pokémon name if "switch").
        If 'singles' is False, the decision is expected to be used for doubles.
        Therefore, the function is expected to return a list of two actions and a list of two targets
        (a pair action-target is determined by their index number).
    singles: a boolean. True if the battle format is singles and False if doubles
    kwargs: the arguments needed for ai_function
    """

    actions, targets = ai_function(kwargs)
    if singles:
        if actions != "move" and actions != "switch":
            raise ValueError("%s is not a valid action. Check you AI function." % actions)
    else:
        if type(actions) is not list or type(targets) is not list:
            raise ValueError("Either actions or targets are not a list. Check your AI function.")
        if len(actions) != 2 or len(targets) != 2:
            raise ValueError("Either actions or targets doesn't have exactly two elements. Check your AI function.")

    return actions, targets