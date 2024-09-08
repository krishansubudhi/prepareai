import inspect
from IPython.display import display, HTML, Image, Markdown
import re


class Tool():

    def _get_tool_metadata(self, excludes=()) -> str:
        """
        Extracts metadata from a tool instance, including function names, signatures, and docstrings,
        and formats it into a Markdown-like string.

        Args:
        - excludes (tuple): Names of attributes to exclude from metadata extraction.

        Returns:
        - str: A formatted string representation of the metadata in Markdown format.
        """
        tool_metadata = []

        # Add class-level docstring
        class_docstring = self.__class__.__doc__
        if class_docstring:
            # tool_metadata.append(f"### Class: {self.__class__.__name__}\n")
            tool_metadata.append(f"{class_docstring.strip()}\n")

        # Iterate over all attributes of the tool
        for name in dir(self):
            if name.startswith('_') or name in excludes:
                continue
            attr = getattr(self, name, None)
            if callable(attr):
                try:
                    # Inspect the method if it's callable
                    signature = inspect.signature(attr)
                    docstring = inspect.getdoc(attr)

                    params = signature.parameters
                    param_strings = []

                    # Process each parameter to show default values
                    for param_name, param in params.items():
                        if param.default is inspect.Parameter.empty:
                            param_strings.append(param_name)  # No default value
                        else:
                            param_strings.append(f"{param_name}={param.default!r}")  # With default value

                    # Join parameters with commas and construct the method signature
                    param_list = ", ".join(param_strings)
                    method_signature = f"{name}({param_list})"
                    
                    method_info = f"* `{name}{signature}` \t{'# ' + docstring.strip() if docstring else ''}"
                    tool_metadata.append(method_info)
                except Exception as e:
                    tool_metadata.append(f"**Error processing method {name}:** {e}\n")

        return "\n\n".join(tool_metadata)

    def _execute_code(self, code_to_execute):
        # Extract code from Markdown (assuming code is enclosed in triple backticks)
        code_pattern = re.compile(r'```(?:python)?\n(.*)\n```', re.DOTALL)
        match = code_pattern.search(code_to_execute)
        
        if match:
            code = match.group(1)
            # Display the code (optional)
            display(Markdown(f"```python\n{code}\n```"))
            try:
                exec(code, globals(), locals())
            except Exception as e:
                raise Exception(f"Error executing LLM-generated code: {str(e)}")
        else:
            print("No valid code block found.")
