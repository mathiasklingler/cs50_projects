def get_color_for_attention_score(attention_score):
    """
    Return a tuple of three integers representing a shade of gray for the
    given `attention_score`. Each value should be in the range [0, 255].
    """
    shade = attention_score * 255
    shade_int = int(shade)
    print(shade)
    print(shade_int)
    color = tuple((shade_int, shade_int, shade_int))
    print(color)
    return tuple()

a = get_color_for_attention_score(0.25)