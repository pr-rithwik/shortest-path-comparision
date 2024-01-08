### Organisation
- All the code is in the repo `code`.
- All the data is in the repo `data`.
- All testing happens in the repo `tests`.

### Technical Approach
- Solve for the shortest path given two actor names.

#### Approach
- There is a chance for an existence of multiple actors with the same name, so need to handle it with the birth year provided in the data.
- Need to check if the chosen/given actor names exist in the data.
- I will be using/exploring the algorithms provided in the `networkx` module for the shortest possible path. I won't be implementing the algorithms from the ground up.
    - Execution times for each of the algorithm will be contrasted to see which may be a better one.
- All the data handling has to be done in one place.
    - data frames, dictionaries and everyth datastore that we may need will be handled in this single place.
- All the validations has to be done in one place.
    - Use the datastores created above to handle the exceptions accordingly.
- All/Most of the strings and constants that we need will be stored in one place to make global changes easier.

### Best Practices
- Write down the approach to solve the project to get the structured flow.
- Write the overall code as the function calls and declaring them when necessary.
    - For every sub-category not just solution. eg: data, solution, tests, validations.