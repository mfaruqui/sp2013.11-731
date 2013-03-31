# returns the list of all subspans in the list l
def get_subspans(l):
    if len(l) <= 1:
        return [l]
    subspans = []
    for i in range(0, len(l)):
        for j in range(i, len(l)):
            subspans.append(l[i:j+1])
    return subspans
    
def get_free_spans2(bit_array):
    first_uncovered = bit_array.index(False)
    spans = []
    for to_index in range(first_uncovered, len(bit_array)):
        spans.append(range(first_uncovered, to_index+1))
    
    return spans

def get_free_spans(bit_array):
    
    seqOn = False
    spans = []
    newSpan = []
    for i, covered in enumerate(bit_array):
        if not covered:
            seqOn = True
            newSpan.append(i)
        elif seqOn:
            spans += get_subspans(newSpan)
            newSpan = []
            seqOn = False
    
    if newSpan != []:
        spans += get_subspans(newSpan)
        
    return spans
    
