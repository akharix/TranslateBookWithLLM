from src.config import TRANSLATE_TAG_IN, TRANSLATE_TAG_OUT, INPUT_TAG_IN, INPUT_TAG_OUT

def generate_translation_prompt(main_content, context_before, context_after, previous_translation_context,
                               source_language="Korean", 
                               target_language="English", 
                               translate_tag_in=TRANSLATE_TAG_IN, translate_tag_out=TRANSLATE_TAG_OUT,
                               custom_instructions=""):
    """
    Generate the translation prompt with all contextual elements.
    
    Returns:
    str: The complete prompt formatted for translation
    """
    source_lang = source_language.upper()

    # PROMPT - can be edited for custom usages
# You are a {target_language} writer
    role_and_instructions_block = f"""
## ROLE
# You are a professional writer and translator, specializing in {source_language} and {target_language} novels.

## TRANSLATION
+ Translate in the author's style
+ Preserve meaning and enhance fluidity
+ Adapt expressions and culture to the {target_language} language
+ Maintain the original layout of the text
+ Do NOT translate: code snippets, command lines, function names, variable names, URLs, file paths, or any technical syntax

## FORMATING
+ Translate ONLY the text enclosed within the tags "{INPUT_TAG_IN}" and "{INPUT_TAG_OUT}" from {source_lang} into {target_language}
+ Surround your translation with {translate_tag_in} and {translate_tag_out} tags. For example: {translate_tag_in}Your text translated here.{translate_tag_out}
+ Return ONLY the translation, formatted as requested
+ IMPORTANT: Preserve all special spaces and indentation exactly as they appear in the source text
+ Do NOT convert spaces to HTML entities like &nbsp; - maintain the original spacing
+ IMPORTANT: If you see placeholders like ⟦TAG0⟧, ⟦TAG1⟧, etc., these represent HTML/XML tags. Keep these placeholders EXACTLY as they appear in their original positions. Do NOT translate or modify these placeholders
"""

    previous_translation_block_text = ""
    if previous_translation_context and previous_translation_context.strip():
        previous_translation_block_text = f"""

## Previous paragraph :
(...) {previous_translation_context}

"""

    custom_instructions_block = ""
    if custom_instructions and custom_instructions.strip():
        custom_instructions_block = f"""

### INSTRUCTIONS
{custom_instructions.strip()}

"""

    text_to_translate_block = f"""
{INPUT_TAG_IN}
{main_content}
{INPUT_TAG_OUT}"""

    structured_prompt_parts = [
        role_and_instructions_block,
        custom_instructions_block,
        previous_translation_block_text,
        text_to_translate_block
    ]
    
    return "\n\n".join(part.strip() for part in structured_prompt_parts if part and part.strip()).strip()


