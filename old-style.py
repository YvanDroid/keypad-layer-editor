import layer_handler as lh

from layers import layer_details, layer_titles
print(layer_titles)
filename = input("please enter the filename to output:\n")
with open(filename,"w+") as json_file:
    json_file.write(lh.json_serialise(layer_details))




