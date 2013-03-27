# Function performs a reverse lookup on a dictionary. Given an item
# in a dictioanry, finds the corresponding key for the first found item

def rev_lookup(dict,item):
        """
        Tests:	
	>>> a = { }
	>>> a['Hi'] = 5
        >>> a[56] = 234
	>>> rev_lookup(a,5)
	'Hi'
        >>> rev_lookup(a,234)
        56
	"""
        for key in dict.keys():
                if dict[key] == item:
                        return key

        return None

if __name__ == "__main__":
        import doctest
        doctest.testmod()
