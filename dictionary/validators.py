from django.core.exceptions import ValidationError

MAX_VOCAB_CATEGORIES = 3

def validate_category_count(categories, *, min_count=0, max_count=MAX_VOCAB_CATEGORIES):
    categories_list = list(categories)
    categories_count = len(categories_list)

    if categories_count < min_count:
        raise ValidationError(
            f"Select at least {min_count} category."
        )
    if categories_count > max_count:
        raise ValidationError(
            f"Select no more than {max_count} categories."
        )

    return categories_list