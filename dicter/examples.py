# %%
import dicter as dt
# print(dir(dt))
# print(dt.__version__)

# %% Verbose test
import dicter as dt
dt.check_logger(verbose=0)
dt.check_logger(verbose=1)
dt.check_logger(verbose=2)
dt.check_logger(verbose=3)
dt.check_logger(verbose=4)
dt.check_logger(verbose=5)
dt.check_logger(verbose=6)

dt.check_logger(verbose=0)
dt.check_logger(verbose=20)
dt.check_logger(verbose=30)
dt.check_logger(verbose=40)
dt.check_logger(verbose=50)

dt.check_logger(verbose='silent')
dt.check_logger(verbose='debug')
dt.check_logger(verbose='info')
dt.check_logger(verbose='warning')
dt.check_logger(verbose='error')

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
