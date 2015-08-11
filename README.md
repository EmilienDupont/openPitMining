# Facility Location
An example of using Gurobi to solve an open-pit mining problem.

![](screenshot.png?raw=true)

# Running the example

1. Start Python's webserver from the command line
    ```
    make
    ```

2. Point your browser at http://localhost:8000

3. Change the block types by clicking them.

4. Click "Compute" to find the optimal mining order.

# Performing an optimization

To just solve the model (without running a web server) do:

```
make test
```
