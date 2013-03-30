from capital import Item

# Test reliability operations. 
# Note: item initialization argument order: 
# cost,rel,icon,lifespan,maintenance,sug_maint

newItem = Item(("Item",20000,0.8,1,1000,900,100))

# Test how many turns till the item fails.
i = 0
while newItem.Update() == False:
    i = i + 1

print(i)
