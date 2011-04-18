__all__ = ['merge_lists']


# HELPER FUNCTION FOR MERGING LISTS
def merge_lists(*args, **kwargs):
    merged = []
    for seq in args:
        for element in seq:
            merged.append(element)
    return merged