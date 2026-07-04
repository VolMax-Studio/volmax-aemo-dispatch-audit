import nemosis.defaults as defs
import inspect

# Print attributes of defs
for attr in dir(defs):
    if 'url' in attr.lower() or 'server' in attr.lower():
        print(f"{attr}: {getattr(defs, attr)}")
