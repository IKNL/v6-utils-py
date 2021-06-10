<h1 align="center">
  <br>
  <a href="https://vantage6.ai"><img src="https://github.com/IKNL/guidelines/blob/master/resources/logos/vantage6.png?raw=true" alt="vantage6" width="400"></a>
</h1>

<h3 align=center> A privacy preserving federated learning solution</h3>

--------------------

# Federated Utilities

|:warning: priVAcy preserviNg federaTed leArninG infrastructurE for Secure Insight eXchange (VANTAGE6) |
|------------------|
| This algorithm is part of [VANTAGE6](https://github.com/IKNL/vantage6). A docker build of this algorithm can be obtained from harbor.vantage6.ai/algorithms/utils |

Collection of tools that can be used on vantage6-nodes.

* `fetch_static_file` - Obtain a static file from the node
* ...


## Usage
```python
from vantage6.client import Client

# Create, athenticate and setup client
client = Client("http://127.0.0.1", 5000, "")
client.authenticate("frank@iknl.nl", "password")
client.setup_encryption(None)

# Define algorithm input
input_ = {
    "method":"fetch_static_file",
    "args": [],
    "kwargs": {'filename': 'name_of_the_static_file.pdf'} # optional argument
}

# Send the task to the central server
task = client.task.create(
    name="testing",
    image="harbor.vantage6.ai/algorithms/utils",
    collaboration=1,
    input=input_,
    description="Human readable description",
    organizations=[2]
)

# Retrieve the task information
task_info = client.task.get(
  id_=task.get("id"),
  include_results=True
)

# Retrieve the result (file in this case)
res = client.result.get(task_info['results'][0]['id'])
result = res['result']

# Write the bytes to a file
with open('name_of_the_static_file.pdf', 'wb') as f:
  f.write(result)

```

## Node configuration
The algorithm looks by default in the `/mnt/data` folder for the file. It is possible to let the algorithm use a different folder by specifying the algorithm environment variable `STATIC_FOLDER`. It is also possible to specify a default file name by setting `STATIC_FILENAME`. Note that the user argument `filename` has priority. Add the block `algorithm_env` to the node configuration file to do so:

```yaml
  application:
    ...
    algorithm_env:
      STATIC_FOLDER: /mnt/data/some/other/folder
      STATIC_FILENAME: filename.txt
    ...
```

------------------------------------
> [vantage6](https://vantage6.ai)