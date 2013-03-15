from capital_database import Item

# Test reliability operations. 
# Note: item initialization argument order: 
# cost,rel,icon,lifespan,maintenance,sug_maint

newItem = Item(20000,1,1,100,100,100)

# Test how many turns till the item fails.
i = 0
while newItem.Update() == False:
    i = i + 1

print(i)
