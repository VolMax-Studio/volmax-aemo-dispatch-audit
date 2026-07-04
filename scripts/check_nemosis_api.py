import inspect
import nemosis

print("nemosis version:", nemosis.__version__)
print("\nSignature of dynamic_data_compiler:")
print(inspect.signature(nemosis.dynamic_data_compiler))

# Get file where it is defined
print("\nDefined in file:", inspect.getfile(nemosis.dynamic_data_compiler))
