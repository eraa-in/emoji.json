#!/usr/bin/env python3
import json
import re

def transform_emoji_data():
    # Read the original emoji.json file
    with open('emoji.json', 'r', encoding='utf-8') as f:
        emojis = json.load(f)
    
    # Categories that should have skin tone variations
    skin_tone_categories = [
        "People & Body",
        "Smileys & Emotion"
    ]
    
    # Group emojis by category
    categorized_emojis = {}
    
    for emoji in emojis:
        # Extract the main category (before the parentheses)
        category = emoji['category']
        main_category = category.split(' (')[0] if ' (' in category else category
        
        # Remove the category field from the emoji object
        emoji_copy = emoji.copy()
        del emoji_copy['category']
        
        # Initialize category if it doesn't exist
        if main_category not in categorized_emojis:
            categorized_emojis[main_category] = []
        
        # Add the emoji to its category
        categorized_emojis[main_category].append(emoji_copy)
    
    # Add skin tone variations for appropriate categories
    skin_tone_modifiers = [
        ("1F3FB", "🏻", "light skin tone"),
        ("1F3FC", "🏼", "medium-light skin tone"),
        ("1F3FD", "🏽", "medium skin tone"),
        ("1F3FE", "🏾", "medium-dark skin tone"),
        ("1F3FF", "🏿", "dark skin tone")
    ]
    
    for category_name, emoji_list in categorized_emojis.items():
        if category_name in skin_tone_categories:
            # Find emojis that can have skin tones (those without existing skin tone modifiers)
            base_emojis = []
            skin_tone_emojis = []
            
            for emoji in emoji_list:
                # Check if this emoji already has a skin tone modifier
                has_skin_tone = any(modifier in emoji['codes'] for _, modifier, _ in skin_tone_modifiers)
                
                if has_skin_tone:
                    skin_tone_emojis.append(emoji)
                else:
                    base_emojis.append(emoji)
            
            # Create skin tone variations for base emojis
            new_emojis = []
            for base_emoji in base_emojis:
                new_emojis.append(base_emoji)
                
                # Only add skin tone variations for emojis that represent people/body parts
                # Skip emojis that are already faces, hearts, etc.
                if (category_name == "People & Body" or 
                    (category_name == "Smileys & Emotion" and "face" in base_emoji.get('subgroup', ''))):
                    
                    for modifier_code, modifier_char, modifier_name in skin_tone_modifiers:
                        # Create skin tone variation
                        skin_tone_emoji = base_emoji.copy()
                        skin_tone_emoji['codes'] = f"{base_emoji['codes']} {modifier_code}"
                        skin_tone_emoji['char'] = f"{base_emoji['char']}{modifier_char}"
                        skin_tone_emoji['name'] = f"{base_emoji['name']}: {modifier_name}"
                        new_emojis.append(skin_tone_emoji)
            
            # Replace the category's emoji list with the new one
            categorized_emojis[category_name] = new_emojis
    
    # Write the transformed data to a new file
    with open('emoji_transformed.json', 'w', encoding='utf-8') as f:
        json.dump(categorized_emojis, f, ensure_ascii=False, indent=2)
    
    print(f"Transformation complete! Output saved to emoji_transformed.json")
    print(f"Categories found: {list(categorized_emojis.keys())}")
    
    # Print some statistics
    for category, emojis in categorized_emojis.items():
        print(f"{category}: {len(emojis)} emojis")

if __name__ == "__main__":
    transform_emoji_data()