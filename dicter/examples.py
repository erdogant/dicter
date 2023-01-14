# %%
import dicter as dt
# print(dir(dt))
# print(dt.__version__)

# %%
d = {'a': 1, 'b': {'f': 'hello world'}, 'c': 3, 'd': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'g': 2}
paths = dt.traverse(d)

# %%
data = {
    "spam": {
        "egg": {
            "bacon": "Well..",
            "sausages": "Spam egg sausages and spam",
            "spam": "does not have much spam in it"
        }
    }
}

print('spam (exists): {}'.format(dt.is_key(data, ["spam"])))
print('spam > bacon (do not exists): {}'.format(dt.is_key(data, ["spam", "bacon"])))
print('spam > egg (exists): {}'.format(dt.is_key(data, ["spam", "egg"])))
print('spam > egg > bacon (exists): {}'.format(dt.is_key(data, ["spam", "egg", "bacon"])))
