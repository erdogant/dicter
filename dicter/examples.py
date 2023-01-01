# %%
import dicter as dt
# print(dir(dt))
# print(dt.__version__)

# %%
d = {'a': 1, 'b': {'f': 'hello world'}, 'c': 3, 'd': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'g': 2}
paths = dt.path(d)

# %%
dt.messages(verbose=10)
