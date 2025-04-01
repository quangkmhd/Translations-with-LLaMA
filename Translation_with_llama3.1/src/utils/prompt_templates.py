def get_translation_prompt(text, source_lang, target_lang, cultural_context):
    """
    Returns a simplified prompt for translating the given text while considering cultural context.
    """
    return f"""
    Translate the following text from {source_lang} to {target_lang}, adapting it to a {cultural_context} context:

    "{text}"

    Translation:
    - [Your translated text here]

    """
