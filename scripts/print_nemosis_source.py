import inspect
import nemosis

print("Signature of dynamic_data_compiler:")
print(inspect.signature(nemosis.dynamic_data_compiler))

print("\nSource code of dynamic_data_compiler:")
try:
    print(inspect.getsource(nemosis.dynamic_data_compiler))
except Exception as e:
    print("Could not get source directly:", e)
    # Print the source of the module defining it
    module = inspect.getmodule(nemosis.dynamic_data_compiler)
    print("Defining module:", module)
    if module:
        print("Module file:", inspect.getfile(module))