def generate_subtitle_block_prompt(subtitle_blocks, previous_translation_block, 
                                 source_language="Korean", target_language="English",
                                 translate_tag_in=TRANSLATE_TAG_IN, translate_tag_out=TRANSLATE_TAG_OUT,
                                 custom_instructions=""):
    """
    Generate translation prompt for multiple subtitle blocks with index markers.
    
    Args:
        subtitle_blocks: List of tuples (index, text) for subtitles to translate
        previous_translation_block: Previous translated block for context
        source_language: Source language 
        target_language: Target language
        translate_tag_in/out: Tags for translation markers
        custom_instructions: Additional translation instructions
        
    Returns:
        str: The complete prompt formatted for subtitle block translation
    """
    source_lang = source_language.upper()
    
    # Enhanced instructions for subtitle translation
    role_and_instructions_block = f"""
## ROLE
# You are a {source_language} - {target_language} subtitle translator and dialogue adaptation specialist.

## TRANSLATION
+ Translate dialogues naturally for subtitles
+ Adapt expressions and {source_language} cultural references for {target_language} viewers
+ Keep subtitle length appropriate for reading speed
+ Ensure consistent use of unique names, titles and locations. For example: if a certain character is first translation as "Queen of Waves and Healing", then that name should be used consistently throughout the translation
+ Ensure consistent use of character' genders and formal pronouns
+ Make sure there isn't any untranslated {source_language} characters across the translation


## FORMATING
+ Translate ONLY the text enclosed within the tags "{INPUT_TAG_IN}" and "{INPUT_TAG_OUT}" from {source_lang} into {target_language}
+ Each subtitle is marked with its index: [index]text
+ Preserve the index markers in your translation
+ Surround your ENTIRE translation block with {translate_tag_in} and {translate_tag_out} tags
+ Return ONLY the translation block, formatted as requested
+ Maintain line breaks between indexed subtitles
"""

    # Custom instructions
    custom_instructions_block = ""
    if custom_instructions and custom_instructions.strip():
        custom_instructions_block = f"""
### ADDITIONAL INSTRUCTIONS
{custom_instructions.strip()}
"""
        
    # Previous translation context
    previous_translation_block_text = ""
    if previous_translation_block and previous_translation_block.strip():
        previous_translation_block_text = f"""
## Previous subtitle block (for context and consistency):
{previous_translation_block}
"""
        
    # Format subtitle blocks with indices
    formatted_subtitles = []
    for idx, text in subtitle_blocks:
        formatted_subtitles.append(f"[{idx}]{text}")
    
    text_to_translate_block = f"""
{INPUT_TAG_IN}
{chr(10).join(formatted_subtitles)}
{INPUT_TAG_OUT}"""

    structured_prompt_parts = [
        role_and_instructions_block,
        custom_instructions_block,
        previous_translation_block_text,
        text_to_translate_block
    ]
    
    return "\n\n".join(part.strip() for part in structured_prompt_parts if part and part.strip()).strip()


def generate_post_processing_prompt(translated_text, target_language="English", 
                                  translate_tag_in=TRANSLATE_TAG_IN, translate_tag_out=TRANSLATE_TAG_OUT,
                                  custom_instructions=""):
    """
    Generate the post-processing prompt to improve translated text quality.
    
    Args:
        translated_text: The already translated text to improve
        target_language: Target language for the text
        translate_tag_in/out: Tags for marking the improved text
        custom_instructions: Additional improvement instructions
        
    Returns:
        str: The complete prompt formatted for post-processing
    """
    
    role_and_instructions_block = f"""
## ROLE
# You are a professional {target_language} editor and proofreader.

## TASK
+ Review and improve the quality of the {target_language} text
+ Enhance fluidity and naturalness while preserving the original meaning
+ Correct any grammatical errors or awkward phrasing
+ Ensure consistency in style and tone
+ Ensure consistency of the translated translated names, titles, locations.
+ Ensure consistent use of formal pronouns and character' genders in the translation
+ Verify technical terminology accuracy
+ Make the text read as if originally written in {target_language}

## FORMATTING
+ Review ONLY the text enclosed within the tags "{INPUT_TAG_IN}" and "{INPUT_TAG_OUT}"
+ Surround your improved version with {translate_tag_in} and {translate_tag_out} tags
+ Return ONLY the improved text, formatted as requested
+ Preserve all formatting, spacing, and special characters from the original
+ Keep placeholders like ⟦TAG0⟧, ⟦TAG1⟧ exactly as they appear
"""

    custom_instructions_block = ""
    if custom_instructions and custom_instructions.strip():
        custom_instructions_block = f"""

### ADDITIONAL INSTRUCTIONS
{custom_instructions.strip()}

"""

    text_to_improve_block = f"""
{INPUT_TAG_IN}
{translated_text}
{INPUT_TAG_OUT}"""

    structured_prompt_parts = [
        role_and_instructions_block,
        custom_instructions_block,
        text_to_improve_block
    ]
    
    return "\n\n".join(part.strip() for part in structured_prompt_parts if part and part.strip()).strip()